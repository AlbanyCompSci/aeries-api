# README
New incarnation of an Aeries API (to go along with the districts new version of Aeries). Currently, only finds gradebook. Run by executing Main.py with email and password in file MyLoginData in the form

email\n
password

can also be generated with ./setLoginData.sh


## Todo
- **clean up code**
- check for edge case bugs
- decide on how to deal with blank fields (None/null type, '' string, 'blank' string etc.)

## Wishlist
- generalized parsing
	- give the parser a model (like a regex statement) with defined variable names
	- parser outputs dictionary with variable names from model
