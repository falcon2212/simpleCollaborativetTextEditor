from math import *
from copy import *
from persist import persist, retrieve
from util import dfs, ancestor


class Node():
	def __init__(self, data, root1 = True):
		self.value = data
		self.left = None 						#stores left child
		self.right = None						#stores left child
		self.size = 1							#stores size of the subtree rooted here
		self.parent = None						#stores parent node
		self.la = self							#stores left desendent whose left child's uid is immediatley smaller to this node's uid
		self.ra = self							#stores right desendent whose right child's uid is immediatley greater to this node's uid
		self.root = False						#stores if the current node is root of treedoc or not
		if(data == ""):
			self.root = root1
	def query(self, n, node):
		if(node.size == 0):
			return node
		if(n > node.size):
			return None
		sizel = 0
		sizer = 0
		sizen = 1
		if(node.value == "" and not node.root):
			sizen-=1
		if(node.left != None):
			sizel = node.left.size
		if(node.right != None):
			sizer = node.right.size			
		if(sizen == 0):
			if(sizel >= n):
				return self.query(n, node.left)
			else:
				return self.query(n-sizel, node.right)	
		if(sizel + 1 == n):
			ra = node
			if(ra.right == None):
				ra = node
			else:	
				ra = ra.right
				while(ra.right != None and ra.right.value == ""):
					ra = ra.right
			if(ra.right != None and ra.right.value != ""):
				ra = None
			la = node
			if(la.left == None):
				la = node
			else:
				la = la.left
				while(la.left != None and la.left.value == ""):
					la = la.left
			if(la.left != None and la.left.value != ""):
				la = None		
			node.ra = ra
			node.la = la
			return node
		elif(sizel + 1 < n):
			return self.query(n-sizel-1, node.right)
		else:
			return self.query(n, node.left)
					
	def conccurentOperations(self, insertQueries, deleteQueries):
		d1 = dict()
		for i in deleteQueries:
			pos, siteId = i
			pos+=1
			d1[pos]=[]
		positions1 = dict()
		for i in deleteQueries:
			pos, siteId = i
			pos+=1
			d1[pos].append(i)
			positions1[pos] = self.query(pos, self)

		d = dict()
		for i in insertQueries:
			atom, pos, siteId = i
			d[pos]=[]
		positions = dict()
		for i in insertQueries:
			atom, pos, siteId = i
			d[pos].append(i)
			if(pos == self.size):
				positions[pos] = [self.query(pos, self)]
			else:
				positions[pos] = [self.query(pos, self),self.query(pos+1, self)]	
		prevSize = self.size

		#DELETE
		for i in positions1:
			if(self.size == 0):
				break
			node = positions1[i]
			node.value = ""
			if(not node.root):
				node.size -= 1
			par = node.parent
			while( par != None ):
				par.size-=1
				par = par.parent

		#INSERT		
		for i in d:
			l = []
			for j in d[i]:
				atom, pos, S = j
				l.append((S, pos, atom))
			l.sort()
			if(i == prevSize):
				b = positions[i][0].ra
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
			else:
				b = positions[i][0]
				f = positions[i][1]
				if(ancestor(b, f)):
					ff = f.la
					S, pos, atom = l[0]
					ff.left = Node(atom)
					ff.left.parent = ff
					ff.size+=1
					par = ff.parent
					while( par != None ):
						par.size+=1
						par = par.parent
					ff = ff.left
					ff = ff.ra
					for j in l[1:]:
						S, pos, atom = j
						ff.right = Node(atom)
						ff.right.parent = ff
						ff.size+=1
						par = ff.parent
						while( par != None ):
							par.size+=1
							par = par.parent
						ff= ff.right
				else:
					bb = b.ra
					for j in l:
						S, pos, atom = j
						bb.right = Node(atom)
						bb.right.parent = bb
						bb.size+=1
						par = bb.parent
						while( par != None ):
							par.size+=1
							par = par.parent
						bb = bb.right
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
				node = Node("", False)
				node.left = allocate(h-1)
				node.left.parent = node	
				node.right = allocate(h-1)
				node.right.parent = node	
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
		self = allocate(h)
		ptr = [0]
		fill(self, atomstring, ptr)
		dfs(self)

#This function returns the uids of deleted and uids,values of undeleted nodes
def getDataFromCRDT(crdt):
	deleted = []
	nondeleted = []
	uid = ""
	def util(node, uid):
		if(node.value == "" and not node.root):
			deleted.append(uid)
		elif(node.value != ""):
			nondeleted.append([uid, node.value])	
		if(node.left != None):
			util(node.left, uid+"0")
		if(node.right != None):
			util(node.right, uid+"1")		
	util(crdt, uid)
	return (deleted, nondeleted) 		

#This function reconstructs the treedoc from uids, atomvalues
def reconstruct(atomIds, atomValues):
	root = Node("")
	for i in range(len(atomIds)):
		atomid = atomIds[i]
		atomvalue = atomValues[i]
		par = root
		j = 0
		while j < len(atomid)-1 :
			if(atomid[j] == '0'):
				if(par.left == None):
					par.left = Node("", False)
					par.left.parent = par
				par = par.left
			else:
				if(par.right == None):
					par.right = Node("",False)
					par.right.parent = par
				par = par.right
			j+=1
		if(j < len(atomid)):
			if(atomid[j] == '0'):
				if(par.left != None):
					par.left.value = atomvalue
				else:
					par.left = Node(atomvalue)
					par.left.parent = par
			else:
				if(par.right != None):
					par.right.value = atomvalue
				else:
					par.right = Node(atomvalue)
					par.right.parent = par
	return root			
