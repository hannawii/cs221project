import collections
from util import *
import copy


class GameState:
	####################################################
	# Accessor methods: use these to access state data #
	####################################################
	def getLegalActions(self, playerNum):
		if self.isWin() or self.isLose(): return []

		return FantasyBBRules.getLegalActions(self, playerNum)

	def generateSuccessor(self, action, playerNum):
		"""
		Returns the successor state after the specified agent takes the action.
		"""

		# Check that successors exist
		if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

		# Copy current state
		state = GameState(prevState=self)

		FantasyBBRules.applyAction(state, action, playerNum)

		if state.data.currPlayer + 1 == state.data.numPlayers and state.data.teams[state.data.currPlayer].isFull() : self.calculateWinner(state)

		state.data.currPlayer += 1

		if (state.data.currPlayer >= state.data.numPlayers): state.data.currPlayer = 0
	
		return state

	def calculateWinner(self, state) :
		winRecord = collections.defaultdict(int)
		for gamePlayer, team in enumerate(state.data.teams) :
			if gamePlayer + 1 == state.data.numPlayers: continue
			for opponent in xrange(gamePlayer + 1, state.data.numPlayers) :
				results = team.play(team, state.data.teams[opponent])
				if results[0] > results[1] : winRecord[gamePlayer] += 1
				elif results[1] >= results[0] : winRecord[opponent] += 1 #currently a tie goes to the opponent
				# else :
				# 	winRecord[gamePlayer] += 1
				# 	winRecord[opponent] += 1
		if max(winRecord, key=winRecord.get) == 0 : state.data._win = True 
		else : state.data._lose = True


	def getNumAgents(self) :
		return self.data.numPlayers

	def getCurrPlayer(self) :
		return self.data.currPlayer

	def isLose( self ):
		return self.data._lose


	def isWin( self ):
		return self.data._win

	def isOver(self) :
		return self.data._win or self.data._lose


	def __init__( self, prevState = None, numPlayers=5):
		if prevState != None: # Initial state
			self.data = GameStateData(prevState=prevState.data, numPlayers=numPlayers)
		else:
			self.data = GameStateData(numPlayers=numPlayers)

	def deepCopy( self ):
		state = GameState( self )
		state.data = self.data.deepCopy()
		return state

	def __eq__( self, other ):
		return self.data == other.data

	def __hash__( self ):
		return hash( self.data )

	def __str__( self ):

		return str(self.data)

class GameStateData:

	def __init__( self, numPlayers = 5, prevState = None ):
		if prevState != None:
			self.playerPool = copy.deepcopy(prevState.playerPool)
			self.teams = copy.deepcopy(prevState.teams)
			self.currPlayer = copy.deepcopy(prevState.currPlayer)
			self.numPlayers = prevState.numPlayers
			# self.money = prevState.money
		else :
			playerMap = PlayerMap('playerData.csv')
			self.playerPool = playerMap.map #change based on fanhals stuff
			self.teams = [Team(playerMap) for i in xrange(numPlayers)]
			self.currPlayer = 0
			self.numPlayers = numPlayers #can change -> need to allow user to dictate
			# self.money = 100
		self._win = False
		self._lose = False

	# def deepCopy(self) :



class FantasyBBRules :

	def getLegalActions(state, playerNum) :
		return Actions.getPossibleActions(state, playerNum)
	getLegalActions = staticmethod(getLegalActions)

	def applyAction(state, action, playerNum) :
		legal = FantasyBBRules.getLegalActions(state, playerNum)
		if not any(a.playerName == action.playerName for a in legal) :
		# if action.playerName not in legal:
			raise Exception("Illegal action " + str(action))

		#Update teams
		state.data.teams[playerNum].add(action.playerName)
		state.data.playerPool.pop(action.playerName, None)

		#Update money
		#state.money -= action.player.price
		# for team in state.data.teams: print team
	applyAction = staticmethod(applyAction)

class Actions :

	def getPossibleActions(state, playerNum) :
		actions=list()
		# positions = [key for key, value in state.data.teams[playerNum].positions.iteritems() if not value]
		# return [player.name for player in state.data.playerPool.values() if player.pos in positions]
		playerPool = state.data.playerPool.values()
		
		for player in playerPool :
			if state.data.teams[playerNum].canAdd(player.pos): 
				actions.append(Actions(player.name, player.rank))
			# else : state.data.playerPool.pop(player.name, None)

		return actions

	getPossibleActions = staticmethod(getPossibleActions)
	
	def __init__(self, name, rank):
		self.playerName = name
		self.playerRank = rank

"""
#Test
start = GameState(numPlayers=2)
next = start.generateSuccessor('LeBron James')
next = next.generateSuccessor('Kevin Durant')
next = next.generateSuccessor('Chris Paul')
next = next.generateSuccessor('Brandon Jennings')
next = next.generateSuccessor('James Harden')
next = next.generateSuccessor('Kobe Bryant')
next = next.generateSuccessor('Josh Smith')
next = next.generateSuccessor('Paul Millsap')
next = next.generateSuccessor('Brook Lopez')
next = next.generateSuccessor('Dwight Howard')
print next.data.teams[0].team
print next.data.teams[1].team
print Team.play(next.data.teams[0],next.data.teams[1])
print next.data._win
print next.data._lose
"""