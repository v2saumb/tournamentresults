## Introduction
A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament. 
This project teach us how to create and use databases through the use of database schemas and how to manipulate the data inside the database. This project has two parts: defining the database schema (SQL table definitions), and writing code that will use it to track a Swiss tournament.

## tournament.py



### connect()
Connect to the PostgreSQL database.  Returns a database connection.

* Returns:
    Returns a database connection.

---


### deleteMatches(eventId, matchId)
    
Remove all the match records from the database.
  
* Arguments
    * eventId: The event id for which the matches have to be deleted.
    * matchId: The match id for which all the matches have to be deleted.
    
---    

### deletePlayers(playername)

Remove all the player records from the database.

* Arguments
    * playername: the player's full name (need not be unique).

---

### deleteUniquePlayer(name)
    
Deletes all players with a unique name.

* Arguments
    * name: the player that has to be deleted.

* Returns
    * then number of records deleted

---

### deleteNonUniquePlayers(name)

If there are more than one players with the same name this function shows the user a list of players to choose from. The user can choose "ALL" to delete all the players with a name. The user can also choose 0 to skip Deletion. The user can select an ID to delete on of the players form the list

* Arguments
    * name: the player that has to be deleted.

---


### processDeletion(msgStr, valid_ids, name)

This is called from deleteNonUniquePlayers function. If there are more than one players with the same name,this function shows the user a list of players to choose from the user can choose "ALL" to delete all the players with a name. The user can also choose 0 to skip Deletion. The user can select an ID to delete on of the players form the list

* Arguments
    * msgStr: the Message that needs to be displayed
    * valid_ids: a list of valid ids that the user can choose from
    * name: the player that has to be deleted.
    
---

### deletePlayersByID(id)
    
Deletes one single player from the players table based on the player_id

* Arguments
    * id: the player id that needs to be deleted

* Returns
    * Number of records deleted    

---

### countRegisteredPlayers()

* Returns
    * The number of players currently registered. All players of all events are included in the count.

---

### countEventPlayers(eventid)

* Arguments
    * eventid: the event for which the count of players is required.

* Returns
    * The number of players currently registered for a particular event.

---


### registerPlayer(name, email)

Adds a player to the tournament database.The database assigns a unique serial id number for the player.  (This is handled by your SQL database schema, not in Python code.)

* Arguments
    * name: the player's full name (need not be unique).
    * email: the email address of the player.

---
 
### playerStandings(eventId)

Returns a list of the players and their win records, sorted by wins. The first entry in the list should be the player in first place for the event, or the player tied for first place if there is currently a tie. The results are returned sorted in the order that the winner is always on the top.
    
* Arguments
    * eventId: The id for the event for which the player standings are required.

* Returns
  A list of tuples, each of which containsthe following:
    * event_id:The event id for the event for which the standings are retested.
    * playerid:the player's id assigned for the event (assigned by the database).
    * player_name: the player's full name (as registered).
    * gamepoints: the total of game points.
    * matchpoints: the total of match points.
    * totalpoints: the total score for the player.
    * matchesplayed:the number of matches the player has played.
    * won: the number of matches the player has won.
    * lost:the number of matches the player has lost.
    * draw:the number of matches the player that were draw.
    * bye:the number of matches the player has a bye win.

---

### reportMatch(eventId, matchId, roundNumber, gameNumber, winnerId, loserId=None, isDraw=False, isBye=False)

Records the outcome of a single match between two players. An entry for the match should exist in the event matches table. If there are more than one rounds for games between the same players per match, multiple entries are allowed. The games and rounds should be mapped in the eventgamemapper and eventgamerounds.Scoring is based on http://www.wizards.com/dci/downloads/swiss_pairings.pdf.

Games and matches are worth the following points during Swiss rounds:

* Game won 3 points
* Game drawn 1 point
* Game lost 0 points
* Unfinished Game 1 point same as draw
* Not played Game 0 points


Records are saved in the database with following status
* 1 - 'WON'
* 2 - 'LOST'
* 3 - 'DRAW'
* 4 - 'BYEWIN'


* Arguments
    * eventId: the event id.
    * matchId: the match Id.
    * roundNumber: the round number what is played.
    * gameNumber: The game number for the round for which the score is recorded.
    * winnerId: the playerID from the eventmatches table.
    * loserId the playerId from the eventmatches table for the losing player.
    * isDraw: true or false depending on if this was a draw or not.
    * isBye: true or false depending on if ths was a bye win. remember only one bye is allowed per event for a player.
    
---


### calculatePlayerMatchScore(eventId, gameNumber, winnerId, loserId=None, isDraw=False, isBye=False)

Calculate the match score for players for a match

* Arguments
    * gameNumber: the gamenumber for which the scoring is done
    * eventId: the event id
    * matchId: the match Id
    * winnerId: the playerID from the eventmatches table. if it is a bye sent
    * the player recieving a bye as winner
    * loserId the playerId from the eventmatches table for the losing player.
    * isDraw: true or false depending on if this was a draw or not. this should be null in case of a bye
    * isBye: true or false depending on if this was a bye win. remember only one bye is allowed per event for a player.
    
* Returns
The score for both the players.
    * score = {"winnerScore": 0, "loserScore": 0} if this is not the last game for the match. or match lost.
    * score = {"winnerScore": 3, "loserScore": 0} if the winner of the game is also the winner of the match.
    * score = {"winnerScore": 0, "loserScore": 3} if the loser of this game won the match.
    * score = {"winnerScore": 1, "loserScore": 1} if the match is a draw.
    * score = {"winnerScore": 3, "loserScore": 0} if this is a bye win.

---
   
### getIndividualPlayerStanding(eventId, playerId)

Get the player standing for a single player

* Arguments
    * playerId:   the Id of the player for whom the score is required.
    * eventId:    the event for which scoring is done

* Returns: A row with player standing for a single player for a event.
    * event_id:The event id for the event for which the standings are retested.
    * playerid:the player's id assigned for the event (assigned by the database).
    * player_name: the player's full name (as registered).
    * gamepoints: the total of game points.
    * matchpoints: the total of match points.
    * totalpoints: the total score for the player.
    * matchesplayed:the number of matches the player has played.
    * won: the number of matches the player has won.
    * lost:the number of matches the player has lost.
    * draw:the number of matches the player that were draw.
    * bye:the number of matches the player has a bye win.

---

### getMaxGameNumber(eventId)

 Returns the max number of games allowed per match 

* Arguments
    * eventId: the event's id for which information is required.
* Returns
    * Number of games that can be played per round for a match.

---

### insertPlayerScore(eventId, matchId, playerId, gameNumber, roundNumber, matchResult, gameScore, matchScore)

This function is used to insert the record for a players match / game result.

* Arguments
    * eventId: the event id 
    * matchId: the match Id
    * playerId: the Id for the player from the eventplayers table
    * roundNumber: the round number what is played
    * gameNumber: The game number for the round for which the score is recorded
    * matchResult: The result for the player won lost draw or bye 
    * gameScore: points for the game 
    * matchScore: points for the match
    
---    

### createevent(eventName, rounds=1, games=1)
    
Create a new event and return the event ID for it

* Arguments
    * eventName: the name of the new event
    * rounds: the number of rounds allowed per match. Default is 1.
    * games: The number of games allowed per round. Default is 1.

* Returns 
    * The event Id for the event just created.
    

---

### creategamesperround(eventId, games, DB)
    
Inserts game mapping records for an event

* Arguments
    * eventId: the event for which the games have to be mapped
    * games: the number of games that need to be added
    * DB: the database connection
 
---

### createroundsperevent(eventId, games, DB)
    
Inserts game mapping records for an event

* Arguments
    * eventId: the event for which the games have to be mapped
    * rounds: the number of rounds that need to be added for the event
    * DB: the database connection

---

### mapPlayersAndEvent(eventId, playerId)
    
Inserts a mapping record for the registered players to an event

* Arguments
    * eventId: the event in question
    * playerId: the id of the Player to be mapped to this event
    
---

### printPlayerScores(eventId)
    
prints the current player standings for an event on screen

---

### updateMatchPlayedStatus(matchId)

Updates the match played record.

* Arguments
    * matchId: the match in question for which the record is to be updated.
    * DB: The database connection

* Returns
    * Returns the number of records updated.

---

### countEventMatches(eventId):
    
Counts the number of matches for an event.

*   Arguments 
        *   eventId: The event Id for which the count is required.

*   Returns
        * Returns the count of matches already registered.

   
---

### countEventMatchesPlayed(eventId):
   
Counts the number of matches already played for an event.

*   Arguments 
        *   eventId: The event Id for which the count is required.

*   Returns
        * Returns the count of matches already registered and played.

   
---


### countGamesPerRound(eventId):

Counts the number of games played per round for an event.

*   Arguments 
        *   eventId: The event Id for which the count is required.

*   Returns
        * Returns the count of games played per round for an event.

   
---


### countRoundPerEvent(eventId):
   
Counts the number of rounds played per  event.

*   Arguments 
        *   eventId: The event Id for which the count is required.

*   Returns
        * Returns the count of rounds played per event.

   
---

### swissPairings() WORK IN PROGRESS


---