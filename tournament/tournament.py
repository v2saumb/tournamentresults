#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches(matchid):
    """Remove all the match records from the database.
      Args:
      matchid: The match id for which all the matches have to be deleted.
    """


def deletePlayers(playername):
    """Remove all the player records from the database.
      Args:
      playername: the player's full name (need not be unique).

    """
    DB = connect()
    player_cursor = DB.cursor()
    name = bleach.clean(playername)
    query = """select count(player_id) as count from players
    where player_name = %s;"""
    player_cursor.execute(query, (name,))
    count = player_cursor.fetchone()[0]
    DB.close()

    if count < 1:
        print "No player found with name " + name + " !"
    elif count > 1:
        deleteNonUniquePlayers(name)
    else:
        deleteUniquePlayer(name)


def deleteUniquePlayer(name):
    """
    deletes all players with a unique name.
    Arg:
     name: the player that has to be deleted.
    """
    DB = connect()
    player_cursor = DB.cursor()
    print "Deleting Player " + name + " ... \n"
    player_cursor.execute("""delete from players
        where player_name = %s""", (name,))
    DB.commit()
    DB.close()


def deleteNonUniquePlayers(name):
    """
    If there are more than one players with the same name
    this function shows the user a list of players to choose from
    The user can choose "ALL" to delete all the players with a name
    The user can also choose 0 to skip Deletion.
    The user can select an ID to delete on of the players form the list
    Arg:
     name: the player that has to be deleted.
    """
    DB = connect()
    player_cursor = DB.cursor()
    query = """select player_id,player_name , player_email
        from players where player_name = %s;"""
    player_cursor.execute(query, (name,))
    rows = player_cursor.fetchall()
    print "Multiple user with name " + name
    msgstr = "ID\tName\tE-mail\n"
    valid_ids = []
    for row in rows:
        msgstr += str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2])
        msgstr += "\n"
        valid_ids.insert(0, str(row[0]))
    DB.close()
    processDeletion(msgstr, valid_ids, name)


def processDeletion(msgStr, valid_ids, name):
    """
    this is called from deleteNonUniquePlayers function
    If there are more than one players with the same name
    this function shows the user a list of players to choose from
    The user can choose "ALL" to delete all the players with a name
    The user can also choose 0 to skip Deletion.
    The user can select an ID to delete on of the players form the list
    Args:
     msgStr: the Message that needs to be displayed
     valid_ids: a list of valid ids that the user can choose from
     name: the player that has to be deleted.
    """
    print msgStr
    player_id = raw_input("""Please enter an ID from above list
    Enter 0 (zero) to skip
    Enter ALL to delete all users in above list: """)
    player_id = bleach.clean(player_id)
    if player_id == "ALL":
        deleteUniquePlayer(name)
    elif player_id == "0":
        print "Skpping..."
    elif player_id in valid_ids:
        deletePlayersByID(player_id)
    else:
        print "Invalid selection please try again!\n"
        processDeletion(msgStr, valid_ids, name)


def deletePlayersByID(id):
    """
    Deletes one single player from the players table
    based on the player_id

    Args:
    id: the player id that needs to be deleted
    """
    DB = connect()
    player_cursor = DB.cursor()
    print "Deleting Player " + id + " ... \n"
    player_cursor.execute("""delete from players
        where player_id = %s""", (id,))
    DB.commit()
    DB.close()


def countRegisteredPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    player_cursor = DB.cursor()
    query = "select count(player_id) as count from players;"
    player_cursor.execute(query)
    count = player_cursor.fetchone()[0]
    DB.close()
    return count


def countEventPlayers(eventid):
    """Returns the number of players currently registered for a
    particular event.
    Args:
    eventid: the event for which the count of players is required
    """
    DB = connect()
    player_cursor = DB.cursor()
    eventid = bleach.clean(eventid)
    query = """select count(event_id) as count from eventplayers
    where event_id = %s;"""
    player_cursor.execute(query, (eventid,))
    count = player_cursor.fetchone()[0]
    DB.close()
    return count


def registerPlayer(name, email):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
      email: the email address of the player.
    """
    DB = connect()
    player_cursor = DB.cursor()
    name = bleach.clean(name)
    email = bleach.clean(email)
    player_cursor.execute("""insert into players (player_name,player_email)
        values (%s, %s);""", (name, email))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

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
    """


def createevent(eventName, rounds=1, games=1):
    """
    Create a new event and return the event ID for it
    Args:
    eventName: the name of the new event
    """
    DB = connect()
    event_cursor = DB.cursor()
    eventName = bleach.clean(eventName)
    event_cursor.execute("""insert into events (name)
        values (%s) RETURNING ID;""", (eventName,))
    event_id = event_cursor.fetchone()[0]
    createroundsperevent(event_id, rounds, DB)
    creategamesperround(event_id, games, DB)

    DB.commit()
    DB.close()
    return event_id


def creategamesperround(eventId, games, DB):
    """
    inserts game mapping records for eventfulness
    Args:
    eventId: the event for which the games have to be mapped
    games: the number of games that need to be added
    DB: the database connection
    """
    counter = 0
    event_cursor = DB.cursor()
    while counter < games:
        counter += 1
        event_cursor.execute("""insert into eventgamemapper
            (event_id,game_number) values (%s,%s);""", (eventId, counter))


def createroundsperevent(eventId, games, DB):
    """
    inserts game mapping records for eventfulness
    Args:
    eventId: the event for which the games have to be mapped
    rounds: the number of rounds that need to be added for the event
    DB: the database connection
    """
    counter = 0
    event_cursor = DB.cursor()
    while counter < games:
        counter += 1
        event_cursor.execute("""insert into eventgamerounds
            (event_id,round_number) values (%s,%s);""", (eventId, counter))


def mapPlayersAndEvent(eventId, playerId):
    """
    inserts a mapping record for the registered players to an event
    Args:
    eventId: the event in question
    playerId: the id of the Player to be mapped to this event
    """
    DB = connect()
    event_cursor = DB.cursor()
    event_cursor.execute("""insert into eventplayers (event_id,player_id)
        values (%s,%s) RETURNING ID;""", (eventId, playerId))
    eventPlayerId = event_cursor.fetchone()[0]
    DB.commit()
    DB.close()
    return eventPlayerId

event_id = createevent("Test id ", 1, 1)
mapPlayersAndEvent(event_id, 1)
mapPlayersAndEvent(event_id, 2)
mapPlayersAndEvent(event_id, 3)
mapPlayersAndEvent(event_id, 4)
print countEventPlayers(event_id)
