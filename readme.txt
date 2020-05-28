This is a simple program to simulate the working of collaborative text edtior.
-> File treedoc.py consists of the implementation of the treedoc CRDT.
-> File util.py consists of util functions that other classes use.
-> File persist.py consists of functions to persist the data in postgres
-> File app.py consists the CRDT type using which you can answer queries for insert, delete, getdocument.

How to test the program:

$sudo -u postgres app.py

NOTE: If you want to run a fresh instance then you have to clear the data base first and then try to run the code.