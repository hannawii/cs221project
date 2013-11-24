from gamestate import *
from util import *
from agent import *

def train(numPlayers,depth,numGames=2000):
    alpha = 1e-1
    numFeats = 11
    evalFn = submission.logLinearEvaluation
    w = [random.gauss(0,1e-2) for _ in range(numFeats)]
    w[-1] = 0

    for it in xrange(numGames):

        g = GameState()
        players=[RandomAgent() for i in xrange(numPlayers-1)]
		players.insert(0,ABMinimaxAgent(evalFn,depth=depth,agent=0,evalArgs=))

        over = False
        playernum=0
        while not over:
            nextState=turn(players[playernum],playernum,g.clone())
            w = submission.TDUpdate(g,nextState,0,w,alpha)
            g = nextState
            for p in players: p.setWeights(w)
            over = g.is_over()

        winner = g.winner()

        if it%100 == 0:
            print "Game : %d/%d"%(it,numGames)

        # flip outcome for training
        winner = 1.0-winner
        w = submission.TDUpdate(state,None,winner,w,alpha)

    # save weights
    fid = open("weights.bin",'w')
    import pickle
    pickle.dump(w,fid)
    fid.close()
    return w

def test(players,numGames=100,draw=False):
    winners = [0,0]
    for _ in xrange(numGames):
        g = game.Game(game.LAYOUT)
        winner = run_game(players,g,draw)
        print "The winner is : Player %s"%players[winner].player
        winners[winner]+=1
    print "Summary:"
    print "Player %s : %d/%d"%(players[0].player,winners[0],sum(winners))
    print "Player %s : %d/%d"%(players[1].player,winners[1],sum(winners))

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
