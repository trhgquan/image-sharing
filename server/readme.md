Full documentation can be found [here](https://documenter.getpostman.com/view/18981203/UVRHiiVn)

You might want to install these softwares:
- sqlitebrowser - to view sqlite files.
```
sudo apt-get install sqlitebrowser
```

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

Stopping:

```
deactivate
```

2. Install required packages:

```
pip install -r requirements.txt
```

3. Setting up environment variables

```
export FLASK_APP=serverside
export FLASK_ENV=development
```

4. Run server.

```
flask run
```

or, a shortcut for those steps:

```
./run_server.sh
```

## Database creation
Repeat from Environment's step 1 to step 3, then type this to the terminal:

```
flask init-db
```
