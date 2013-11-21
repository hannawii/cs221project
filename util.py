import csv

class Player:
	def __init__(self, row):
		self.name = row[0]
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
			rownum+=1

class Team:
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
		return float(self.fg)/self.fga

	def ftp(self):
		return float(self.ft)/self.fta

	@staticmethod
	def play(team, otherTeam):
		wins = 0
		losses = 0

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