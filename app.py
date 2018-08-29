import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, send
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mycrazyoldcodingsecret'
socketio = SocketIO(app)

SESSION_TYPE = 'filesystem'

app.config.from_object(__name__)
Session(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/leavegame', methods=['GET', 'POST'])
def leavegame():
    return ('Hello')
    
@app.route('/game', methods=['GET', 'POST'])
def game():
    return ('Hello')
    
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    return ('Hello')
    
@app.route('/answer', methods=['GET', 'POST'])
def answer():
    return ('Hello')
    
@app.route('/leaderboard')
def leaderboard():
    return ('Hello')





if __name__ == "__main__":
    socketio.run(app,host=os.getenv('IP'), port=int(os.getenv('PORT')))