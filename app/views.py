import datetime
import json

import requests
from flask import Flask, flash, redirect, render_template, request, session, abort
import mysql.connector

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="mailblock"
)

mycursor = mydb.cursor()

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)

        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)
@app.route('/')
def login(msg=""):
	if not session.get('logged_in'):
		return render_template('login.html',msg=msg)
	else:
		return index()


@app.route('/signup')
def signup(msg=""):
	return render_template('signup.html',msg=msg)

@app.route('/signup_save', methods=['POST'])
def signup_save():
	if request.form['email'] !=None and request.form['password'] !=None:
		email=request.form['email']
		password=request.form['password']

		mycursor.execute("INSERT INTO signup(Email,Password) values(%s,%s)",(email,password))
		mydb.commit()
		return signup()
	else:
		return signup(msg="Enter data correctly!")


@app.route('/login', methods=['POST'])
def do_admin_login():
  if request.form['username']=="admin" and request.form['password']=="mailblock":
    session['logged_in'] = True
    session['username']=request.form['username']
    return index()
  if request.form['username'] !=None and request.form['password'] !=None:
    mycursor.execute("SELECT * FROM signup")
    myresult = mycursor.fetchall()
    for x in myresult:
      user=x[1]
      passw=x[2]
      if(user==request.form['username'] and passw==request.form['password']):
        session['logged_in'] = True
        session['username']=request.form['username']
        return index()
    return login("Enter correct data!")
  else:
    return login("Enter all data!")

@app.route("/logout")
def logout():
	session['logged_in'] = False
	return login()

@app.route('/app')
def index():
	username = session.get('username')
	print(username)
	fetch_posts()
	return render_template('index.html',
                           posts=posts,
                           username=username,
                           node_address=CONNECTED_NODE_ADDRESS,
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    # Submit a transaction
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})

    return redirect('/app')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')
