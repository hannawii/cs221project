from util import *
from gamestate import *

def simpleEvaluation(state, evalArgs=None):
	record = [0]*3
	for opponent in xrange(1, state.data.numPlayers):
		results = Team.play(state.data.teams[0], state.data.teams[opponent])
		record[0]+=results[0]
		record[1]+=results[1]
		# record[2]+=results[2]
	# return float(record[0])-record[1]+record[2]*.5
	return float(record[0] - record[1])

def simpleEvaluation2(state, evalArgs=None):
	totalStats = 0
	for playerName in state.data.teams[0].team:
		player = state.data.teams[0].playerMap.map[playerName]
		totalStats += player.threes+player.reb+player.ast+player.pts+player.stl+player.blk-player.tov
	return totalStats

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

    #Add number of remaining people in each position in the pool?



	return features

def logLinearEvaluation(state, w):
    """
    Evaluate the current state using the log-linear evaluation
    function.

    @param state : Tuple of (game, player), the game is
    a game object (see game.py for details, and player in
    {'o', 'x'} designates whose turn it is.

    @param w : List of feature weights.

    @returns V : Evaluation of current game state.
    """
    # BEGIN_YOUR_CODE (around 4 lines of code expected)
    features = extractFeatures(state)
    product = 0
    for i in range(len(w)):
        product += w[i]*features[i]
    return 1/(1+math.exp(-1*product))
    # END_YOUR_CODE
    return V

def TDUpdate(state, nextState, reward, w, eta):
    """
    Given two sequential game states, updates the weights
    with a step size of eta, using the Temporal Difference learning
    algorithm.

    @param state : Tuple of game state (game object, player).
    @param nextState : Tuple of game state (game object, player),
    note if the game is over this will be None. In this case, 
    the next value for the TD update will be 0.
    @param reward : The reward is 1 if the game is over and your
    player won, 0 otherwise.
    @param w : List of feature weights.
    @param eta : Step size for learning.

    @returns w : Updated weights.
    """
    # BEGIN_YOUR_CODE (around 13 lines of code expected)
    if nextState is None:
        r = reward-logLinearEvaluation(state,w)
    else: r = reward+logLinearEvaluation(nextState,w)-logLinearEvaluation(state,w)
    features = extractFeatures(state)
    product = 0
    for i in range(len(w)):
        product += w[i]*features[i]
    gradient = float(math.exp(-1*product))/math.pow(1+math.exp(-1*product),2)
    for i in range(len(w)):
        w[i] += eta*r*gradient*features[i]
    # END_YOUR_CODE
    return w
	