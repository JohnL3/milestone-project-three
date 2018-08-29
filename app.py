import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, send
import json
from data.helper import id_type

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mycrazyoldcodingsecret'
socketio = SocketIO(app)

SESSION_TYPE = 'filesystem'

app.config.from_object(__name__)
Session(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    username = ''
    '''
    First if is so I can have username always in input box so person dosent have to try and remember
    username when the close browser and come back another time if they created one previously.
    And make sure a blank username is not being used by removing required field from input box
    '''
    if 'username' in session and session.get('username') != '':
        username = session.get('username')
        
    if request.method == 'POST':
        username = request.form['username']
        
        #In case anyone deletes required field from input and trys to enter without username
        #they stay on home page
        if username != '':
            if 'username' in session:
                if session.get('username') == username:
                    return redirect(url_for('game'))
            else:
                session['username'] = username
               
                return redirect(url_for('game'))
        else:
            return render_template('index.html')
            
    return render_template('index.html', username=username)

@app.route('/leavegame', methods=['GET', 'POST'])
def leavegame():
    return ('Hello')
    
@app.route('/game', methods=['GET', 'POST'])
def game():
    idType = id_type()
    return render_template('game.html', type_id = idType)
    
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