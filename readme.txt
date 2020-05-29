This is a simple program to simulate the working of collaborative text edtior.
-> File treedoc.py consists of the implementation of the treedoc CRDT.
-> File util.py consists of util functions that other classes use.
-> File persist.py consists of functions to persist the data in postgres
-> File app.py consists the CRDT type using which you can answer queries for insert, delete, getdocument.

How to test the program:

-> You have to provide your queries in the main function of app.py.
-> Insert Queries look like (atom, positionToBeInserted, siteId, timestamp).
-> Delete Queries look like (positionToBeInserted, siteId, timestamp).
-> Use getdocument function in CRDT class to get the document as a string.
-> Use saveDocument function in CRDT class to save the treedoc in the database.
-> Use retrieveDocument function in CRDT class to retrieve treedoc from the database.
-> The command to run the program is: 
		$sudo -u postgres app.py.


