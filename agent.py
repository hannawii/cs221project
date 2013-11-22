import random
import gamestate as gameState
import numpy as np
import util
from evalFunctions import *

class Agent:
	def getAction(self, actions, gameState=None):
		raise NotImplementedError("Override me")

class RandomAgent(Agent):
	def getAction(self, actions, gameState=None):
		if actions:
			return random.choice(list(actions))
		return None

# class IntelligentAgent(Agent) :
#	 def getAction(self, actions, gameState=None) :
#		 if actions :

#		 return None

class SearchAgent(Agent):

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '1', agent = 0):
		self.index = agent #any agent can be who we are maximizing
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)


class ABMinimaxAgent(SearchAgent):
	"""
	Your minimax agent with alpha-beta pruning
	"""

	def getAction(self, actions, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		def Vopt(newGameState, numAgent, depth, alpha, beta) :	 

			
			def getVopt(action) :
				return Vopt(newGameState.generateSuccessor(action, numAgent % newGameState.getNumAgents()), numAgent + 1, depth, alpha, beta)

			
			actions = newGameState.getLegalActions(numAgent % newGameState.getNumAgents())	
			# if Directions.STOP in actions : actions.remove(Directions.STOP)		 

			if newGameState.isWin() or newGameState.isLose() or len(actions) == 0 or depth == 0 :
				if numAgent == self.index : return None
				else : return self.evaluationFunction(newGameState)
				# return self.evaluationFunction(newGameState)
			

			if numAgent == self.index :
				bestAction = None
				v = float('-inf')
				for action in actions :
					newV = getVopt(action)
					v = max(v, newV)
					if v == newV : bestAction = action
					if v >= beta : return action
					alpha = max(v, alpha)

				return bestAction


			elif numAgent % newGameState.getNumAgents() == self.index : 
				v = float('-inf')
				for action in actions :
					v = max(v, getVopt(action))
					if v >= beta : return v
					alpha = max(v, alpha)
				return v

			elif ((numAgent + 1) % newGameState.getNumAgents()) == self.index :
				depth -= 1
				v = float('+inf')
				for action in actions :
					v = min(v, getVopt(action))
					if v <= alpha : return v
					beta = min(beta, v)
				return v

			else :
				v = float('+inf')
				for action in actions :
					v = min(v, getVopt(action))
					if v <= alpha : return v
					beta = min(beta, v)
				return v

		return Vopt(gameState, gameState.getCurrPlayer(), self.depth, float('-inf'), float('+inf'))
		


# class ABExpectimaxAgent(SearchAgent):
# 	"""
# 	Your minimax agent with alpha-beta pruning
# 	"""

# 	def getAction(self, gameState):

# 		def Vopt(newGameState, depth, alpha, beta) :	 

			
# 			def getVopt(action) :	
# 				return Vopt(newGameState.generateSuccessor(action), depth, alpha, beta)

			
# 			actions = newGameState.getLegalActions()	
# 			# if Directions.STOP in actions : actions.remove(Directions.STOP)		 


# 			if newGameState.isWin() or newGameState.isLose() or len(actions) == 0 or depth == 0 :
# 				# if numAgent == self.index : return Directions.STOP
# 				# else : return self.evaluationFunction(newGameState)
# 				return self.evaluationFunction(newGameState)
			

# 			if newGameState.getCurrPlayer() == self.index :
# 				bestAction = None
# 				v = float('-inf')
# 				for action in actions :
# 					newV = getVopt(action)
# 					v = max(v, newV)
# 					if v == newV : bestAction = action
# 					if v >= beta : return action
# 					alpha = max(v, alpha)

# 				return bestAction


# 			elif newGameState.getCurrPlayer() % newGameState.getNumAgents() == 0 : 
# 				v = float('-inf')
# 				for action in actions :
# 					v = max(v, getVopt(action))
# 					if v >= beta : return v
# 					alpha = max(v, alpha)
# 				return v

# 			elif ((newGameState.getCurrPlayer() + 1) % newGameState.getNumAgents()) == 0 :
# 				depth -= 1
# 				v = float('+inf')
# 				for action in actions :
# 					v = min(v, getVopt(action))
# 					if v <= alpha : return v
# 					beta = min(beta, v)
# 				return v

# 			else :
# 				v = float('+inf')
# 				for action in actions :
# 					v = min(v, getVopt(action))
# 					if v <= alpha : return v
# 					beta = min(beta, v)
# 				return v

# 		return Vopt(gameState, self.depth, float('-inf'), float('+inf'))


class HumanAgent(Agent):

	def getAction(self, actions, gameState=None):
		while True:
			if not actions:
				raw_input("No NBA players for you...(hit enter)")
				return None
			while True:
				action = raw_input("Please enter a basketball player to draft: ")
				#action = self.get_formatted_move(mv1, game)
				if not action:
					print 'The player you chose is not very good, you should reconsider'
				else:
					break

			# while True:
			#	 mv2 = raw_input("Please enter a second move (enter to skip): ")
			#	 if mv2 == '':
			#		 mv2 = None
			#		 break
			#	 mv2 = self.get_formatted_move(mv2)
			#	 if not mv2:
			#		 print 'Bad format enter e.g. "3,4"'
			#	 else:
			#		 break

			# if mv2:
			#	 move = (mv1,mv2)
			# else:
			#	 move = (mv1,)

			if action in actions:
				break
			# elif move[::-1] in moves:
			#	 move = move[::-1]
			#	 break
			else:
				print "You can't play that move"
		return action

	def get_formatted_move(self, action, gameState):

		if stringAction in gameState.data.playerPool:
			return gameState.data.playerPool[stringAction]
		else :
			return False
