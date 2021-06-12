# Requests


## Group
```
curl --location --request POST 'http://127.0.0.1:8000/ledger/group/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "group1"
}'
```
## User
```
curl --location --request POST 'http://127.0.0.1:8000/ledger/user/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "demouser"
}'
```
## Event:

### create:
```
curl --location --request POST 'http://127.0.0.1:8000/ledger/event/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"user": [{
		"id": 1,
		"amount": 2000,
	    "Percent": 0
	}, {
		"id": 2,
		"amount": 100,
	    "percent": 50
	}, {
		"id": 3,
		"amount": 0,
	  	"percent": 50
	}],
	"name": "groceries",
	"type": "percent",
	"group": 6
}'
```
### get: 
```
curl --location --request GET 'http://127.0.0.1:8000/ledger/event/'
```
### delete:
```
curl --location --request DELETE 'http://127.0.0.1:8000/ledger/event/46/'
```
## Transaction:
```
curl --location --request GET 'http://127.0.0.1:8000/ledger/transactions/?user=3'
```
## Summary:
```
curl --location --request GET 'http://127.0.0.1:8000/ledger/summary/?group=6'
```
## Settlement:
```
curl --location --request GET 'http://127.0.0.1:8000/ledger/settle/?lender=1&borrower=3&amount=500&group=6'
```

