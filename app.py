from treedoc import *
class CRDT(object):
	def __init__(self):
		self.treedoc = Node("")
		self.arg = arg
		self.queryList = []
	def insert(atom, pos, siteid,timestamp):
		 queryList.append([timestamp, "insert", [atom, pos, siteid]])
	def delete(pos, siteid, timestamp):
		 queryList.append([timestamp, "delete", [pos, siteid]])
	def getdocument():
		queryList.sort()
		queryDict = dict()
		for i in queryList:
			queryDict[i[0]] = dict()
			queryDict[i[0]].setdefault("insert",[])
			queryDict[i[0]].setdefault("delete",[])
		for i in queryList:
			queryDict[i[0]][i[1]].append(i[2])	
			