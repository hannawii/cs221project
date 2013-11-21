import random
import gamestate as gameState
import numpy as np

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
