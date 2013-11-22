from util import *
from gamestate import *

def simpleEvaluation(state, evalArgs=None):
	record = [0]*3
	for opponent in xrange(1, state.data.numPlayers):
		results = Team.play(state.data.teams[0], state.data.teams[opponent])
		record[0]+=results[0]
		record[1]+=results[1]
		record[2]+=results[2]
	return float(record[0])-record[1]+record[2]*.5

def extractFeatures(state):
	features=[]
	#Indicator on what positions each team has
	for team in state.data.teams:
		features += team.positions.values()

	#Indicator on whether we beat each other team
	for opponent in xrange(1, state.data.numPlayers):
		results = Team.play(state.data.teams[0], state.data.teams[opponent])
		if results[0] > results[1]: features += [1]
		else: features += [0]
	