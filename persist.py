import psycopg2

def persist(atomIds, atomValues):
	with psycopg2.connect(database="postgres", user="postgres", password="") as conn:
	    with conn.cursor() as cur:
	        conn.autocommit = True   
	        cur.execute("DROP TABLE IF EXISTS treedoc;")
	        cur.execute(
	        	"CREATE TABLE treedoc( UID VARCHAR(10000) PRIMARY KEY,atom_value VARCHAR (255) NOT NULL);"
	        	)
	        for i in range(len(atomIds)):
		        cmd = "INSERT INTO treedoc (UID, atom_value) VALUES ("
		        cmd += "'"+str(atomIds[i])+"', '"+str(atomValues[i])
		        cmd +="');"
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
		     	        
persist(["10011","101001"],["hi", "how are you"])
print retrieve()