import random
import gamestate as gameState
import numpy as np
import util
from gamestate import Actions
from heapq import nsmallest, nlargest
from evalFunctions import *

class Agent:
	def getAction(self, actions, gameState=None):
		raise NotImplementedError("Override me")
	def setWeights(self,w):
		return None
	def getActionWithExploring(self, actions, gameState=None):
		if random.random() < .4:
			if actions:
	 			def	getRank(action) :
	 				return action.playerRank
				return random.choice(list(nsmallest(5, actions, key=getRank)))
			return None
		else: 
			return self.getAction(actions, gameState)

class RandomAgent(Agent):
	def getAction(self, actions, gameState=None):
		if actions:
			return random.choice(list(actions))
		return None

class IntelligentAgent(Agent) :
	def getAction(self, actions, gameState=None) :
	 	def	getRank(action) :
	 		return action.playerRank

		if actions :
			return random.choice(list(nsmallest(20, actions, key=getRank)))
		return None

class FeaturesAgent(Agent) :
	def __init__(self, evalFn, depth = '1', agent = 0, evalArgs = None):
		self.index = agent #any agent can be who we are maximizing
		self.evaluationFunction = evalFn
		self.depth = int(depth)
		self.evaluationArgs = evalArgs
	def setWeights(self, w):
		"""
		Updates weights of reflex agent.  Used for training.
		"""
		self.evaluationArgs = w


class FeatAgent(FeaturesAgent) :
	def getAction(self, actions, gameState=None) :
		def getWeight(action) :
			newGameState = gameState.generateSuccessor(action, self.index)
			return self.evaluationFunction(newGameState, self.evaluationArgs)
		return max(actions, key=getWeight)
	"""
	def getActionWithExploring(self, actions, gameState=None) :
		def getWeight(action) :
			newGameState = gameState.generateSuccessor(action, self.index)
			return self.evaluationFunction(newGameState, self.evaluationArgs)
		if random.random() < .4:
			if actions:
				return random.choice(list(actions))
			return None
		else: return max(actions, key=getWeight)
	"""


class SearchAgent(Agent):

	def __init__(self, evalFn, depth = '1', agent = 0, evalArgs = None):
		self.index = agent #any agent can be who we are maximizing
		self.evaluationFunction = evalFn
		self.depth = int(depth)
		self.evaluationArgs = evalArgs
	def setWeights(self, w):
		"""
		Updates weights of reflex agent.  Used for training.
		"""
		self.evaluationArgs = w

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
				else : return self.evaluationFunction(newGameState,self.evaluationArgs)
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

		if random.random() < .2:
			if actions:
				return random.choice(list(actions))
			return None
		else: return Vopt(gameState, gameState.getCurrPlayer(), self.depth, float('-inf'), float('+inf'))
		


class ExpectimaxAgent(SearchAgent):

	def getAction(self, actions, gameState):

		def Vopt(newGameState, numAgent, depth) :	 
		
			def getVopt(action) :	
				return Vopt(newGameState.generateSuccessor(action, numAgent % newGameState.getNumAgents()), numAgent + 1, depth)

			def expectedValue(actionList) :
				vList = []
				for action in actionList :
					vList.append(getVopt(action))
				prob = len(vList)
				vList[:] = [float(i / prob) for i in vList] 
				return sum(vList)

		
			actions = newGameState.getLegalActions(numAgent % newGameState.getNumAgents())		 

			if newGameState.isWin() or newGameState.isLose() or len(actions) == 0 or depth == 0 :
				if numAgent == self.index : return None
				else : return self.evaluationFunction(newGameState,self.evaluationArgs)
		

			if numAgent == self.index : return max(actions, key=getVopt)

			elif numAgent % newGameState.getNumAgents() == self.index : 
				v = float('-inf')
				for action in actions :
					v = max(v, getVopt(action))
				return v

			elif ((numAgent + 1) % newGameState.getNumAgents()) == self.index :
				depth -= 1
				return expectedValue(actions)

			else :
				return expectedValue(actions)


		return Vopt(gameState, gameState.getCurrPlayer(), self.depth)


class HumanAgent(Agent):

	def getAction(self, actions, gameState=None):
		while True:
			if not actions:
				raw_input("No NBA players for you...(hit enter)")
				return None
			while True:
				action = raw_input("Please enter a basketball player to draft: ")
				action = self.get_formatted_move(action, gameState)
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

			# if action in actions:
			# 	legal = FantasyBBRules.getLegalActions(state, playerNum)
			if any(a.playerName == action.playerName for a in actions) :
				break
			# elif move[::-1] in moves:
			#	 move = move[::-1]
			#	 break
			else:
				print "You can't play that move"
		return action

	def get_formatted_move(self, playerName, gameState):

		if playerName in gameState.data.playerPool.keys() :
			return Actions(playerName, gameState.data.playerPool[playerName].rank) 
		else :
			return None
