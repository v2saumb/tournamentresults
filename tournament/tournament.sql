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
CREATE TABLE eventgamemapper(event_id integer REFERENCES events(id) ON DELETE CASCADE,
	game_id integer UNIQUE,
	PRIMARY KEY (game_id, event_id) );

-- Table eventgamerounds
-- should have at least one row in this table
-- and one row for number of round played per match
CREATE TABLE eventgamerounds(event_id integer REFERENCES events(id) ON DELETE CASCADE,
	round_id integer UNIQUE,
	PRIMARY KEY (round_id, event_id) );

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
CREATE TABLE playerscore(match_id integer REFERENCES eventmatches(match_id) ON DELETE CASCADE,
	player_id integer REFERENCES players ON DELETE CASCADE,
	game_number integer REFERENCES eventgamemapper(game_id),
	round_number integer REFERENCES eventgamerounds(round_id),
	match_result integer REFERENCES resultmaster(id), 
	game_score integer DEFAULT 0, 
	match_score integer DEFAULT 0, 
	PRIMARY KEY (player_id,match_id,game_number,round_number));

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
    RETURNS NULL ON NULL INPUT;

--VIEWS
-- Match Details -- lists the matches along with the player names.
CREATE OR REPLACE VIEW match_details AS
    select e.match_id, a.player_name as player1, 
    b.player_name as player2 from players a, players b, 
    eventmatches e where a.player_id = e.player1_id and 
    b.player_id  = e.player2_id order by e.event_id, e.match_id;

-- Player Standing

select p.player_name as playername,sum(ps.game_score) as gamepoints,sum(ps.match_score) as matchpoints,
sum(ps.game_score+ps.match_score) as totalpoints, count(ps.match_id) as matchesplayed
 from players p, playerscore ps 
 where p.player_id = ps.player_id 
 group by p.player_name,ps.player_id order by totalpoints desc ;

