from gamestate import *
from util import *
from agent import *
def run_game(players,g):
	over = False
	while not over:
		for playerNum, player in enumerate(players):
			g=turn(player,playerNum,g)
			over = g.isOver()
	return g.isWin()

def turn(player,playerNum,g):
	actions = g.getLegalActions(playerNum)
	print [action.playerName for action in actions]
	# print actions
	if actions: 
		action = player.getAction(actions,g)
		print action
	else: action = None
	if action: g=g.generateSuccessor(action, playerNum)
	for team in g.data.teams: print team
	return g

def main(args=None):
	from optparse import OptionParser
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-n","--num",dest="numPlayers",default=5,help="Number of players")
	parser.add_option("-d","--depth",dest="depth",default=2,help="Depth explored")
	parser.add_option("-a","--agent",dest="agent",default='HumanAgent',help="Opponent agent")

	(opts,args) = parser.parse_args(args)	
	numPlayers = int(opts.numPlayers)
	depth = int(opts.depth)

	# players=[HumanAgent() for i in xrange(numPlayers-1)]
	players=[IntelligentAgent() for i in xrange(numPlayers-1)]
	players.insert(0,ABMinimaxAgent('simpleEvaluation',depth=depth, agent=0))
	print run_game(players,GameState(numPlayers=numPlayers))

if __name__=="__main__":
	main()
