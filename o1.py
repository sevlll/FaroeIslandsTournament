from random import *

N = 10  # N is number of teams


def homeSwap(scheduleTable, team1, team2):
    for tour in range(1, N + 1):
        if abs(scheduleTable[team1][tour]) == team2:
            scheduleTable[team1][tour] *= -1
            scheduleTable[team2][tour] *= -1
            break
    return scheduleTable


def teamSwap(scheduleTable, team1, team2):
    for tour in range(1, N + 1):
        if abs(scheduleTable[team1][tour]) != team2:
            scheduleTable[team1][tour], scheduleTable[team2][tour] = scheduleTable[team2][tour], scheduleTable[team1][
                tour]
            break
    return scheduleTable


def teamShift(scheduleTable, team1, team2, tour):
    # force team1 play with team2 in tour
    while abs(scheduleTable[team1][tour]) != team2:
        team1Opponent = abs(scheduleTable[team1][tour])
        team2Opponent = abs(scheduleTable[team2][tour])
        if scheduleTable[team1][tour] > 0:
            scheduleTable[team1][tour] = team2
            scheduleTable[team2][tour] = -team1
        else:
            scheduleTable[team1][tour] = -team2
            scheduleTable[team2][tour] = team1
        if scheduleTable[team1Opponent][tour] > 0:
            scheduleTable[team1Opponent][tour] = team2Opponent
            scheduleTable[team2Opponent][tour] = -team1Opponent
        else:
            scheduleTable[team1Opponent][tour] = -team2Opponent
            scheduleTable[team2Opponent][tour] = team1Opponent
    return scheduleTable


def scheduleScore(scheduleTable, distanceTable):
    # the lower score -- the better schedule
    for team in range(1, N + 1):
        teamPlace = team
        sumTravel = 0
        for tour in range(1, N + 1):
            if scheduleTable[team][tour] > 0:
                host = team  # match in home
            else:
                host = -scheduleTable[team][tour]  # match not in home
            sumTravel += distanceTable[teamPlace][host]
            teamPlace = host


def scheduleByPermutation(P):
    scheduleTable = [[0] * N for _ in range(N + 1)]
    for tour in range(1, N):
        Q = [0] + P[1] + P[tour + 1:] + P[2:tour + 1]
        for team in range(1, N + 1):
            teamIndex = Q.index(team)
            if teamIndex == 1:
                opponentIndex = 2
            elif teamIndex == 2:
                opponentIndex = 1
            else:
                opponentIndex = N - (teamIndex - 3)
            scheduleTable[team][tour] = opponentIndex
            if teamIndex % 2 == 0:
                scheduleTable[team][tour] *= -1
    return scheduleTable


def randomPermutation():
    P = [i for i in range(1, N + 1)]
    shuffle(P)
    P = [0] + P
    return P


teamsNames = ["", "Klaksvik", "Torshavn", "Vikingur", "Runavik", "Torshavn", "Fuglafjordur",
              "Streymur", "Vestur", "Toftir", "Tvoroyri"]
teamsNumbers = dict()
for teamNumber in range(1, N + 1):
    teamsNumbers[teamsNames[teamNumber]] = teamNumber
distanceTable = [[0] * (N + 1) for _ in range(N + 1)]

initialSize = 10 ** 4
homeSwapsLimit = 10 ** 4
population = []
for _ in range(initialSize):
    P = randomPermutation()
    scheduleTable = scheduleByPermutation(P)
    for _ in range(homeSwapsLimit):
        team1 = randint(1, N)
        team2 = randint(1, N)
        scheduleTableOptimized = homeSwap(scheduleTable, team1, team2)
        if scheduleScore(scheduleTable, distanceTable) > scheduleScore(scheduleTableOptimized, distanceTable):
            scheduleTable = scheduleTableOptimized
    population.append(scheduleTable)
generationsNumber = 10 ** 6
indvidNumber = 10 ** 3
for _ in range(generationsNumber):
    newPopulation = []
    parent1 = population[randint(0, len(population) - 1)]
    parent2 = population[randint(0, len(population) - 1)]
