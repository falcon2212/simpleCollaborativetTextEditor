from math import *
from copy import *
from persist import persist, retrieve
from util import dfs, ancestor
# from flask import Flask, request
# from flask_restful import Resource, Api
# app = Flask(__name__)
# api = Api(app)


class Node():
	def __init__(self, data):
		self.value = data
		self.left = None
		self.right = None
		self.counter = 0
		self.size = 1
		self.parent = None
		self.la = self
		self.ra = self
		if(data == ""):
			self.size = 0

	#returns node corresponding to the character at nth position in crdt	
	def query(self, n):
		if(self.size == 0):
			return self
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
		ra = ans[0]
		if(ra.right == None):
			ra = ans[0]
		else:
			ra = ra.right
			while(ra.left != None):
				ra = ra.left
		la = ans[0]
		if(la.left == None):
			la = ans[0]
		else:
			la = la.left
			while(la.right != None):
				la = la.right
		ans[0].ra = ra
		ans[0].la = la
		return ans[0]

					
	def conccurentInsert(self, queries):
		d = dict()
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
			cnt = 0;
			if(i == 1):
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
				b.counter+=1	
			elif(i == prevSize):
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
				b.counter+=1	
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
					ff.counter+=1	
				elif(ancestor(f, b)):
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
					bb.counter+=1
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
					bb.counter+=1					
	def insert(self, atom, insertPos, siteId):
		if(atom == ""):
			return -1
		child = None
		if(insertPos == 1):
			f = self.query(insertPos)
			f = f.la
			f.left = Node(atom)
			child = f.left
			child.parent = f
			f.counter += 1
		elif(insertPos >= self.size):
			f = self.query(self.size)		
			f = f.ra
			f.right = Node(atom)
			child = f.right
			child.parent = f
			f.counter += 1
		else:
			b = None
			b = self.query(insertPos-1)
			f = self.query(insertPos)
			if(ancestor(b,f)):
				f = f.la
				f.left = Node(atom)
				child = f.left
				child.parent = f
				f.counter+=1
			elif(ancestor(f,b)):
				b = b.ra
				b.right = Node(atom)
				child = b.right
				child.parent = b
				b.counter+=1
			else:
				b = b.ra
				b.right = Node(atom)
				child = b.right
				child.parent = b
				b.counter+=1
		par = child.parent
		while( par != None):
			par.size+=1
			par = par.parent
		
	def delete(self, pos, siteId):

		node = self.query(pos)
		node.value = ""
		node.size -= 1
		par = node.parent
		while( par != None ):
			par.size-=1
			par = par.parent

	def conccurentDeletes(self, queries):
		d = dict()
		for i in queries:
			pos, siteId = i
			d[pos]=[]
		positions = dict()
		for i in queries:
			pos, siteId = i
			d[pos].append(i)
			positions[pos] = self.query(pos)
		for i in positions:
			node = positions[i]
			node.value = ""
			node.size -= 1
			par = node.parent
			while( par != None ):
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

def getDataFromCRDT(crdt):
	deleted = []
	nondeleted = []
	uid = ""
	def util(node, uid):
		if(node.value == "" and len(uid) > 0):
			deleted.append(uid)
		elif(node.value != ""):
			nondeleted.append([uid, node.value])	
		if(node.left != None):
			util(node.left, uid+"0")
		if(node.right != None):
			util(node.right, uid+"1")		
	util(crdt, uid)
	return (deleted, nondeleted) 		

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
					par.left = Node("")
					par.left.parent = par
				par = par.left
			else:
				if(par.right == None):
					par.right = Node("")
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

'''

These are the things left to do :

create a wraper function to process queries 
use flask to make an rest api

'''
def main():
	crdt = Node("")
	crdt.insert("hi",1,1)
	crdt.insert("!",2,2)
	crdt.insert("how are you",3,1)
	crdt.insert("how are you ",3,2)
	crdt.delete(4,2)
	conccurentQueries = [["this assignment ", 3, 1],["was fun\n", 3, 2],[" this is khalid, ",2,1], [" this is khalid, ",2,2]]
	crdt.conccurentInsert(conccurentQueries)
	conccurentQueries = [[3,2],[3,1],[4,1]]
	crdt.conccurentDeletes(conccurentQueries)
	# crdt.delete(3,2)
	# crdt.delete(3,2)
	crdt.insert("\nBut not as easy\n", crdt.size,1)
	crdt.insert(", ",4, 1)
	crdt.insert("Since It has been a whlie\n",crdt.size, 2)
	crdt.insert("Since I coded in python\n",crdt.size, 1)
	print crdt.flatten()
	ncrdt = reconstruct(['1101', '1001'], ['hi', 'how are you'])
	print ncrdt.flatten()
	print getDataFromCRDT(ncrdt)
	print retrieve()
main()