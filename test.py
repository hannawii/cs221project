from util import *
from gamestate import *
from evalFunctions import *

start = GameState(numPlayers=2)
extractFeatures(start)
next = start.generateSuccessor('LeBron James')
next = next.generateSuccessor('Kevin Durant')
next = next.generateSuccessor('Chris Paul')
next = next.generateSuccessor('Brandon Jennings')
next = next.generateSuccessor('James Harden')
next = next.generateSuccessor('Kobe Bryant')
next = next.generateSuccessor('Josh Smith')
next = next.generateSuccessor('Paul Millsap')
extractFeatures(start)
next = next.generateSuccessor('Brook Lopez')
next = next.generateSuccessor('Dwight Howard')
"""
print next.data.teams[0].team
print next.data.teams[1].team
print Team.play(next.data.teams[0],next.data.teams[1])
print next.data._win
print next.data._lose
"""