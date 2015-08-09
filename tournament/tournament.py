#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import random
import sys


def calculatePlayerMatchScore(eventId, gameNumber, winnerId, loserId=None,
                              isDraw=False, isBye=False):
    """
    Calculates the match score for a player;

        *   Arguments:
                *   gameNumber: the gamenumber for which the scoring is done
                *   eventId: the event id
                *   matchId: the match Id
                *   winnerId: the playerID from the eventmatches table. if it
                    is a bye sent the player recieving a bye as winner
                *   loserId the playerId from the eventmatches table for the
                    losing player.
                *   isDraw: true or false depending on if this was a draw
                    or not. this
                    should be null in case of a bye
                *   isBye: true or false depending on if ths was a bye win.
                    remember only one bye is allowed per event for a player.
        *   Returns:
                *   score = {"winnerScore": <score>, "loserScore": <score>}
                    Based on the following rule.
                        *   0 (zero) if this is not the last game for the match
                            or match lost
                        *   3 if matches won
                        *   1 if the match was a draw.
                        *   Match won 3 points
                        *   Match drawn 1 point
                        *   Match lost 0 points
    """

    score = {"winnerScore": 0, "loserScore": 0}
    totalWonP2 = 0
    totalWon = 0
    games = getMaxGameNumber(eventId)

    if games == gameNumber:
        currentStandngWinner = getIndividualPlayerStanding(
            eventId, winnerId)
        if loserId is not None:
            currentStandingLoser = getIndividualPlayerStanding(
                eventId, loserId)
            # matchesPlayedP2 = currentStandingLoser['matchesplayed']
            wonP2 = currentStandingLoser['won']
            # lostP2 = currentStandingLoser['lost']
            drawP2 = currentStandingLoser['draws']
            byeP2 = currentStandingLoser['bye']
            totalWonP2 = wonP2 + drawP2 + byeP2

        # matchesPlayed = currentStandngWinner['matchesplayed']
        won = currentStandngWinner['won']
        # lost = currentStandngWinner['lost']
        draw = currentStandngWinner['draws']
        bye = currentStandngWinner['bye']
        totalWon = won + draw + bye

        if isBye is True:
            totalWon = totalWon + 1

        if isDraw is True:
            totalWon = totalWon + 1
            totalWonP2 = totalWonP2 + 1

        if isBye is True:
            score = {"winnerScore": 3, "loserScore": 0}
        elif totalWon == totalWonP2:
            score = {"winnerScore": 1, "loserScore": 1}
        elif totalWon > totalWonP2:
            score = {"winnerScore": 3, "loserScore": 0}
        elif totalWonP2 > totalWon:
            score = {"winnerScore": 0, "loserScore": 3}
        else:
            score = score = {"winnerScore": 0, "loserScore": 0}
    else:
        score = score = {"winnerScore": 0, "loserScore": 0}
    return score


def connect():
    """
    Connect to the PostgreSQL database.

    *   Returns
            *   returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def countRegisteredPlayers():
    """Returns the number of players currently registered.

        *   Returns:
                *   The count of number of players currently registered.
                This is the total number of players registered in the system.
    """
    try:
        DB = connect()
        player_cursor = DB.cursor()
        query = """select count(player_id) as count from players
         where player_id>0;"""
        player_cursor.execute(query)
        count = player_cursor.fetchone()[0]
        DB.close()
        return count
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error counting registered
             players [countRegisteredPlayers]!""")


def countEventPlayers(eventid):
    """
    Returns the number of players currently registered for a
    particular event.

    *   Arguments:
            *   eventid: the event for which the count of players is required

      *   Returns:
                *   The count of number of players currently registered
                for an event.
    """
    try:
        DB = connect()
        player_cursor = DB.cursor()
        eventid = bleach.clean(eventid)
        query = """select * from playercount(%s);"""
        player_cursor.execute(query, (eventid,))
        count = player_cursor.fetchone()[0]
        DB.close()
        return count
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error counting
            players [countEventPlayers] !""")


def countEventMatches(eventId):
    """
        Counts the number of matches for an event.

        *   Arguments
                *   eventId: The event Id for which the count is required.

        *   Returns
                * Returns the count of matches already registered.

    """
    try:
        DB = connect()
        match_cursor = DB.cursor()
        query = "select * from getMatchCount(%s);"
        match_cursor.execute(query, (eventId,))
        count = match_cursor.fetchone()[0]
        DB.close()
        return count
    except:
        printErrorDetails(
            sys.exc_info(), "There was an error getting current match count!")


def countEventMatchesPlayed(eventId):
    """
        Counts the number of matches already played for an event.

        *   Arguments
                *   eventId: The event Id for which the count is required.

        *   Returns
                * Returns the count of matches already registered and played.

    """
    try:
        DB = connect()
        match_cursor = DB.cursor()
        query = "select * from getMatchesPlayedCount(%s);"
        match_cursor.execute(query, (eventId,))
        count = match_cursor.fetchone()[0]
        DB.close()
        return count
    except:
        printErrorDetails(
            sys.exc_info(), "There was an error getting matches played count!")


def countGamesPerRound(eventId):
    """
        Counts the number of games played per round for an event.

        *   Arguments
                *   eventId: The event Id for which the count is required.

        *   Returns
                * Returns the count of games played per round for an event.

    """
    try:

        DB = connect()
        match_cursor = DB.cursor()
        query = "select * from getTotalGamesCount(%s);"
        match_cursor.execute(query, (eventId,))
        count = match_cursor.fetchone()[0]
        DB.close()
        return count
    except:
        printErrorDetails(
            sys.exc_info(), "There was an error getting game count!")


def countRoundPerEvent(eventId):
    """
        Counts the number of rounds played per  event.

        *   Arguments
                *   eventId: The event Id for which the count is required.

        *   Returns
                * Returns the count of rounds played per event.

    """
    try:
        DB = connect()
        match_cursor = DB.cursor()
        query = "select * from getTotalRoundsCount(%s);"
        match_cursor.execute(query, (eventId,))
        count = match_cursor.fetchone()[0]
        DB.close()
        return count
    except:
        printErrorDetails(
            sys.exc_info(), "There was an error getting round count!")


def createevent(eventName, rounds=1, games=1):
    """
    Create a new event and return the event ID for it
        *   Arguments:
                *   eventName: the name of the new event
    """
    try:
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
        # map the dummy player this will be used for
        # reporting bye.
        mapPlayersAndEvent(event_id, 0)
        return event_id
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error counting
            players [createevent] !""")
        DB.rollback()
        DB.close()


def creategamesperround(eventId, games, DB):
    """
    Inserts game mapping records for eventfulness

        *   Arguments:
                *   eventId: the event for which the games have to be mapped
                *   games: the number of games that need to be added
                *   DB: the database connection
    """
    try:
        counter = 0
        event_cursor = DB.cursor()
        while counter < games:
            counter += 1
            event_cursor.execute("""insert into eventgamemapper
                (event_id,game_number) values (%s,%s);""", (eventId, counter))
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error creating game
             record [creategamesperround] !""")
        DB.rollback()


def createParingGroups(currentStandings):
    """
       Breaks the standings in smaller groups based on points
       *   Arguments
            *   currentStandings : the events current standings.
    """
    tempStandings = []
    tempScore = -1
    indx = 0
    newArrry = []
    while indx < len(currentStandings):
        if currentStandings[indx]['totalpoints'] != tempScore:
            tempScore = currentStandings[indx]['totalpoints']
            if len(newArrry) > 0:
                print '--pushing new group'
                tempStandings.insert(0, newArrry)
                newArrry = []

        newArrry.insert(0, currentStandings[indx])
        indx += 1
    tempStandings.insert(0, newArrry)
    return tempStandings


def createParings(currentStandings, eventId):
    """
    Creates the parings for the event.

    *   Arguments
            *   currentStandings : the events current standings.
            *   eventId:    The event Id that will be passed to the DB function

    """
    rowCounter = 1
    matchDetails = {'Player1': None, 'Player2': None}
    groups = createParingGroups(currentStandings)
    currentPairings = getCurrentParings(eventId)
    newParing = []
    oddManOut = None
    for group in groups:
        if oddManOut is not None:
            group.insert(0, oddManOut)
            oddManOut = None

        group = randomizeGroup(group)
        rowCounter = 1
        grplen = len(group)

        if (grplen % 2) == 0:
            isGroupOdd = False
        else:
            isGroupOdd = True

        if isGroupOdd is True:
            oddManOut = group.pop(0)
            print "Group is odd popping item ", oddManOut

        for pstand in group:
            if rowCounter % 2 == 0:
                fieldName = 'Player2'
            else:
                fieldName = 'Player1'

            matchDetails[fieldName] = pstand

            if (rowCounter % 2) == 0:
                newParing.insert(0, matchDetails)
                matchDetails = {'Player1': None, 'Player2': None}
            rowCounter += 1

    if oddManOut is not None:
        print "Reporting a bye for popped Item"
        createByeRecord(oddManOut, eventId)

    if verifyPairs(currentPairings, newParing) is True:
        return newParing
    else:
        return createParings(currentStandings, eventId)


def createByeRecord(byePlayer, eventId):
    """
    Processes the bye record. This function will created a bye match and
     then report the score for it

     *  Arguments:
        *  byePlayer : the player receiving bye

    """
    try:
        DB = connect()
        oddPair = {
            'Player1': {'playerId': byePlayer['playerId']},
            'Player2': {'playerId': getDummyUserId(eventId)}}

        print "found dummy  ", oddPair
        matchId = insertMatchRecord(eventId, oddPair, DB)
        DB.commit()
        DB.close()
        # reportMatch(eventId, matchId, roundNumber, gameNumber, winnerId,
        # loserId=None, isDraw=False, isBye=False):
        reportMatch(
            eventId, matchId, 1, 1, byePlayer['playerId'], None, False, True)
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error creating rounds
             record [createByeRecord] !""")
        DB.rollback()
        DB.close()


def createroundsperevent(eventId, games, DB):
    """
    Inserts game mapping records for eventfulness

        *   Arguments:
                *   eventId: the event for which the games have to be mapped
                *   rounds: the number of rounds that need to be added for the
                     event
                *   DB: the database connection
    """
    try:
        counter = 0
        event_cursor = DB.cursor()
        while counter < games:
            counter += 1
            event_cursor.execute("""insert into eventgamerounds
                (event_id,round_number) values (%s,%s);""", (eventId, counter))
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error creating rounds
             record [createroundsperevent] !""")
        DB.rollback()


def deleteEvent(eventId):
    """
      Deletes the event and all related records.
      * Arguments:
          * eventId: The event id for which the matches have to be deleted.
      * Returns:
            *   Returns the number of records deleted.
    """
    try:
        print "Deleting event " + str(eventId)
        DB = connect()
        match_cur = DB.cursor()
        query = "delete from events where id = %s"
        match_cur.execute(query, (eventId, ))
        rowcount = match_cur.rowcount
        DB.commit()
        DB.close()
        print str(rowcount) + " deleted."
        return rowcount
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error deleting matches
             for the event!""")
        DB.rollback()
        DB.close()


def deleteMatches(eventId, matchId=None):
    """
      Remove all the match records from the database. if a matchId is passed
      only that specific match record will be deleted.
      when the match record is deleted the scores are
      also deleted automatically

      * Arguments:
          * eventId: The event id for which the matches have to be deleted.
          * matchId: if match id is passed only this match record is deleted.

      * Returns:
            *   Returns the number of records deleted.
    """
    try:
        DB = connect()
        match_cur = DB.cursor()
        query = "delete from eventmatches where event_id = %s"
        if matchId is not None:
            query += " and match_id=%s"

        print "Deleting Match(s) ", eventId, matchId
        if matchId is not None:
            match_cur.execute(query, (eventId, matchId))
        else:
            match_cur.execute(query, (eventId, ))

        rowcount = match_cur.rowcount
        DB.commit()
        DB.close()
        print str(rowcount) + " deleted."
        return rowcount
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error deleting matches
             for the event!""")
        DB.rollback()
        DB.close()


def deleteNonUniquePlayers(name):
    """
    If there are more than one players with the same name
    this function shows the user a list of players to choose from
    The user can choose "ALL" to delete all the players with a name
    The user can also choose 0 to skip Deletion.
    The user can select an ID to delete on of the players form the list

    *   Arguments:
            *  name: the player that has to be deleted.

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


def deleteAllPlayers():
    """
    This function deletes all the registered players from the
    system.
    """
    try:
        DB = connect()
        player_cursor = DB.cursor()
        print "Deleting All Player "
        player_cursor.execute("""delete from players where player_id >0""")
        rowcount = player_cursor.rowcount
        DB.commit()
        DB.close()
        print rowcount, " deleted."
        return rowcount
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error deleting
            player [deletePlayersByID]!""")
        DB.rollback()
        DB.close()


def deletePlayers(playername):
    """
    Remove the player records from the database with a name.

    *   Arguments:
            *   playername: the player's full name (need not be unique).

    """
    try:
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
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error deleting player!""")
        DB.rollback()
        DB.close()


def deletePlayersByID(playerId):
    """
    Deletes one single player from the players table
    based on the player_playerId

    *   Arguments:
            *   playerId: the players Id that needs to be deleted

    *   Returns:
            *   the number of records deleted
    """
    try:
        DB = connect()
        player_cursor = DB.cursor()
        if playerId == 0:
            print "Cannot delete dummy user!"
            return
        print "Deleting Player " + playerId + " ... \n"
        player_cursor.execute("""delete from players
            where player_id = %s""", (playerId,))
        rowcount = player_cursor.rowcount
        DB.commit()
        DB.close()
        print rowcount, " deleted."
        return rowcount
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error deleting
            player [deletePlayersByID]!""")
        DB.rollback()
        DB.close()


def deleteUniquePlayer(name):
    """
    Deletes all players with a unique name.

    *   Arguments:
            *   name: the player that has to be deleted.

    *   Returns:
            *   the number of records deleted
    """
    try:
        DB = connect()
        player_cursor = DB.cursor()
        player_cursor.execute("""delete from players
            where player_name = %s""", (name,))
        rowcount = player_cursor.rowcount
        DB.commit()
        DB.close()
        return rowcount
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error deleting player
            [deleteUniquePlayer]!""")
        DB.rollback()
        DB.close()


def getCurrentParings(eventId):
    """
    gets the list of current mappings
    *   Argument
            *   eventId: the event Id for which the records are being inserted.

    *   Returns
            *   returns a list of current mappings
    """
    try:

        DB = connect()
        score_cursor = DB.cursor()
        eventId = bleach.clean(eventId)
        score_cursor.execute("""select * from eventmatches where
            event_id = %s and played=true;""", (eventId,))
        rows = score_cursor.fetchall()
        currentMatches = [{
            'event_id': int(row[0]),
            'matchId': int(row[1]),
            'player1_id': int(row[2]),
            'player2_id': int(row[3]),
            'played': int(row[4])} for row in rows]
        DB.close()
        return currentMatches
    except:
        printErrorDetails(
            sys.exc_info(), "There was an error getting current match Pairs!")
        DB.close()


def getDummyUserId(eventId):
    """
    finds and returns the eventPlayerID for the dummy user

    *  Arguments:
        *  eventId : the eventId

    * returns the Dummy users player Id

    """
    try:
        player_id = None
        DB = connect()
        player_cursor = DB.cursor()
        query = """select id  from eventplayers where
         player_id=0 and event_id=%s;"""
        player_cursor.execute(query, (eventId,))
        player_id = player_cursor.fetchone()[0]
        print "found dummy  ", player_id
        DB.commit()
        DB.close()
        return player_id
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error [getDummyUserId] !""")
        DB.rollback()


def getIndividualPlayerStanding(eventId, playerId):
    """
    get the player standing for a single player
      Arguments:
        playerId:   the Id of the player for whom the score is required.
        eventId:    the event for which scoring is done;
      Returns: a row with player standing
    """
    rows = playerStandings(eventId)
    for pStand in rows:
        if pStand['playerId'] == playerId:
            result = pStand
    return result


def getMaxGameNumber(eventId):
    """ returns the max number of games allowed per match
    Arguments :
        eventId: the event's id for which information is required.
    Returns:
        number of games played per round.
    """
    DB = connect()
    game_cursor = DB.cursor()
    eventId = bleach.clean(eventId)
    query = """select max(game_number) from eventgamemapper
     where event_id=%s;"""
    game_cursor.execute(query, (eventId,))
    games = game_cursor.fetchone()[0]
    DB.close()
    return games


def insertMatchRecord(eventId, paring, DB):
    """
    Inserts the match record in the event matches table
    *   Argument
            *   eventId: the event Id for which the records are being inserted.
            *   praring:  Paring for the current players
            *   DB: The database connection

    *   Returns
            *   returns the id for the current inserted record
    """
    try:
        matchCursor = DB.cursor()
        matchCursor.execute("""insert into eventmatches (event_id,player1_id, player2_id, played)
        values(%s, %s, %s, False) RETURNING match_id;""",
                            (eventId, paring["Player1"]["playerId"],
                             paring["Player2"]["playerId"]))
        matchId = matchCursor.fetchone()[0]
        print "-- Match record created \n -- MatchId = " + str(matchId) + \
            "\t" + str(eventId) + "\t" + str(paring["Player1"]["playerId"]) + "\t" + \
            str(paring["Player2"]["playerId"])
        return matchId
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error inserting
             match records[]insertMatchRecord]!""")
        DB.rollback()


def insertPlayerScore(eventId, matchId, playerId, gameNumber, roundNumber,
                      matchResult, gameScore, matchScore):
    """
    Inserts the score record for the player for a match

    *   Arguments:
            *   eventId: the event id
            *   matchId: the match Id
            *   playerId: the Id for the player from the eventplayers table
            *   roundNumber: the round number what is played
            *   gameNumber: The game number for the round for which the score
                is recorded
            *   matchResult: The result for the player won lost
                draw or bye
            *   gameScore: points for the game
            *   matchScore: points for the match
    """
    try:
        DB = connect()
        event_cursor = DB.cursor()
        event_cursor.execute("""insert into playerscore (event_id,match_id,
         player_id, game_number, round_number, match_result,
         game_score,match_score)
        values (%s,%s,%s,%s,%s,%s,%s,%s);""", (eventId, matchId, playerId,
                                               gameNumber, roundNumber,
                                               matchResult, gameScore,
                                               matchScore))
        DB.commit()
        DB.close()
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error saving match
                                     score [insertPlayerScore]!""")
        DB.rollback()
        DB.close()


def mapPlayersAndEvent(eventId, playerId):
    """
    Inserts a mapping record for the registered players to an event

        *   Arguments:
            *   eventId: the event in question
            *   playerId: the id of the Player to be mapped to this event
    """
    try:
        DB = connect()
        event_cursor = DB.cursor()
        print "Mapping Player", playerId, " and event ", eventId
        event_cursor.execute("""insert into eventplayers (event_id,player_id)
            values (%s,%s) RETURNING ID;""", (eventId, playerId))
        eventPlayerId = event_cursor.fetchone()[0]
        DB.commit()
        DB.close()
        print "Player Mapped."
        return eventPlayerId
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error mapping events and players
                         [mapPlayersAndEvent]!""")
        DB.rollback()
        DB.close()


def printErrorDetails(errorOccurance, messageStr=None):
    """
    Prints the error details
    *   Argument
            *   errorOccurance: Error Object.
            *   messageStr: Any specific message that has to be
                printed before the error details.
    """
    errorDetails = None
    if errorOccurance[1] is not None:
        errorDetails = errorOccurance[1]
    else:
        errorDetails = errorOccurance[1]
    if messageStr is not None:
        messageStr += "\n\t"
        print messageStr, errorDetails
    else:
        print "There was an processing your request!\n\t", errorDetails


def printPlayerScores(eventId):
    """
    prints the current player standings for an event
    """
    rows = playerStandings(eventId)
    logString = """playername \t-\t totalpoints \t-\t won \t-\t lost \t-\t
     draws \t-\t bye"""
    print logString
    for pstand in rows:
        logString = pstand['playername'] + "\t-\t" + \
            str(pstand['totalpoints']) + "\t-\t" + \
            str(pstand['won']) + "\t-\t"
        logString = logString + \
            str(pstand['lost']) + "\t-\t" + str(pstand['draws'])
        logString = logString + "\t-\t" + str(pstand['bye'])
        print logString


def processDeletion(msgStr, valid_ids, name):
    """
    This function is called from deleteNonUniquePlayers function
    If there are more than one players with the same name
    this function shows the user a list of players to choose from
    The user can choose "ALL" to delete all the players with a name
    The user can also choose 0 to skip Deletion.
    The user can select an ID to delete on of the players form the list

    *   Arguments:
            *  msgStr: the Message that needs to be displayed
            *  valid_ids: a list of valid ids that the user can choose from
            *  name: the player that has to be deleted.
    """
    try:

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
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error deleting player
            [processDeletion]!""")


def playerStandings(eventId):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place for
    the event, or the player tied for first place if there is currently a tie.
    The results are returned sorted in the following order
    totalpoints desc ,matchesplayed desc, won desc, lost desc , draw desc
    ep.event_id asc, ep.player_id asc
        *   Arguments:
                *   eventId: The id for the event for which the player
                     standings are required.
        *   Returns:
                *   A list of tuples, each of which contains the following:
                        *   event_id:The event id for the event for which the
                         standings are requested
                        *   playerid:the player's id assigned for the event
                        (assigned by the database)
                        *   player_name: the player's full name (as registered)
                        *   gamepoints: the total of gam points
                        *   matchpoints: the total of match points
                        *   totalpoints: the total score for the player
                        *   matchesplayed:the number of matches the player has
                                    played
                        *   won: the number of matches the player has won
                        *   lost:the number of matches the player has lost
                        *   draw:the number of matches the player that were
                                 draw
                        *   bye:the number of matches the player has a bye win
    """
    DB = connect()
    score_cursor = DB.cursor()
    eventId = bleach.clean(eventId)
    score_cursor.execute("""select * from player_standing where
        event_id = %s;""", (eventId,))
    rows = score_cursor.fetchall()
    standings = [{'event_id': int(row[0]), 'playerId': int(row[1]),
                  'playername': str(row[2]), 'gamepoints': int(row[3]),
                  'matchpoints': int(row[4]), 'totalpoints': int(row[5]),
                  'matchesplayed': int(row[6]), 'won': int(row[7]),
                  'lost': int(row[8]), 'draws': int(row[9]),
                  'bye': int(row[10])} for row in rows]
    DB.close()
    if len(standings) == 0:
        print "No standings available at this time!"
    return standings


def registerPlayer(name, email):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    *   Arguments:
            *   name: the player's full name (need not be unique).
            *   email: the email address of the player.
    """
    try:
        DB = connect()
        player_cursor = DB.cursor()
        name = bleach.clean(name)
        email = bleach.clean(email)
        player_cursor.execute("""insert into players (player_name,player_email)
            values (%s, %s) RETURNING player_id;;""", (name, email))
        player_id = player_cursor.fetchone()[0]
        DB.commit()
        DB.close()
        return player_id
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error registerPlayer player
             [registerPlayer]!""")
        DB.rollback()
        DB.close()


def reportMatch(eventId, matchId, roundNumber, gameNumber, winnerId,
                loserId=None, isDraw=False, isBye=False):
    """
    Records the outcome of a single match between two players.
    An entry for the match should exist in the event matches table.
    If there are more than one rounds for games between the same players
    per match, multiple entries are allowed. The games and rounds should be
    mapped in the eventgamemapper and eventgamerounds.
    Scoring is based on http://www.wizards.com/dci/downloads/swiss_pairings.pdf

        Games and matches are worth the following points during Swiss rounds:
        ------------------------------------------------
        Game won 3 points
        Game drawn 1 point
        Game lost 0 points
        Unfinished Game 1 point same as draw
        Unplayed Game 0 points
        -------------------------------------------------


        Status
        ------
        1,'WON'
        2,'LOST'
        3,'DRAW'
        4,'BYEWIN'

    *   Arguments:
            *   eventId: the event id
            *   matchId: the match Id
            *   roundNumber: the round number what is played
            *   gameNumber: The game number for the round for which the
                 score is recorded
            *   winnerId: the playerID from the eventmatches table
            *   loserId the playerId from the eventmatches table for the
                 losing player.
            *   isDraw: true or false depending on if this was a draw or not
            *   isBye: true or false depending on if ths was a bye win.
                 remember only one bye is allowed per event for a player.
    """
    try:
        DB = connect()
        if isDraw is True and isBye is True:
            print(
                """Error: Match can not be both draw
                 and bye at the same time !""")
            return None

        playerMatchScores = calculatePlayerMatchScore(
            eventId, gameNumber, winnerId, loserId, isDraw, isBye)

    # Calculate the scores
        if isDraw is True:
            insertPlayerScore(eventId, matchId, winnerId, gameNumber,
                              roundNumber, 3, 1,
                              playerMatchScores["winnerScore"])
            insertPlayerScore(eventId, matchId, loserId, gameNumber,
                              roundNumber, 3, 1,
                              playerMatchScores["loserScore"])
        elif isBye is True:
            """
            Pair players randomly for the first round by shuffling the note
            cards. Keep the paired cards together for the rest of the round.
            If you have an odd number of players, the player remaining once
            pairings are completed receives a bye, equaling two game wins
            (6 game points) and one match win (3 match points)
            """
            insertPlayerScore(
                eventId, matchId, winnerId, gameNumber, roundNumber, 4, 6, 3)
        else:
            #   insert winner score
            insertPlayerScore(eventId, matchId, winnerId, gameNumber,
                              roundNumber, 1, 3,
                              playerMatchScores["winnerScore"])
            #   insert loser score
            insertPlayerScore(eventId, matchId, loserId, gameNumber,
                              roundNumber, 2, 1,
                              playerMatchScores["loserScore"])

        updateMatchPlayedStatus(matchId, DB)
        DB.close()
    except:
        printErrorDetails(
            sys.exc_info(), "There was an error when reporting match!")


def randomizeGroup(group):
    """
    Returns the shuffled group

    *   Argument
            *   group: List of players registered for the match

    """
    return random.sample(group, len(group))


def showPlayers():
    """
    Display the list of players registered
    can be used to when creating event mappings etc
    """
    DB = connect()
    player_cursor = DB.cursor()
    player_cursor.execute("""select * from players""")
    rows = player_cursor.fetchall()
    if len(rows) == 0:
        print "No Players registered yet!"
    else:
        print "\n\tPlayer Id\t\tPlayer Name\t\tPlayer Email"
        for row in rows:
            print "\n\t\t" + str(row[0]) + "\t\t" + \
                str(row[1]) + "\t\t" + str(row[2])

    DB.close()


def swissPairings(eventId):
    """
    Inserts pairs of players for the next round of a match.
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
    parings = ""
    DB = connect()
    # count if there are matches already registered.
    currentMatches = countEventMatches(eventId)
    matchesPlayed = 0
    rows = playerStandings(eventId)
    matchPairs = []

    if currentMatches != 0:
        matchesPlayed = countEventMatchesPlayed(eventId)
        print "--Matches already played " + str(matchesPlayed)
        if currentMatches == matchesPlayed:
            matchPairs = createParings(rows, eventId)
        else:
            print """-- Previous matches not complete\n
            Finish all current matches to get correct standings
            """
    else:
        print "--No matches registered generating matches"
        matchPairs = createParings(rows, eventId)

    if len(matchPairs) > 0:
        for pair in matchPairs:
            insertMatchRecord(eventId, pair, DB)

    DB.commit()
    DB.close()
    return parings


def updateMatchPlayedStatus(matchId, DB):
    """
    # updateMatchPlayedStatus(matchId)

    Updates the match played record.

    * Arguments
        * matchId: the match in question for which the record is to be updated.
        * DB: The database connection

    * Returns
        * Returns the number of records updated.

    ---
    """
    try:
        match_cursor = DB.cursor()
        match_cursor.execute("""update eventmatches set played=true
             where match_id=%s;""", (matchId,))
        rowcount = match_cursor.rowcount
        DB.commit()
        DB.close()
        return rowcount
    except:
        printErrorDetails(
            sys.exc_info(), """There was an error updating
             match status[updateMatchPlayedStatus]!""")
        DB.rollback()
        DB.close()


def verifyPairs(currentPairings, newParing):
    """
    Checks if the new pairs are unique.

    *   Argument
            *   currentPairings: the list of current pairs.
            *   newParing: The new pairs that were just created.

    """
    result = True
    for pair in newParing:
        player1_id = pair['Player1']['playerId']
        player2_id = pair['Player2']['playerId']
        for cPair in currentPairings:
            if player1_id == cPair['player1_id']:
                if player2_id == cPair['player2_id']:
                    result = False
            elif player2_id == cPair['player1_id']:
                if player1_id == cPair['player2_id']:
                    result = False
    return result
