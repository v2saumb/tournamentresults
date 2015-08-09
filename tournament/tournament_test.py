#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *


def testDeleteMatches():
    deleteMatches(1)
    print "1. Old matches can be deleted."


def testDelete():
    deleteAllPlayers()
    print "2. Player records can be deleted."


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
    print "3. After deleting, countPlayers() returns zero."


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
    print "4. After registering a player, countPlayers() returns 1."


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
    print "5. Players can be registered and deleted."


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
    print "new event " + str(event_id)
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
    printPlayerScores(event_id)
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
    if set([playername1, playername2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("""Registered players' names should appear in
             standings,even if they have no matches played.""")

    print """6. Newly registered players appear in the
     standings with no matches."""
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
    players.insert(0, registerPlayer("Scott B", "sb@myprojec.com"))
    # System supports multiple events creating event

    event_id = createevent("Swimming Meet")
    print "new event " + str(event_id)

    for player in players:
        print player
        # map registered players to the event
        mapPlayersAndEvent(event_id, player)

    standings = playerStandings(event_id)
    printPlayerScores(event_id)
    swissPairings(event_id)
    printPlayerScores(event_id)

    # [id1, id2, id3, id4] = [row[0] for row in standings]
    # reportMatch(id1, id2)
    # reportMatch(id3, id4)
    # standings = playerStandings()
    # for (i, n, w, m) in standings:
    #     if m != 1:
    #         raise ValueError("Each player should have one match recorded.")
    #     if i in (id1, id3) and w != 1:
    #         raise ValueError(
    #             "Each match winner should have one win recorded.")
    #     elif i in (id2, id4) and w != 0:
    #         raise ValueError(
    #             "Each match loser should have zero wins recorded.")
    # print "7. After a match, players have updated standings."
    deleteEvent(event_id)
    deleteAllPlayers()


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


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
    # testPairings()
    print "Success!  All tests pass!"
