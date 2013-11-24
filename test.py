from util import *
from gamestate import *
from evalFunctions import *

start = GameState(numPlayers=2)
print extractFeatures(start)
next = start.generateSuccessor('LeBron James',0)
next = next.generateSuccessor('Kevin Durant',1)
next = next.generateSuccessor('Chris Paul',0)
next = next.generateSuccessor('Brandon Jennings',1)
next = next.generateSuccessor('James Harden',0)
next = next.generateSuccessor('Kobe Bryant',1)
next = next.generateSuccessor('Josh Smith',0)
next = next.generateSuccessor('Paul Millsap',1)
print extractFeatures(next)
next = next.generateSuccessor('Brook Lopez',0)
next = next.generateSuccessor('Dwight Howard',1)
"""
print next.data.teams[0].team
print next.data.teams[1].team
print Team.play(next.data.teams[0],next.data.teams[1])
print next.data._win
print next.data._lose
"""