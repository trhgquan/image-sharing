# Server-side installation
## Environment
1. Create venv:
```
python3 venv venv
```

Running:
```
. venv/bin/activate
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Run server
```
export FLASK_APP=serverside
export FLASK_ENV=development
flask run
```

or,

```
./run_server.sh
```

## Database creation
```
flask init-db
```
