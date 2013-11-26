from util import *
from gamestate import *
import math
import numpy

def simpleEvaluation(state, evalArgs=None):
	print 'please dont happen'
	record = [0]*3
	for opponent in xrange(1, state.data.numPlayers):
		results = Team.play(state.data.teams[0], state.data.teams[opponent])
		record[0]+=results[0]
		record[1]+=results[1]
		# record[2]+=results[2]
	# return float(record[0])-record[1]+record[2]*.5
	return float(record[0] - record[1])

def simpleEvaluation2(state, evalArgs=None):
	print 'please dont happen either'
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

	#Indicator on how many players at each unfilled position remain
	#Note, the given state is not good if numPlayers is large and there are little of a certain position


	team = state.data.teams[0]
	#Indicator on strength of each stat
	if team.fgp() >= .50: features += [1]
	else: features += [0]

	if team.ftp() >= .80: features += [1]
	else: features += [0]

	if team.threes >= len(team.team)*100: features += [1]
	else: features += [0]

	if team.reb >= len(team.team)*600: features += [1]
	else: features += [0]

	if team.stl >= len(team.team)*100: features += [1]
	else: features += [0]

	if team.ast >= len(team.team)*400: features += [1]
	else: features += [0]

	if team.blk >= len(team.team)*50: features += [1]
	else: features += [0]

	if team.pts >= len(team.team)*1500: features += [1]
	else: features += [0]

	if team.tov <= len(team.team)*150: features += [1]
	else: features += [0]

	# if team.fgp() > .45: features += [1 + team.fgp()]
	# else: features += [0]

	# if team.ftp() > .80: features += [1 + team.ftp()]
	# else: features += [0]

	# if team.threes > len(team.team)*100: features += [team.threes - len(team.team) * 100]
	# else: features += [0]

	# if team.reb > len(team.team)*600: features += [team.reb - len(team.team) * 600]
	# else: features += [0]

	# if team.stl > len(team.team)*60: features += [team.stl - len(team.team) * 60]
	# else: features += [0]

	# if team.ast > len(team.team)*400: features += [team.ast - len(team.team) * 400]
	# else: features += [0]

	# if team.blk > len(team.team)*30: features += [team.blk - len(team.team) * 30]
	# else: features += [0]

	# if team.pts > len(team.team)*1500: features += [team.pts - len(team.team) * 1500]
	# else: features += [0]

	# if team.tov < len(team.team)*40: features += [len(team.team) * 40 - team.tov]
	# else: features += [0]

	# features += [team.fgp()]
	# features += [team.ftp()]
	# features += [team.threes - len(team.team) * 100]
	# features += [team.reb - len(team.team) * 600]
	# features += [team.stl - len(team.team) * 60]
	# features += [team.ast - len(team.team) * 400]
	# features += [team.blk - len(team.team) * 30]
	# features += [team.pts - len(team.team) * 1500]
	# features += [team.tov - len(team.team) * 40]

	#Indicator on whether we beat each other team
	for opponent in xrange(1, state.data.numPlayers):
		results = Team.scaledPlay(state.data.teams[0], state.data.teams[opponent])
		# if results[0] > results[1]: features += [1]
		# if results[0] > results[1]: features += [results[0] - results[1]]
		# else: features += [0]
		if len(state.data.teams[opponent].team) > 0 : features += [results[0] - results[1]]
		else : features += [0]

	#Add number of remaining people in each position in the pool?	

	def fgp(team) : return team.fgp()
	def ftp(team) : return team.ftp()
	def threes(team) : return team.threes
	def reb(team) : return team.reb
	def stl(team) : return team.stl
	def ast(team) : return team.ast
	def blk(team) : return team.blk
	def pts(team) : return team.pts
	def tov(team) : return team.tov

	stats = {0 : fgp, 1 : ftp, 2 : threes, 3 : reb, 4 : stl, 5 : ast, 6 : blk, 7 : pts, 8 : tov}

	#Indicator on each stat compared to other teams
	largeTeam = True
	for stat in xrange(9) :
		nums = [] 
		
		for t in state.data.teams:
			sizeDiff = 0
			if len(team.team) > 0 : sizeDiff = float(len(t.team)) / float(len(team.team))
			if len(t.team) == len(team.team) : num = stats[stat](t) * sizeDiff
			else : num = stats[stat](t)
			if len(t.team) <= 0 : largeTeam = False
			nums.append(num)
		# if not largeTeam : break
		
		if (numpy.median(nums) < (stats[stat](team) * sizeDiff)) : features += [1]#and largeTeam : features += [1]
		else : features += [0]
		
		if (max(nums) <= (stats[stat](team) * sizeDiff)) and largeTeam : features += [2]
		# if numpy.median(nums) < stats[stat](team) : features += [(stats[stat](team) - numpy.median(nums))]
		else : features += [0]
		# features += [(stats[stat](team) - numpy.median(nums))]

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
	for i in range(len(features)):
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
	print 'in td update, weights is now {}'.format(w)
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
	