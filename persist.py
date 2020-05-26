import psycopg2
def persist(data):
	deleted = data[0]
	nondeleted = data[1]
	with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
	    with conn.cursor() as cur:
	        conn.autocommit = True   
	        cur.execute(
	        	"CREATE TABLE IF NOT EXISTS treedoc( UID VARCHAR(10000) PRIMARY KEY,atom_value VARCHAR (255) NOT NULL);"
	        	)
	        for i in deleted:
	        	atomid = i
	        	cmd = "DELETE FROM treedoc WHERE uid = '" + str(atomid)+"';"
	        	cur.execute(cmd) 
	        for i in nondeleted:
		        atomid, atomvalue = i
		        cmd = "SELECT * FROM treedoc WHERE treedoc.UID = '"+str(atomid)+"';"
		        cur.execute(cmd)
		        res = cur.fetchall()
		        if(len(res) > 0):
		        	continue
		        cmd = "INSERT INTO treedoc (UID, atom_value) VALUES ('"+str(atomid)+"', '"+str(atomvalue)+"');"
		        print cmd
	     	        cur.execute(cmd)
def retrieve():
	with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
	    with conn.cursor() as cur:
	        conn.autocommit = True   
	        cur.execute("SELECT * FROM treedoc;")
	      	records = cur.fetchall()
	      	uids = []
	      	values = []
	      	for i in records:
	      		uids.append(i[0])
	      		values.append(i[1])
	      	return uids, values

persist((['1', '10', '100', '11', '110'], [['100121', 'how are you'], ['11101', 'hi']]))
