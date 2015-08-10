#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDeleteMatches():
    deleteMatches(1)
    print "*" * 79
    print "1. Old matches can be deleted."
    print "*" * 79


def testDelete():
    deleteAllPlayers()
    print "*" * 79
    print "2. Player records can be deleted."
    print "*" * 79


def testCount():
    # commenting this is not required here
    # deleteMatches(1)

    deletePlayers("Patric W")
    # c = countPlayers()
    # replacing the method to count all the registered players
    c = countRegisteredPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError(
            "After deleting, countPlayers should return zero.")
    print "*" * 79
    print "3. After deleting, countPlayers() returns zero."
    print "*" * 79


def testRegister():
    # commenting not required here
    # deleteMatches()
    # Replacing the method with correct method name
    # deletePlayers()
    deleteAllPlayers()
    # replacing with correct implementation
    # registerPlayer("Chandra Nalaar")
    registerPlayer("Chandra Nalaar", "cn@myproject.com")

    # replacing the method to count all the registered players
    # c = countPlayers()
    c = countRegisteredPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "*" * 79
    print "4. After registering a player, countPlayers() returns 1."
    print "*" * 79


def testRegisterCountDelete():
    # deleteMatches()
    # deletePlayers() replacing with correct implementation
    deleteAllPlayers()
    registerPlayer("Markov Chaney", "mc@myproject.com")
    registerPlayer("Joe Malik", "jm@myproject.com")
    registerPlayer("Mao Tsu-hsi", "mt@myproject.com")
    registerPlayer("Atlanta Hope", "ah@myproject.com")
    # showPlayers()
    # c = countPlayers() replacing with correct implementations
    c = countRegisteredPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    # deletePlayers() replacing with correct implementation
    deleteAllPlayers()
    # showPlayers()
    # c = countPlayers() replacing with correct implementation
    c = countRegisteredPlayers()
    if c != 0:
        raise ValueError(
            "After deleting, countPlayers should return zero.")
    print "*" * 79
    print "5. Players can be registered and deleted."
    print "*" * 79


def testStandingsBeforeMatches():
    # deleteMatches() not relevant system can handle more than one event
    # deletePlayers() replacing
    deleteAllPlayers()
    player1id = registerPlayer("Melpomene Murray", "mm@myproject.com")
    player2id = registerPlayer("Randy Schwartz", "rs@myproject.com")
    # This system supports multiple events
    # Create a new event
    event_id = createevent("Swimming Meet")
    # map registered players to the event
    mapPlayersAndEvent(event_id, player1id)
    mapPlayersAndEvent(event_id, player2id)
    standings = playerStandings(event_id)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before"
                         " they have played any matches.")
    elif len(standings) > 2:
        raise ValueError(
            "Only registered players should appear in standings.")
    # Modifying the test case player standings return a lot more information
    # if len(standings[0]) != 4:
    #     raise ValueError(
    #         "Each playerStandings row should have four columns.")
    if len(standings[0]) != 11:
        raise ValueError(
            "Each playerStandings row should have 11 columns.")

    matchesplayed1 = standings[0]['matchesplayed']
    matchesplayed2 = standings[1]['matchesplayed']
    won1 = standings[0]['won']
    won2 = standings[1]['won']
    playername1 = standings[0]['playername']
    playername2 = standings[1]['playername']

    if matchesplayed1 != 0 or matchesplayed2 != 0 or won1 != 0 or won2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    set1 = set([playername1, playername2])
    set2 = set(["Melpomene Murray", "Randy Schwartz"])
    if set1 != set2:
        raise ValueError("""Registered players' names should appear in
             standings,even if they have no matches played.""")

    print "*" * 79
    print """6. Newly registered players appear in the
     standings with no matches."""
    print "*" * 79
    deleteEvent(event_id)


def testReportMatches():
    # deleteMatches() not relevant system can handle more than one event
    # deletePlayers() replacing
    deleteAllPlayers()
    players = []
    players.insert(0, registerPlayer("Bruno Walton", "bw@myprojec.com"))
    players.insert(0, registerPlayer("Boots O'Neal", "bo@myprojec.com"))
    players.insert(0, registerPlayer("Cathy Burton", "cb@myprojec.com"))
    players.insert(0, registerPlayer("Diane Grant", "dg@myprojec.com"))
    # system works with odd number of players too...
    # players.insert(0, registerPlayer("Scott B", "sb@myprojec.com"))
    # System supports multiple events creating event
    event_id = createevent("Swimming Meet")

    # map registered players to the event
    for player in players:
        mapPlayersAndEvent(event_id, player)

    newParings = swissPairings(event_id)

    # [id1, id2, id3, id4] = [row[0] for row in standings] this wont work

    id1 = newParings[0]['Player1']['playerId']
    id2 = newParings[0]['Player2']['playerId']
    id3 = newParings[1]['Player1']['playerId']
    id4 = newParings[1]['Player2']['playerId']

    matchId1 = newParings[0]['matchId']
    matchId2 = newParings[1]['matchId']
    # Because the system supports draws and byes , multiple games and rounds
    #  we need to Change these to accommodate the extra functionality
    # reportMatch(id1, id2)
    # reportMatch(id3, id4)
    reportMatch(event_id, matchId1, 1, 1, id1, id2, False, False)
    reportMatch(event_id, matchId2, 1, 1, id3, id4, False, False)
    standings = playerStandings(event_id)
    for mr in standings:
        i = mr['playerId']
        m = mr['matchesplayed']
        w = mr['won']
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError(
                "Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError(
                "Each match loser should have zero wins recorded.")
    print "*" * 79
    print "7. After a match, players have updated standings."
    print "*" * 79
    deleteEvent(event_id)
    deleteAllPlayers()


def testPairings():
    # deleteMatches() not relevant system can handle more than one event
    # deletePlayers() replacing
    deleteAllPlayers()
    players = []
    players.insert(
        0, registerPlayer("Twilight Sparkle", "ts@myproject.com"))
    players.insert(0, registerPlayer("Fluttershy", "fshy@myproject.com"))
    players.insert(0, registerPlayer("Applejack", "aj@myproject.com"))
    players.insert(0, registerPlayer("Pinkie Pie", "ppie@myproject.com"))

    event_id = createevent("Swimming Meet")
    # map registered players to the event
    for player in players:
        mapPlayersAndEvent(event_id, player)
    # changing test logic to accommodate new functionality
    # standings = playerStandings()
    # [id1, id2, id3, id4] = [row[0] for row in standings]
    # reportMatch(id1, id2)
    # reportMatch(id3, id4)
    # pairings = swissPairings()
    newParings = swissPairings(event_id)

    id1 = newParings[0]['Player1']['playerId']
    id2 = newParings[0]['Player2']['playerId']
    id3 = newParings[1]['Player1']['playerId']
    id4 = newParings[1]['Player2']['playerId']

    matchId1 = newParings[0]['matchId']
    matchId2 = newParings[1]['matchId']

    reportMatch(event_id, matchId1, 1, 1, id1, id2, False, False)
    reportMatch(event_id, matchId2, 1, 1, id3, id4, False, False)
    # Start round 2 details
    newParings = swissPairings(event_id)

    pid1 = newParings[0]['Player1']['playerId']
    pid2 = newParings[0]['Player2']['playerId']
    pid3 = newParings[1]['Player1']['playerId']
    pid4 = newParings[1]['Player2']['playerId']

    matchId1 = newParings[0]['matchId']
    matchId2 = newParings[1]['matchId']

    if len(newParings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    # [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "*" * 79
    print "8. After one match, players with one win are paired."
    print "*" * 79
    deleteEvent(event_id)
    deleteAllPlayers()


def testParingsWithOddNumberOfPlayers():
    deleteAllPlayers()
    players = []
    players.insert(
        0, registerPlayer("Twilight Sparkle", "ts@myproject.com"))
    players.insert(0, registerPlayer("Fluttershy", "fshy@myproject.com"))
    players.insert(0, registerPlayer("Applejack", "aj@myproject.com"))
    players.insert(0, registerPlayer("Pinkie Pie", "ppie@myproject.com"))
    players.insert(0, registerPlayer("Scott B", "sb@myprojec.com"))

    event_id = createevent("Swimming Meet")
    # map registered players to the event
    for player in players:
        mapPlayersAndEvent(event_id, player)
    # changing test logic to accommodate new functionality
    # standings = playerStandings()
    # [id1, id2, id3, id4] = [row[0] for row in standings]
    # reportMatch(id1, id2)
    # reportMatch(id3, id4)
    # pairings = swissPairings()
    newParings = swissPairings(event_id)

    if len(newParings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    else:
        print "*" * 79
        print """9. Created correct number of pairs even with
         odd number of players."""
        print "*" * 79

    id1 = newParings[0]['Player1']['playerId']
    id2 = newParings[0]['Player2']['playerId']
    id3 = newParings[1]['Player1']['playerId']
    id4 = newParings[1]['Player2']['playerId']

    matchId1 = newParings[0]['matchId']
    matchId2 = newParings[1]['matchId']

    reportMatch(event_id, matchId1, 1, 1, id1, id2, False, False)
    reportMatch(event_id, matchId2, 1, 1, id3, id4, False, False)

    currentStandings = playerStandings(event_id)
    printPlayerScores(event_id)

    countByes = 0
    for playerResult in currentStandings:
        if playerResult['bye'] > 0:
            countByes += 1

    if countByes != 1:
        raise ValueError(
            """There should be only one player with a bye win.""")
    else:
        print "*" * 79
        print "10. Only one player received a bye win."
        print "*" * 79
    deleteEvent(event_id)
    deleteAllPlayers()


def testForDrawGames():
    deleteAllPlayers()
    players = []
    players.insert(0, registerPlayer("Bruno Walton", "bw@myprojec.com"))
    players.insert(0, registerPlayer("Boots O'Neal", "bo@myprojec.com"))
    players.insert(0, registerPlayer("Cathy Burton", "cb@myprojec.com"))
    players.insert(0, registerPlayer("Diane Grant", "dg@myprojec.com"))
    event_id = createevent("Swimming Meet")
    # map registered players to the event
    for player in players:
        mapPlayersAndEvent(event_id, player)

    newParings = swissPairings(event_id)
    id1 = newParings[0]['Player1']['playerId']
    id2 = newParings[0]['Player2']['playerId']
    id3 = newParings[1]['Player1']['playerId']
    id4 = newParings[1]['Player2']['playerId']

    matchId1 = newParings[0]['matchId']
    matchId2 = newParings[1]['matchId']
    reportMatch(event_id, matchId1, 1, 1, id1, id2, True, False)
    reportMatch(event_id, matchId2, 1, 1, id3, id4, False, False)
    standings = playerStandings(event_id)
    countDraws = 0
    for mr in standings:
        d = mr['draws']
        if d > 0:
            countDraws += 1

    if countDraws != 2:
        raise ValueError("There should be 2 players with a draw record")

    print "*" * 79
    print "11. After a draw match, 2 players have draw in standings."
    print "*" * 79

    deleteEvent(event_id)
    deleteAllPlayers()


def testSupportForMoreThanOneEvent():
    deleteAllPlayers()
    players = []
    players.insert(0, registerPlayer("Bruno Walton", "bw@myprojec.com"))
    players.insert(0, registerPlayer("Boots O'Neal", "bo@myprojec.com"))
    players.insert(0, registerPlayer("Cathy Burton", "cb@myprojec.com"))
    players.insert(0, registerPlayer("Diane Grant", "dg@myprojec.com"))
    players.insert(0, registerPlayer("Sam Malik", "sm@myproject.com"))
    players.insert(0, registerPlayer("Papst j", "pj@myprojec.com"))
    event_id = createevent("Swimming Meet")
    # map only the first 4 registered players to the event
    count = 0
    while count < 4:
        mapPlayersAndEvent(event_id, players[count])
        count += 1

    newParings = swissPairings(event_id)
    id1 = newParings[0]['Player1']['playerId']
    id2 = newParings[0]['Player2']['playerId']
    id3 = newParings[1]['Player1']['playerId']
    id4 = newParings[1]['Player2']['playerId']

    matchId1 = newParings[0]['matchId']
    matchId2 = newParings[1]['matchId']
    reportMatch(event_id, matchId1, 1, 1, id1, id2, False, False)
    reportMatch(event_id, matchId2, 1, 1, id3, id4, False, False)

    # create the second event
    event_id2 = createevent("Chess Championship 2015")
    # map only the last 4 registered players to this event
    count = 2
    while count < len(players):
        mapPlayersAndEvent(event_id2, players[count])
        count += 1

    newParings = swissPairings(event_id2)
    pid1 = newParings[0]['Player1']['playerId']
    pid2 = newParings[0]['Player2']['playerId']
    pid3 = newParings[1]['Player1']['playerId']
    pid4 = newParings[1]['Player2']['playerId']

    pmatchId1 = newParings[0]['matchId']
    pmatchId2 = newParings[1]['matchId']
    reportMatch(event_id2, pmatchId1, 1, 1, pid1, pid2, False, False)
    reportMatch(event_id2, pmatchId2, 1, 1, pid3, pid4, False, False)

    standings = playerStandings(event_id)
    standings2 = playerStandings(event_id2)
    printPlayerScores(event_id)
    printPlayerScores(event_id2)
    if len(standings) == 4 and len(standings2) == 4:
        print "*" * 79
        print "12. Multiple events supported with individual standings."
        print "*" * 79
    else:
        raise ValueError("There should be 4 records for both the events ")

    deleteEvent(event_id)
    deleteEvent(event_id2)
    deleteAllPlayers()


if __name__ == '__main__':
    # See the registered players details
    # showPlayers()
    testDeleteMatches()
    testDelete()
    # register another player for the next delete
    registerPlayer("Patric W", "PW@myproject.com")
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    # Extra credits tests
    testParingsWithOddNumberOfPlayers()
    testForDrawGames()
    testSupportForMoreThanOneEvent()
    print "Success!  All tests pass!"
