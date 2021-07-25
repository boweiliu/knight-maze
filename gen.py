#!/usr/bin/env python3

import random
from print_data import print_data, print_animation
import sys

def main(argv):
    n = 5
    try:
        n = int(argv[1])
    except:
        pass
    print_animation(gen(n))

def gen(n=4):
    data = [[0 for colIdx in range(n)] for rowIdx in range(n)]
    yield data
    coords = [(colIdx, rowIdx) for colIdx in range(n) for rowIdx in range(n)] # list of pairs

    # test neighbors function
    #print(utilGetNeighbors(n, (0, 0)))
    #data[0][0] = 1
    #for nbor in utilGetNeighbors(n, (0,0)):
    #    data[nbor[0]][nbor[1]] = 1

    # shuffle all coords
    shuffledCoords = coords.copy()
    random.shuffle(shuffledCoords)

    # testing animation yielding
    #tempData = data
    #for i in range(len(shuffledCoords)):
    #    tempData = dataSet(tempData, shuffledCoords[i], 1)
    #    yield tempData

    # algorithm: set state to 1 == making walls. don't make walls that disconnect the graph, and don't make walls that just chop off dead ends.
    for coord in shuffledCoords:
        # is it a dead end? if so, skip
        nbors = utilGetNeighbors(n, coord)
        emptyNbors = [ nbor for nbor in nbors if dataAt(data, nbor) == 0 ] # find nbors which are empty (not walls)
        # print(emptyNbors, coord) # debug
        if (len(emptyNbors) <= 1):
            continue

        if (isArticulationPoint(data, coord)):
            continue

        # otherwise, create a wall
        data = dataSet(data, coord, 1)
        yield data


# TODO(bowei): do tarjan articulation points
def isArticulationPoint(data, coord):
    n = len(data)

    nbors = utilGetNeighbors(n, coord)
    emptyNbors = [ nbor for nbor in nbors if dataAt(data, nbor) == 0 ] # find nbors which are empty (not walls)
    # assert: len(emptyNbors) >= 2

    # algorithm: DFS from one of them, but dont go through start. if all the others are reachable, it is NOT an articulation point
    touched = {}
    touched[coord] = True
    stack = []
    stack.append(emptyNbors[0])
    while len(stack) > 0:
        curr = stack.pop()
        if curr in touched:
            continue;
        touched[curr] = True
        nbors = [ n for n in utilGetNeighbors(n, curr) if dataAt(data, n) == 0 ]
        for nbor in nbors:
            if nbor in touched:
                continue
            else:
                stack.append(nbor)

    otherNeighbors = emptyNbors[1:]
    # see if all other neighbors are reachable
    if all([ n in touched for n in otherNeighbors]):
        return False
    return True

# shorthand for pair access
def dataAt(data, coord):
    return data[coord[0]][coord[1]]

# shorthand for immutable setting
def dataSet(data, coord, value):
    # first deep copy data
    newData = [ data[i].copy() for i in range(len(data))]
    newData[coord[0]][coord[1]] = value
    return newData

# returns list of neighboring indices
#def utilGetNeighbors(n, centerCoords):
#    (rowIdx, colIdx) = centerCoords
#    candidates = [(rowIdx, colIdx + 1), (rowIdx, colIdx - 1), (rowIdx - 1, colIdx), (rowIdx + 1, colIdx)]
#    return [ c for c in candidates if c[0] >= 0 and c[0] <= n - 1 and c[1] >= 0 and c[1] <= n - 1]

# returns list of KNIGHTS MOVE indices
def utilGetNeighbors(n, centerCoords):
    (r, c) = centerCoords
    candidates = [(r + 1, c + 2), (r +1 , c - 2), (r -1 , c+ 2), (r-1, c-2), (r+2, c+1), (r+2, c-1), (r-2, c+1), (r-2 ,c-1)]
    return [ c for c in candidates if c[0] >= 0 and c[0] <= n - 1 and c[1] >= 0 and c[1] <= n - 1]


if __name__ == '__main__':
    main(sys.argv)

