import psycopg2
from treedoc import *
class CRDT():
	def __init__(self):
		self.treedoc = Node("")
		self.queryList = []
		self.queryNumber = 0
		self.latestQueryNumber = 0
		with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
		    with conn.cursor() as cur:
		        conn.autocommit = True   
		        cmd = "CREATE TABLE IF NOT EXISTS delete_query_db ( id integer PRIMARY KEY,timestamp TIMESTAMP NOT NULL,"
		        cmd+="type VARCHAR(10), pos integer, siteid integer);"
		        cur.execute(cmd)
		        cmd = "CREATE TABLE IF NOT EXISTS insert_query_db ( id integer PRIMARY KEY,timestamp TIMESTAMP NOT NULL,"
		        cmd+="type VARCHAR(10), atom  VARCHAR(255), pos integer, siteid integer);"
		        cur.execute(cmd)

	def insert(self, atom, pos, siteid, timestamp):
		self.queryNumber+=1
		self.queryList.append([timestamp, "insert", [atom, pos, siteid]])
		with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
		    with conn.cursor() as cur:
		        conn.autocommit = True   
			cmd = "INSERT INTO insert_query_db (id, timestamp, type, atom, pos, siteid) VALUES ("+str(self.queryNumber)+", '"
			cmd+= str(timestamp)+"', "+"'insert', '"+str(atom)+"', "+str(pos)+", "+str(siteid)+");" 
			cur.execute(cmd)
	def delete(self, pos, siteid, timestamp):
		self.queryNumber+=1
		self.queryList.append([timestamp, "delete", [pos, siteid]])
		with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
		    with conn.cursor() as cur:
		        conn.autocommit = True   
			cmd = "INSERT INTO delete_query_db (id, timestamp, type, pos, siteid) VALUES ("+str(self.queryNumber)+", '"
			cmd+=str(timestamp)+"', "+"'delete', "+str(pos)+", "+str(siteid)+");" 
			cur.execute(cmd)
	def getdocument(self):
		self.queryDict = dict()
		self.queryList = []
		with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
		    with conn.cursor() as cur:
		        conn.autocommit = True   
			cmd = "SELECT * FROM insert_query_db WHERE id >"+str(self.latestQueryNumber)+";"
			cur.execute(cmd)
			l = cur.fetchall()
			for i in l:
				tblid, timestamp, typ, atom, pos, siteid = i
				self.queryList.append([timestamp, typ, [atom, pos, siteid]])		
			cmd = "SELECT * FROM delete_query_db;"
			cur.execute(cmd)
			l1 = cur.fetchall()
			for i in l1:
				tblid, timestamp, typ, pos, siteid = i
				self.queryList.append([timestamp, typ, [pos, siteid]])	
			self.queryList.sort()
		for i in self.queryList:
			self.queryDict[i[0]] = dict()
			self.queryDict[i[0]]["insert"]=[]
			self.queryDict[i[0]]["delete"]=[]
		for i in self.queryList:
			self.queryDict[i[0]][i[1]].append(i[2])	
		for ii in self.queryList:
			i = ii[0]
			q = [self.queryDict[i]["insert"],self.queryDict[i]["delete"]]
			self.treedoc.conccurentOperations(q[0], q[1])	
		
		self.latestQueryNumber = self.queryNumber
		return self.treedoc.flatten()		
			
if __name__ == "__main__":
        crdt = CRDT()	
        crdt.insert("a", 1, 1, '2011-05-16 15:36:38')		
        crdt.insert("b", 1, 2, '2011-05-16 15:36:38')
        crdt.insert("c", 1, 1, '2011-05-16 15:37:38')		
        crdt.insert("d", 1, 2, '2011-05-16 15:37:38')		
        crdt.delete( 1, 2, '2011-05-16 15:37:38')		
        crdt.delete( 2, 2, '2011-05-16 15:39:38')		
        print crdt.getdocument()
