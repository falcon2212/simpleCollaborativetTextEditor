from math import *
def dfs(node):
	szleft = 0
	szright = 0
	for i in node.adjacencyListLeft:
		szleft+=dfs(node.adjacencyListLeft[i])	
	for i in node.adjacencyListRight:
		szright+=dfs(node.adjacencyListRight[i])	
	node.size = szright+szleft
	if(node.value != ""):
		node.size+=1
	return node.size	
class Node:
	def __init__(self, data):
		self.value = data
		#adjacency list stores the information of children as {(bit, disambiguator): childNode}
		self.adjacencyListLeft = dict()
		self.adjacencyListRight = dict()
		self.counter = 0
		self.size = 1
		if(data == ""):
			self.size = 0

	#returns node corresponding to the character at pos in crdt	
	def query(self, n):
		dfs(self)
		# print "Query ", n, self.size
		if(n > self.size):
			return None
		def util(node, k, pos, ans):
			if(len(node.adjacencyListLeft) > 0):
				for i in node.adjacencyListLeft:
					j = node.adjacencyListLeft[i]
					util(j, k, pos, ans)
					if(len(ans) > 0):
						return
			if(len(node.value) > 0):
				k[0]+=1
			# print "Query util ", k, pos, ans, node.value
			if(pos[0] == k[0]):
				ans.append(node)
				return
			if(len(node.adjacencyListRight) > 0):
				for i in node.adjacencyListRight:
					j = node.adjacencyListRight[i]
					util(j, k, pos, ans)
					if(len(ans) > 0):
						return
		pos = [n]
		k = [0]
		ans = []
		util(self, k, pos, ans)	
		# print k, pos, ans[0].value
		return ans[0]

					
	def conccurentInsert(self, queries):
		d = dict()
		dfs(self)

		# print self.size, queries
		for i in queries:
			atom, pos, siteId = i
			d[pos]=[]
		for i in queries:
			atom, pos, siteId = i
			d[pos].append(i)
		for i in d:
			l = []
			for j in d[i]:
				atom, pos, S = j
				l.append((S, pos, atom))
			l.sort()
			cnt = 0;
			for j in l:
				S, pos, atom = j
				pos+=cnt
				# print j, pos
				self.insert(atom, pos, S)
				cnt+=1

		 
	def insert(self, atom, insertPos, siteId):
		if(atom == ""):
			return -1
		dfs(self)
		# print "insert ", atom, insertPos, siteId,self.size
		if(insertPos == 1):
			f = self.query(insertPos)
			f.adjacencyListLeft[(0,(siteId, f.counter+1))] = Node(atom)
			f.counter += 1
		elif(insertPos >= self.size):
			f = self.query(self.size)		
			f.adjacencyListRight[(1,(siteId, f.counter+1))] = Node(atom)
			f.counter += 1
		else:
			b = None
			b = self.query(insertPos-1)
			f = self.query(insertPos)
			if(f in b.adjacencyListRight.values()):
				f.adjacencyListLeft[(0,(siteId, f.counter+1))] = Node(atom)
				f.counter+=1
			elif(b in f.adjacencyListLeft.values()):
				b.adjacencyListRight[(1, (siteId, b.counter+1))] = Node(atom)
				b.counter+=1
			else:
				b.adjacencyListRight[(1, (siteId, b.counter+1))] = Node(atom)
				b.counter+=1					
	def delete(self, pos, siteId):
		node = self.query(pos)
		node.value = ""
		node.size = 0

	def flatten(self):
		ans = [""]
		def util(node, ans):
			for i in node.adjacencyListLeft:
				util(node.adjacencyListLeft[i], ans)
			ans[0]+=node.value
			for i in node.adjacencyListRight:
				util(node.adjacencyListRight[i], ans)
		util(self, ans)
		return ans[0]

	def explode(self, atomstring):
		n = len(atomstring)
		h = ceil(log(n+1))
		def allocate(h):
			if(h == 1):
				return Node("")
			else:
				node = Node("")
				node.adjacencyListLeft[(0,(0,0))] = allocate(h-1)	
				node.adjacencyListLeft[(1,(0,0))] = allocate(h-1)
				return node
		def fill(node, atomsting, ptr):
			if(ptr == len(atomstring)):
				return
			else:
				if(len(node.adjacencyListLeft) > 0):
					for i in node.adjacencyListLeft:
						j = node.adjacencyListLeft[i]
						fill(j, atomstring, ptr)
				node.value = atomstring[ptr[0]]
				ptr[0]+=1
				if(len(node.adjacencyListRight) > 0):
					for i in node.adjacencyListRight:
						j = node.adjacencyListRight[i]
						fill(j, atomstring, ptr)
		allocate(h)
		ptr = [0]
		fill(self, atomstring, ptr)

def main():
	crdt = Node("_")
	crdt.insert("hi",1,1)
	crdt.insert("!",2,2)
	crdt.insert("how are you",3,1)
	crdt.delete(3,2)
	conccurentQueries = [["this assignment", 3, 1],["was fun", 3, 2]]
	crdt.conccurentInsert(conccurentQueries)
	s = crdt.flatten()
	print s
main()