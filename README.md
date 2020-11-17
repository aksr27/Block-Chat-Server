#in cmd for localhost

1) set FLASK_APP=node_server.py
2) flask run --port 8000

#in another cmd

1) python run_app.py

#for online sharing

1) ngrok.exe http 5000


****************************************************************************************************************************
# python_blockchain_app
Start a blockchain node server,

```sh
# Windows users can follow this: https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery
$ set FLASK_APP=node_server.py
$ flask run --port 8000
```

One instance of our blockchain node is now up and running at port 8000.


Run the application on a different terminal session,

```sh
$ python run_app.py
```

The application should be up and running at [http://localhost:5000](http://localhost:5000).

Here are a few screenshots

1. Posting some content

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/1.png)

2. Requesting the node to mine

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/2.png)

3. Resyncing with the chain for updated data

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/3.png)
