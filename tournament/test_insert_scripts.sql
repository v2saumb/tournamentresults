-- tournament test  insert scripts 
-- contains insert scripts for testing 

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

insert into players (player_name,player_email) values ('player 17', 'player17@email.com');		

-- events table
insert into events (id,name) values(1, 'Chess Championship 2015');
insert into events (id,name) values(2, 'Reading Swimming Meet 2015');

-- eventgamemapper table
insert into eventgamemapper (event_id,game_number) values (1,1);

insert into eventgamemapper (event_id,game_number) values (2,1);	

-- eventgamerounds table 
insert into eventgamerounds (event_id,round_number) values (1,1);
insert into eventgamerounds (event_id,round_number) values (1,2);

insert into eventgamerounds (event_id,round_number) values (2,1);

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


-- event number 2
insert into eventplayers (id,event_id,player_id) values (17,2,1);
insert into eventplayers (id,event_id,player_id) values (18,2,2);
insert into eventplayers (id,event_id,player_id) values (19,2,3);
insert into eventplayers (id,event_id,player_id) values (20,2,4);
insert into eventplayers (id,event_id,player_id) values (21,2,5);
insert into eventplayers (id,event_id,player_id) values (22,2,6);
insert into eventplayers (id,event_id,player_id) values (23,2,7);
insert into eventplayers (id,event_id,player_id) values (24,2,8);

--insert into eventplayers (id,event_id,player_id) values (17,1,17);	



-- eventmatches table assuming matches have been played event 1
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,1,1,3,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,2,5,7,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,3,9,11,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,4,13,15,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,5,2,4,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,6,6,8,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,7,10,12,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,8,14,16,TRUE);

insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,9,1,5,TRUE);	
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,10,9,13,TRUE);	
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,11,2,6,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,12,10,14,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,13,3,7,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,14,11,15,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,15,4,8,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (1,16,12,16,TRUE);

--	event 2 event matches
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (2,17,1,2,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (2,18,3,4,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (2,19,5,6,TRUE);
insert into eventmatches (event_id,match_id,player1_id,player2_id,played) values (2,20,7,8,TRUE);


-- player score assuming the first player won.
--round 1 score
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,1,1,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,1,3,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,2,5,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,2,7,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,3,9,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,3,11,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,4,13,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,4,15,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,5,2,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,5,4,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,6,6,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,6,8,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,7,10,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,7,12,1,1,2,0,0);		

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,8,14,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,8,16,1,1,2,0,0);

-- round 2 scores
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,9,5,1,2,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,9,1,1,2,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,10,9,1,2,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,10,13,1,2,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,11,6,1,2,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,11,2,1,2,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,12,14,1,2,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,12,10,1,2,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,13,3,1,2,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,13,7,1,2,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,14,11,1,2,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,14,15,1,2,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,15,4,1,2,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,15,8,1,2,2,0,0);		

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,16,16,1,2,2,0,0);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (1,16,12,1,2,1,3,3);

-- event 2 round 1 score
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,17,17,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,17,18,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,18,19,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,18,20,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,19,21,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,19,22,1,1,2,0,0);

insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,20,23,1,1,1,3,3);
insert into playerscore (event_id,match_id, player_id, game_number,
	round_number, match_result, game_score,match_score) values (2,20,24,1,1,2,0,0);
