from gamestate import *
from util import *
from agent import *
import evalFunctions

def train(numPlayers,depth,numGames=500):
	alpha = 2e-1
	numFeats = 20
	evalFn = evalFunctions.logLinearEvaluation
	w = [random.gauss(0,1e-2) for _ in range(numFeats)]
	w[-1] = 0

	for it in xrange(numGames):

		g = GameState(numPlayers=numPlayers)
		players=[IntelligentAgent() for i in xrange(numPlayers-1)]
		players.insert(0,ABMinimaxAgent(evalFn,depth=depth,agent=0,evalArgs=w))

		over = False
		playernum=0
		while not over:
			nextState=turn(players[playernum],playernum,g)
			w = evalFunctions.TDUpdate(g,nextState,0,w,alpha)
			g = nextState
			for p in players: p.setWeights(w)
			over = g.isOver()
			if playernum==0:playernum=1
			else:playernum=0

		if g.isWin(): winner=0
		else: winner=1

		if it%1 == 0:
			print "Game : %d/%d"%(it,numGames)

		# flip outcome for training
		print 'winner is {}'.format(winner)
		w = evalFunctions.TDUpdate(g,None,1-winner,w,alpha)

	# save weights
	fid = open("weights.bin",'w')
	import pickle
	pickle.dump(w,fid)
	fid.close()
	return w

def test(numPlayers,depth,w,numGames=50,draw=False):
	players=[IntelligentAgent() for i in xrange(numPlayers-1)]
	evalFn = evalFunctions.logLinearEvaluation
	players.insert(0,ABMinimaxAgent(evalFn,depth=depth,agent=0,evalArgs=w))
	winners = [0,0]
	for _ in xrange(numGames):
		g = GameState(numPlayers=numPlayers)
		winner = run_game(players,g)
		print "The winner is : Player %s"%winner
		winners[winner]+=1
	print "Summary:"
	print "Player %s : %d/%d"%(0,winners[0],sum(winners))
	print "Player %s : %d/%d"%(1,winners[1],sum(winners))

def run_game(players,g):
	over = False
	while not over:
		for playerNum, player in enumerate(players):
			g=turn(player,playerNum,g)
			over = g.isOver()
	if g.isWin(): return 0
	return 1

def turn(player,playerNum,g):
	actions = g.getLegalActions(playerNum)
	#print [action.playerName for action in actions]
	# print actions
	if actions: 
		action = player.getAction(actions,g)
		print '{} drafts {}'.format(playerNum,action.playerName)
	else: action = None
	if action: g=g.generateSuccessor(action, playerNum)
	#for team in g.data.teams: print team
	return g

def load_weights(weights):
	if weights is None:
		try:
			import pickle
			weights = pickle.load(open('weights.bin','r'))
		except IOError:
			print "You need to train the weights to use the better evaluation function"
	return weights

def main(args=None):
	from optparse import OptionParser
	usage = "usage: %prog [options]"
	parser = OptionParser(usage=usage)
	parser.add_option("-n","--num",dest="numPlayers",default=5,help="Number of players")
	parser.add_option("-d","--depth",dest="depth",default=1,help="Depth explored")
	parser.add_option("-t","--train",dest="train",action="store_true",default=False,help="Train")
	parser.add_option("-e","--eval",dest="eval",action="store_true",default=False,help="Play with the better eval function for player")

	(opts,args) = parser.parse_args(args)	
	numPlayers = int(opts.numPlayers)
	depth = int(opts.depth)

	weights=None
	if opts.train:
		weights=train(numPlayers,depth)

	if opts.eval:
		weights = load_weights(weights)
		evalFn = evalFunctions.logLinearEvaluation
		evalArgs = weights
	else:
		evalFn = evalFunctions.logLinearEvaluation
		evalArgs = weights

	"""
	# players=[HumanAgent() for i in xrange(numPlayers-1)]
	players=[IntelligentAgent() for i in xrange(numPlayers-1)]
	players.insert(0,ABMinimaxAgent(evalFn,depth=depth,agent=0))
	print run_game(players,GameState(numPlayers=numPlayers))
	"""

	test(numPlayers,depth,w=weights)

if __name__=="__main__":
	main()
