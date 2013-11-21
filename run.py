from gamestate import *
from util import *
from agent import *
def run_game(players,g):
    over = False
    while not over:
        for player in players:
            turn(player,g)
            over = g.is_over()
    return g.winner()

def turn(player,g):
    actions = g.getLegalActions()
    if moves: move = player.getAction(actions,g)
    else: move = None
    if move: g.generateSuccessor(move)

def main(args=None):
    from optparse import OptionParser
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-n","--num",dest="numPlayers",default=5,help="Number of players")

    (opts,args) = parser.parse_args(args)    

    players=[HumanAgent() for i in xrange(opts.numPlayers)]
    run_game(players,GameState())

if __name__=="__main__":
    main()
