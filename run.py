from gamestate import *
from util import *
from agent import *
def run_game(players,g):
	over = False
	while not over:
		for player in players:
			g=turn(player,g)
			over = g.isOver()
	return g.isWin()

def turn(player,g):
	actions = g.getLegalActions()
	print actions
	if actions: 
		action = player.getAction(actions,g)
		print action
	else: action = None
	if action: g=g.generateSuccessor(action)
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

	players=[ABMinimaxAgent('simpleEvaluation',depth=depth) for i in xrange(numPlayers-1)]
	players.insert(0,HumanAgent())
	print run_game(players,GameState(numPlayers=numPlayers))

if __name__=="__main__":
	main()
