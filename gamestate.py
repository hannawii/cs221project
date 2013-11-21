import collections
import util


class GameState:
	####################################################
  	# Accessor methods: use these to access state data #
  	####################################################

  	def getLegalActions( self):
    """
    Returns the legal actions for the agent specified.
    """
	    if self.isWin() or self.isLose(): return []

	    return FantasyBBRules.getLegalActions(self)

 	def generateSuccessor(self, stringAction):
    """
    Returns the successor state after the specified agent takes the action.
    """

	    # Check that successors exist
	    if self.isWin() or self.isLose(): raise Exception('Can\'t generate a successor of a terminal state.')

	    # Copy current state
	    state = GameState(self)

	    action = state.data.playerPool[stringAction]

	    FantasyBBRules.applyAction(state, action)

	    if state.data.currPlayer + 1 == state.data.numPlayers and state.data.teams[state.data.currPlayer].isFull() : self.calculateWinner(state)

	    state.data.currPlayer += 1

	    if (state.data.currPlayer >= state.data.numPlayers) state.data.currPlayer = 0
	   	
	    return state

	def calculateWinner(state) :
		winRecord = collections.defaultdict()
		for gamePlayer, team in enumerate(state.data.teams) :
			if gamePlayer + 1 == state.data.numPlayers continue
			for opponent, oppteam in enumerate(state.data.teams[gamePlayer + 1:]) :
				results = team.play(team, state.data.teams[opponent])

				if results[0] > results[1] : winRecord[gamePlayer] += 1
				elif results[1] > results[0] : winRecord[opponent] += 1

		if max(winRecord, key=winRecord.get) == 0 : state.data._win = True #note that this will not deal with no winner
		else : state.data._lose = True


	def isLose( self ):
    	return self.data._lose


 	def isWin( self ):
    	return self.data._win


    def __init__( self, prevState = None ):
    """
    Generates a new state by copying information from its predecessor.
    """
	    if prevState != None: # Initial state
	      	self.data = GameStateData(prevState.data)
	    else:
	      	self.data = GameStateData()

	def deepCopy( self ):
	    state = GameState( self )
	    state.data = self.data.deepCopy()
	    return state

  	def __eq__( self, other ):
    """
    Allows two states to be compared.
    """
    	return self.data == other.data

  	def __hash__( self ):
    """
    Allows states to be keys of dictionaries.
    """
    	return hash( self.data )

  	def __str__( self ):

    	return str(self.data)

class GameStateData:
  """

  """
  def __init__( self, numPlayers = 5, prevState = None ):
    """
    Generates a new data packet by copying information from its predecessor.
    """
    if prevState != None:
      	self.playerPool = prevState.playerPool.shallowCopy()
      	self.teams = prevState.teams.shallowCopy()
      	self.currPlayer = prevState.currPlayer
      	self.numPlayers = prevState.numPlayers
      	# self.money = prevState.money
    else :
    	self.playerPool = PlayerMap("playerdata.csv").map #change based on fanhals stuff
    	self.teams = [Team(PlayerMap("playerdata.csv"))] * numPlayers
    	self.currPlayer = 0
    	self.numPlayers = numPlayers #can change -> need to allow user to dictate
    	# self.money = 100
    self._win = False
    self._lose = False


class FantasyBBRules :

	def getLegalActions(state) :
	"""
    Returns a list of possible actions.
    """
    	return Actions.getPossibleActions(state)

    def applyAction(state, acton) :
    """
    Edits the state to reflect the results of the action.
    """
	    legal = PacmanRules.getLegalActions(state)
	    if action not in legal:
	      	raise Exception("Illegal action " + str(action))

	    #Update teams
	    state.data.teams[state.data.currPlayer].addPlayer(action.name)

	    #Update money
	    #state.money -= action.player.price


class Actions :

	def getPossibleActions(state) :

		for player in state.data.playerPool.values() :
			if state.data.teams[state.data.currPlayer].canAdd(player.name) : actions.add(player)

		return actions

	# def __init__(self, action, player = None):
	# 	self.action = action
	# 	self.player = player







