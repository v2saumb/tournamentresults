## Introduction
A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament. 
This project teach us how to create and use databases through the use of database schemas and how to manipulate the data inside the database. This project has two parts: defining the database schema (SQL table definitions), and writing code that will use it to track a Swiss tournament.

## tournament.py

### connect()
Connect to the PostgreSQL database.  Returns a database connection.


### deleteMatches(matchid)
Remove all the match records from the database.

-	Arguments
      -	matchid: The match id for which all the matches have to be deleted.


### deletePlayers(playername)

Remove all the player records from the database.

-	Arguments
      -	playername: the player's full name (need not be unique).


### deleteUniquePlayer(name)

    Deletes all players with a unique name.

-	Arguments
     -	name: the player that has to be deleted.


### deleteNonUniquePlayers(name):

    If there are more than one players with the same name
    this function shows the user a list of players to choose from
    The user can choose "ALL" to delete all the players with a name
    The user can also choose 0 to skip Deletion.
    The user can select an ID to delete on of the players form the list

-	Arguments
     -	name: the player that has to be deleted.

### processDeletion(msgStr, valid_ids, name)

This is called from deleteNonUniquePlayers function. If there are more than one players with the same name this function shows the user a list of players to choose from the user can choose "ALL" to delete all the players with a name The user can also choose 0 to skip Deletion. The user can select an ID to delete on of the players form the list

-	Arguments
     -	msgStr: the Message that needs to be displayed
     -	valid_ids: a list of valid ids that the user can choose from
     -	name: the player that has to be deleted.


### deletePlayersByID(id)

Deletes one single player from the players table based on the player_id

-	Arguments
    -	id: the player id that needs to be deleted


### countRegisteredPlayers()

Returns the number of players currently registered.



### countEventPlayers(eventid)
Returns the number of players currently registered for a particular event.
-	Arguments
    -	eventid: the event for which the count of players is required


### registerPlayer(name, email)

Adds a player to the tournament database. The database will generate a unique id for the player. The database is designed to handle multiple events.

-	Arguments
      -	name: the player's full name (need not be unique).
      -	email: the email address of the player.

-	Returns 
	This method return the id of the newly registered player.


### playerStandings()
Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
	


### reportMatch(winner, loser)
Records the outcome of a single match between two players.

-	Arguments
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
	


### swissPairings()
Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
	


### createevent(eventName, rounds=1, games=1)
Create a new event and return the event ID for it
-	Arguments
    -	eventName: the name of the new event
    -	rounds: the number of rounds that can be played per event default is 1
    -	games: The number of games allowed per round


### creategamesperround(eventId, games, DB)
Inserts game mapping records for eventfulness
-	Arguments
    -	eventId: the event for which the games have to be mapped
    -	games: the number of games that need to be added
    -	DB: the database connection



### createroundsperevent(eventId, games, DB)
Inserts game mapping records for eventfulness
-	Arguments
    -	eventId: the event for which the games have to be mapped
    -	rounds: the number of rounds that need to be added for the event
    -	DB: the database connection


### mapPlayersAndEvent(eventId, playerId)
Inserts a mapping record for the registered players to an event. `eventplayers` table contains the information about which registered player has signed up for a particular event

-	Arguments
    -	eventId: the event in question
    -	playerId: the id of the Player to be mapped to this event
