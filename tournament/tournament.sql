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
	score integer DEFAULT 0, 
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
CREATE VIEW match_details AS
    select e.match_id, a.player_name as player1, 
    b.player_name as player2 from players a, players b, 
    eventmatches e where a.player_id = e.player1_id and 
    b.player_id  = e.player2_id order by e.event_id, e.match_id;

-- insert script for testing
-- players table
insert into players (player_name,player_email) values ('player 1', 'player1@email.com');
insert into players (player_name,player_email) values ('player 2', 'player2@email.com');
insert into players (player_name,player_email) values ('player 3', 'player3@email.com');
insert into players (player_name,player_email) values ('player 4', 'player4@email.com');
insert into players (player_name,player_email) values ('player 5', 'player5@email.com');
insert into players (player_name,player_email) values ('player 6', 'player6@email.com');
insert into players (player_name,player_email) values ('player 7', 'player7@email.com');
insert into players (player_name,player_email) values ('player 8', 'player8@email.com');
insert into players (player_name,player_email) values ('player 9', 'player9@email.com');
insert into players (player_name,player_email) values ('player 10', 'player10@email.com');
insert into players (player_name,player_email) values ('player 11', 'player11@email.com');
insert into players (player_name,player_email) values ('player 12', 'player12@email.com');
insert into players (player_name,player_email) values ('player 13', 'player13@email.com');
insert into players (player_name,player_email) values ('player 14', 'player14@email.com');
insert into players (player_name,player_email) values ('player 15', 'player15@email.com');
insert into players (player_name,player_email) values ('player 16', 'player16@email.com');	

-- events table
insert into events (id,name) values(1, 'Chess Championship 2015');

-- event players
insert into eventplayers (id,event_id,player_id) values (1,1,1);
insert into eventplayers (id,event_id,player_id) values (2,1,2);
insert into eventplayers (id,event_id,player_id) values (3,1,3);
insert into eventplayers (id,event_id,player_id) values (4,1,4);
insert into eventplayers (id,event_id,player_id) values (5,1,5);
insert into eventplayers (id,event_id,player_id) values (6,1,6);
insert into eventplayers (id,event_id,player_id) values (7,1,7);
insert into eventplayers (id,event_id,player_id) values (8,1,8);
insert into eventplayers (id,event_id,player_id) values (9,1,9);
insert into eventplayers (id,event_id,player_id) values (10,1,10);
insert into eventplayers (id,event_id,player_id) values (11,1,11);
insert into eventplayers (id,event_id,player_id) values (12,1,12);
insert into eventplayers (id,event_id,player_id) values (13,1,13);
insert into eventplayers (id,event_id,player_id) values (14,1,14);
insert into eventplayers (id,event_id,player_id) values (15,1,15);
insert into eventplayers (id,event_id,player_id) values (16,1,16);

-- eventgamemapper table
insert into eventgamemapper (event_id,game_id) values (1,1);

-- eventgamerounds table 
insert into eventgamerounds (event_id,round_id) values (1,1);

-- eventmatches table assuming matches have been played
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,1,1,3,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,2,5,7,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,3,9,11,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,4,13,15,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,5,2,4,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,6,6,8,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,7,10,12,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,8,14,16,TRUE);

-- player score assuming the first player won.
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (1,1,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (1,3,1,1,2,0);

insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (2,5,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (2,7,1,1,2,0);

insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (3,9,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (3,11,1,1,2,0);

insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (4,13,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (4,15,1,1,2,0);

insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (5,2,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (5,4,1,1,2,0);

insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (6,6,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (6,8,1,1,2,0);

insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (7,10,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (7,12,1,1,2,0);		

insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (8,14,1,1,1,1);
insert into playerscore (match_id, player_id, game_number,
	round_number, match_result, score) values (8,16,1,1,2,0);



