from math import *
from copy import *
def dfs(node):
	szleft = 0
	szright = 0
	if(node == None):
		return 0
	szleft+=dfs(node.left)	
	szright+=dfs(node.right)	
	node.size = szright+szleft
	if(node.value != ""):
		node.size+=1
	return node.size	
#returns true if node1 is ancestor of node2		
def ancestor(node1, node2):
	par = node2;
	while par != None:
		if(par == node1):
			return True
		par = par.parent	
	return False	
class Node:
	def __init__(self, data):
		self.value = data
		#adjacency list stores the information of children as {(bit, disambiguator): childNode}
		self.left = None
		self.right = None
		self.counter = 0
		self.size = 1
		self.parent = None
		if(data == ""):
			self.size = 0

	#returns node corresponding to the character at pos in crdt	
	def query(self, n):
		if(self.size == 0):
			return self
		# print "Query ", n, self.size
		if(n > self.size):
			return None
		def util(node, k, pos, ans):
			if(node.left != None):
				j = node.left
				util(j, k, pos, ans)
				if(len(ans) > 0):
					return
			if(len(node.value) > 0):
				k[0]+=1
			# print "Query util ", k, pos, ans, node.value
			if(pos[0] == k[0]):
				ans.append(node)
				return
			if(node.right != None):
				j = node.right
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

		# print self.size, queries
		for i in queries:
			atom, pos, siteId = i
			d[pos]=[]
		positions = dict()
		for i in queries:
			atom, pos, siteId = i
			d[pos].append(i)
			if(pos == 1 or pos == self.size):
				positions[pos] = [self.query(pos)]
			else:
				positions[pos] = [self.query(pos-1),self.query(pos)]	
		cnt1 = 0
		prevSize = self.size
		for i in d:
			l = []
			for j in d[i]:
				atom, pos, S = j
				l.append((S, pos, atom))
			l.sort()
			# print l,i 
			# print prevSize,positions[i][0].value
			# if(len(positions[i])>1):
 		# 		print positions[i][1].value
			cnt = 0;
			if(i == 1):
				for j in l:
					S, pos, atom = j
					positions[i][0].right = Node(atom)
					positions[i][0].right.parent = positions[i][0]
					positions[i][0].size+=1
					par = positions[i][0].parent
					while( par != None ):
						par.size+=1
						par = par.parent
					positions[i][0] = positions[i][0].right
				positions[i][0].counter+=1	
			elif(i == prevSize):
				for j in l:
					S, pos, atom = j
					positions[i][0].right = Node(atom)
					positions[i][0].right.parent = positions[i][0]
					positions[i][0].size+=1
					par = positions[i][0].parent
					while( par != None ):
						par.size+=1
						par = par.parent
					positions[i][0] = positions[i][0].right
				positions[i][0].counter+=1	
			else:
				b = positions[i][0]
				f = positions[i][1]
				if(ancestor(b, f)):
					S, pos, atom = l[0]
					f.left = Node(atom)
					f.left.parent = f
					f.size+=1
					par = f.parent
					while( par != None ):
						par.size+=1
						par = par.parent
					f = f.left
					for j in l[1:]:
						S, pos, atom = j
						f.right = Node(atom)
						f.right.parent = f
						f.size+=1
						par = f.parent
						while( par != None ):
							par.size+=1
							par = par.parent
						f = f.right
					f.counter+=1
				elif(ancestor(f, b)):
					for j in l:
						S, pos, atom = j
						b.right = Node(atom)
						b.right.parent = b
						b.size+=1
						par = b.parent
						while( par != None ):
							par.size+=1
							par = par.parent
						b = b.right
					b.counter+=1
				else:
					for j in l:
						S, pos, atom = j
						b.right = Node(atom)
						b.right.parent = b
						b.size+=1
						par = b.parent
						while( par != None ):
							par.size+=1
							par = par.parent
						b = b.right
					b.counter+=1					
	def insert(self, atom, insertPos, siteId):
		if(atom == ""):
			return -1
		# print "insert ", atom, insertPos, siteId,self.size
		child = None
		if(insertPos == 1):
			f = self.query(insertPos)
			f.left = Node(atom)
			child = f.left
			child.parent = f
			f.counter += 1
		elif(insertPos >= self.size):
			f = self.query(self.size)		
			f.right = Node(atom)
			child = f.right
			child.parent = f
			f.counter += 1
		else:
			b = None
			b = self.query(insertPos-1)
			f = self.query(insertPos)
			if(ancestor(b,f)):
				f.left = Node(atom)
				child = f.left
				child.parent = f
				f.counter+=1
			elif(ancestor(f,b)):
				b.right = Node(atom)
				child = b.right
				child.parent = b
				b.counter+=1
			else:
				b.right = Node(atom)
				child = b.right
				child.parent = b
				b.counter+=1
		# print "child ", child.value		
		par = child.parent
		while( par != None):
			par.size+=1
			par = par.parent
		
	def delete(self, pos, siteId):
		node = self.query(pos)
		node.value = ""
		node.size -= 1
		par = node.parent
		while( par != None):
			par.size-=1
			par = par.parent

	def flatten(self):
		ans = [""]
		def util(node, ans):
			if(node.left != None):
				util(node.left, ans)
			ans[0]+=node.value
			if(node.right != None):
				util(node.right, ans)
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
				node.left = allocate(h-1)	
				node.right = allocate(h-1)
				return node
		def fill(node, atomsting, ptr):
			if(ptr == len(atomstring)):
				return
			else:
				if(node.left != None):
					fill(node.left, atomstring, ptr)
				node.value = atomstring[ptr[0]]
				ptr[0]+=1
				if(node.right != None):
					fill(node.right, atomstring, ptr)
		allocate(h)
		ptr = [0]
		fill(self, atomstring, ptr)

def main():
	crdt = Node("")
	crdt.insert("hi",1,1)
	crdt.insert("!",2,2)
	crdt.insert("how are you",3,1)
	crdt.insert("how are you ",3,2)
	crdt.delete(4,2)
	conccurentQueries = [["this assignment ", 3, 1],["was fun\n", 3, 2],[" this is khalid, ",2,1], [" this is khalid, ",2,2]]
	crdt.conccurentInsert(conccurentQueries)
	crdt.delete(3,2)
	crdt.delete(3,2)
	crdt.insert("\nBut not as easy\n", crdt.size,1)
	crdt.insert(", ",4, 1)
	crdt.insert("Since It has been a whlie\n",crdt.size, 2)
	crdt.insert("Since I coded in python\n",crdt.size, 1)
	s = crdt.flatten()
	print s
main()