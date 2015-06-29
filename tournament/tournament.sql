-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- Table resultmaster
-- table contains different resutls and their meanings
CREATE TABLE resultmaster(id serial PRIMARY KEY, name TEXT NOT NULL);

-- insert scripts for the results master
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
	game_id number,
	UNIQUE (id, event_id) );

-- Table eventgamerounds
-- should have at least one row in this table
-- and one row for number of round played per match
CREATE TABLE eventgamerounds(event_id integer REFERENCES events(id) ON DELETE CASCADE,
	round_id number,
	UNIQUE (id, event_id) );

-- Table Matches
-- This table will contain all who plays against whom and for what event
CREATE TABLE eventmatches(match_id serial UNIQUE,event_id integer 
	REFERENCES events ON DELETE CASCADE,
	player1_id integer REFERENCES eventplayers(id) ON DELETE CASCADE,
	player2_id integer REFERENCES eventplayers(id) ON DELETE CASCADE,
	played boolean DEFAULT false,  PRIMARY KEY (event_id, player1_id, player2_id));


-- Table playerscore
-- Table will contain the score for various eventmatches 
CREATE TABLE matchscore(event_id integer REFERENCES events(id) ON DELETE CASCADE,
	match_id integer REFERENCES eventmatches(match_id) ON DELETE CASCADE,
	player_id integer REFERENCES players ON DELETE CASCADE,
	score integer DEFAULT 0, 
	game_number integer REFERENCES eventgamemapper(game_id),
	round_number integer REFERENCES eventgamerounds(round_id),
	match_result integer REFERENCES resultmaster(id), 
	PRIMARY KEY (event_id,player_id,match_id,game_number,round_number));

-- Table eventbyewinners
-- contains information if any player won by a bye of free win.
CREATE TABLE eventbyewinners(event_id integer REFERENCES events(id) ON DELETE CASCADE,
	match_id integer REFERENCES eventmatches(match_id) ON DELETE CASCADE,
	player_id integer REFERENCES players ON DELETE CASCADE,
	PRIMARY KEY (event_id,player_id,match_id));  

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
insert into eventplayers (id,event_id,player_id) value (1,1,1);--
insert into eventplayers (id,event_id,player_id) value (1,1,2);
insert into eventplayers (id,event_id,player_id) value (1,1,3);--
insert into eventplayers (id,event_id,player_id) value (1,1,4);
insert into eventplayers (id,event_id,player_id) value (1,1,5);--
insert into eventplayers (id,event_id,player_id) value (1,1,6);
insert into eventplayers (id,event_id,player_id) value (1,1,7);--
insert into eventplayers (id,event_id,player_id) value (1,1,8);
insert into eventplayers (id,event_id,player_id) value (1,1,9);--
insert into eventplayers (id,event_id,player_id) value (1,1,10);
insert into eventplayers (id,event_id,player_id) value (1,1,11);
insert into eventplayers (id,event_id,player_id) value (1,1,12);
insert into eventplayers (id,event_id,player_id) value (1,1,13);
insert into eventplayers (id,event_id,player_id) value (1,1,14);
insert into eventplayers (id,event_id,player_id) value (1,1,15);
insert into eventplayers (id,event_id,player_id) value (1,1,16);

-- eventgamemapper table
insert into eventgamemapper (event_id,game_id) values (1,1);

-- eventgamerounds table 
insert into eventgamerounds (event_id,round_id) values (1,1);

-- eventmatches table
insert into eventmatches (event_id,player1_id,player2_id) values (1,1,3);
insert into eventmatches (event_id,player1_id,player2_id) values (1,5,7);
insert into eventmatches (event_id,player1_id,player2_id) values (1,9,11);
insert into eventmatches (event_id,player1_id,player2_id) values (1,13,15);
insert into eventmatches (event_id,player1_id,player2_id) values (1,2,4);
insert into eventmatches (event_id,player1_id,player2_id) values (1,6,8);
insert into eventmatches (event_id,player1_id,player2_id) values (1,10,12);
insert into eventmatches (event_id,player1_id,player2_id) values (1,14,16);
