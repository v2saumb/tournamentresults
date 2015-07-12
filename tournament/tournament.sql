-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- Table resultmaster
-- table contains different resutls and their meanings
CREATE TABLE resultmaster(id serial PRIMARY KEY, name TEXT NOT NULL);

-- insert scripts for the results master
-- do not remove required for the functioning of the program.
insert into resultmaster (id, name) values (1,'WON');
insert into resultmaster (id, name) values (2,'LOST');
insert into resultmaster (id, name) values (3,'DRAW');
insert into resultmaster (id, name) values (4,'BYEWIN');


-- Table Players
-- Contain detail of the players with their unique id
CREATE TABLE players(player_id serial PRIMARY KEY,
	player_name Text not null,
	player_email Text);

-- Table events 
-- This table contains the names and Ids of the different events
CREATE TABLE events (id serial PRIMARY KEY,name Text NOT NULL);

-- Table event Players Contains information of which of the registered
-- players are playing in a  tournament
CREATE TABLE eventplayers (id serial UNIQUE,
	event_id integer REFERENCES events ON DELETE CASCADE,
	player_id integer REFERENCES players (player_id) ON DELETE CASCADE,
	PRIMARY KEY (event_id, player_id)
	);

-- Table eventgamemapper
-- should have at least one row in this table
-- and one row for number of games played per match
CREATE TABLE eventgamemapper(game_id serial UNIQUE,
	event_id integer REFERENCES events(id) ON DELETE CASCADE,
	game_number integer,
	PRIMARY KEY (game_number, event_id) );

-- Table eventgamerounds
-- should have at least one row in this table
-- and one row for number of round played per match
CREATE TABLE eventgamerounds(round_id serial UNIQUE,
	event_id integer REFERENCES events(id) ON DELETE CASCADE,
	round_number integer,
	PRIMARY KEY (round_number, event_id) );

-- Table Matches
-- This table will contain all who plays against whom and for what event
CREATE TABLE eventmatches(event_id integer REFERENCES events ON DELETE CASCADE,
	match_id serial UNIQUE,
	player1_id integer REFERENCES eventplayers(id) ON DELETE CASCADE,
	player2_id integer REFERENCES eventplayers(id) ON DELETE CASCADE,
	played boolean DEFAULT FALSE,
	PRIMARY KEY (event_id, player1_id, player2_id));


-- Table playerscore
-- Table will contain the score for various eventmatches 
CREATE TABLE playerscore(event_id integer REFERENCES events ON DELETE CASCADE,
	match_id integer REFERENCES eventmatches(match_id) ON DELETE CASCADE,
	player_id integer REFERENCES eventplayers(id) ON DELETE CASCADE,
	game_number integer, 
	round_number integer,
	match_result integer REFERENCES resultmaster(id), 
	game_score integer DEFAULT 0, 
	match_score integer DEFAULT 0, 
	PRIMARY KEY (player_id,match_id,game_number,round_number),
	FOREIGN KEY (game_number, event_id) REFERENCES eventgamemapper (game_number, event_id),
	FOREIGN KEY (round_number, event_id) REFERENCES eventgamerounds (round_number, event_id));

-- Table eventbyewinners
-- contains information if any player won by a bye of free win.
CREATE TABLE eventbyewinners(event_id integer REFERENCES events(id) ON DELETE CASCADE,
	match_id integer REFERENCES eventmatches(match_id) ON DELETE CASCADE,
	player_id integer REFERENCES players ON DELETE CASCADE,
	PRIMARY KEY (event_id,player_id,match_id));  

-- FUNCTIONS
-- playercount
-- returns the count of number of players in each event
CREATE OR REPLACE FUNCTION playercount(integer) RETURNS BIGINT
    AS 'select count(event_id) as player_count from eventplayers where event_id =$1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS 0 ON NULL INPUT;

-- matchresultcount
-- returns the count of number of players in each event
CREATE OR REPLACE FUNCTION matchresultcount(integer,integer,integer) RETURNS BIGINT
    AS 'select coalesce(count(match_id),0) as result from playerscore where
     player_id =$1 and match_result = $2 and event_id=$3;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS 0 ON NULL INPUT;

-- matchcount
-- returns the count of number of matches played by a player in an event
CREATE OR REPLACE FUNCTION playermatchcount(integer,integer) RETURNS BIGINT
    AS 'select coalesce(count(match_id),0) as result from playerscore where
     player_id =$1 and event_id=$2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS 0 ON NULL INPUT;   


--VIEWS
-- Match Details -- lists the matches along with the player names.
CREATE OR REPLACE VIEW match_details AS
    select e.event_id, e.match_id, a.player_name as player1, 
    b.player_name as player2 from players a, players b, 
    eventmatches e , eventplayers ep , eventplayers ep2 where a.player_id = ep.player_id and 
    ep.id=e.player1_id and  b.player_id  = ep2.player_id 
    and ep2.id = e.player2_id
    order by e.event_id, e.match_id;


-- Player Standing
CREATE OR REPLACE VIEW player_standing AS
	select coalesce(ep.event_id,0) as event_id,ep.id as playerId,p.player_name as player_name,sum(coalesce(ps.game_score,0)) as gamepoints,
	sum(coalesce(ps.match_score,0)) as matchpoints,
	sum(coalesce(ps.game_score,0)+coalesce(ps.match_score,0)) as totalpoints,
	coalesce(playermatchcount(ps.player_id,ep.event_id),0) as matchesplayed,
	coalesce(matchresultcount(ps.player_id,1,ep.event_id),0) as won,
	coalesce(matchresultcount(ps.player_id,2,ep.event_id),0) as lost, 
	coalesce(matchresultcount(ps.player_id,3,ep.event_id),0) as draw,
	coalesce(matchresultcount(ps.player_id,4,ep.event_id),0) as bye
	from eventplayers ep  left join playerscore ps on ps.player_id = ep.id , players p
	where p.player_id = ep.player_id
	Group by ep.event_id,p.player_name,ep.id,ps.player_id,ep.player_id 
	order by totalpoints desc ,matchesplayed desc,won desc, lost desc ,
	draw desc,ep.event_id asc, ep.player_id asc ;

 

 