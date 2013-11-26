import csv

class Player:
	def __str__(self):
		return player.name
		
	def __init__(self, row):
		self.name = row[0]
		# self.rank = row[1]
		self.fg = int(row[1])
		self.fga = int(row[2])
		self.threes = int(row[3])
		self.ft = int(row[4])
		self.fta = int(row[5])
		self.reb = int(row[6])
		self.ast = int(row[7])
		self.stl = int(row[8])
		self.blk = int(row[9])
		self.tov = int(row[10])
		self.pts = int(row[11])
		self.pos = row[12]
		# self.rank = row[13]
		self.rank = 0

class PlayerMap:
	def __init__(self, playerData):
		f = open(playerData,"rb")
		reader = csv.reader(f)
		self.map = dict()
		rownum=0
		for row in reader:
			if rownum>0:
				player = Player(row)
				self.map[player.name] = player
				player.rank = rownum
			rownum+=1

class Team:
	def __str__(self):
		return str(self.team)

	def __init__(self, playerMap):
		self.MAX_TEAM_SIZE = 5
		self.team = list()
		self.playerMap = playerMap
		
		#Team comp
		self.positions = {'PG':False,'SG':False,'SF':False,'PF':False,'C':False}

		#Stats
		self.fg = 0
		self.fga = 0
		self.threes = 0
		self.ft = 0
		self.fta = 0
		self.reb = 0
		self.ast = 0
		self.stl = 0
		self.blk = 0
		self.tov = 0
		self.pts = 0

	def add(self, playerName):
		self.team.append(playerName)
		cur = self.playerMap.map[playerName]
		self.positions[cur.pos] = True
		self.fg += cur.fg
		self.fga += cur.fga
		self.threes += cur.threes
		self.ft += cur.ft
		self.fta += cur.fta
		self.reb += cur.reb
		self.ast += cur.ast
		self.stl += cur.stl
		self.blk = cur.blk
		self.tov += cur.tov
		self.pts += cur.pts

	def isFull(self):
		return len(self.team) >= self.MAX_TEAM_SIZE

	def canAdd(self, position):
		return not self.positions[position]

	def fgp(self):
		if self.fga==0: return 0
		return float(self.fg)/self.fga

	def ftp(self):
		if self.fta==0: return 0
		return float(self.ft)/self.fta

	def scaledPlay(team, otherTeam) :
		wins = 0
		losses = 0
		if len(team.team) > 0 : sizeDiff = float(len(otherTeam.team)) / float(len(team.team))
		else : sizeDiff = 0

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

		for stat in xrange(9) :
			if (stats[stat](team) * sizeDiff) > stats[stat](otherTeam) : wins+=1
			elif (stats[stat](team) * sizeDiff) < stats[stat](otherTeam) : losses+=1

		return (wins,losses,9-wins-losses)

	@staticmethod
	def play(team, otherTeam):
		wins = 0
		losses = 0

		# if team.fgp() > otherTeam.fgp(): wins+=team.fgp() - otherTeam.fgp()
		# elif team.fgp() < otherTeam.fgp(): losses+=otherTeam.fgp() - team.fgp()

		# if team.threes > otherTeam.threes: wins+=team.threes - otherTeam.threes
		# elif team.threes < otherTeam.threes: losses+=otherTeam.threes - team.threes

		# if team.ftp > otherTeam.ftp: wins+=team.ftp() - otherTeam.ftp()
		# elif team.ftp < otherTeam.ftp: losses+=otherTeam.ftp() - team.ftp()

		# if team.reb > otherTeam.reb: wins+=team.reb - otherTeam.reb
		# elif team.reb < otherTeam.reb: losses+=otherTeam.reb - team.reb

		# if team.ast > otherTeam.ast: wins+=team.ast - otherTeam.ast
		# elif team.ast < otherTeam.ast: losses+=otherTeam.ast - team.ast

		# if team.stl > otherTeam.stl: wins+=team.stl - otherTeam.stl
		# elif team.stl < otherTeam.stl: losses+=otherTeam.stl - team.stl

		# if team.blk > otherTeam.blk: wins+=team.blk - otherTeam.blk
		# elif team.blk < otherTeam.blk: losses+=otherTeam.blk - team.blk

		# if team.tov < otherTeam.tov: wins+=team.tov - otherTeam.tov
		# elif team.tov > otherTeam.tov: losses+=otherTeam.tov - team.tov

		# if team.pts > otherTeam.pts: wins+=team.pts - otherTeam.pts
		# elif team.pts < otherTeam.pts: losses+=otherTeam.pts - team.pts		

		# return (wins, losses)

		if team.fgp() > otherTeam.fgp(): wins+=1
		elif team.fgp() < otherTeam.fgp(): losses+=1

		if team.threes > otherTeam.threes: wins+=1
		elif team.threes < otherTeam.threes: losses+=1

		if team.ftp > otherTeam.ftp: wins+=1
		elif team.ftp < otherTeam.ftp: losses+=1

		if team.reb > otherTeam.reb: wins+=1
		elif team.reb < otherTeam.reb: losses+=1

		if team.ast > otherTeam.ast: wins+=1
		elif team.ast < otherTeam.ast: losses+=1

		if team.stl > otherTeam.stl: wins+=1
		elif team.stl < otherTeam.stl: losses+=1

		if team.blk > otherTeam.blk: wins+=1
		elif team.blk < otherTeam.blk: losses+=1

		if team.tov < otherTeam.tov: wins+=1
		elif team.tov > otherTeam.tov: losses+=1

		if team.pts > otherTeam.pts: wins+=1
		elif team.pts < otherTeam.pts: losses+=1

		return (wins,losses,9-wins-losses)



def lookup(name, namespace):
	"""
	Get a method or class from any imported module from its name.
	Usage: lookup(functionName, globals())
	"""
	dots = name.count('.')
	if dots > 0:
		moduleName, objName = '.'.join(name.split('.')[:-1]), name.split('.')[-1]
		module = __import__(moduleName)
		return getattr(module, objName)
	else:
		modules = [obj for obj in namespace.values() if str(type(obj)) == "<type 'module'>"]
		options = [getattr(module, name) for module in modules if name in dir(module)]
		options += [obj[1] for obj in namespace.items() if obj[0] == name ]
		if len(options) == 1: return options[0]
		if len(options) > 1: raise Exception, 'Name conflict for %s'
		raise Exception, '%s not found as a method or class' % name



		