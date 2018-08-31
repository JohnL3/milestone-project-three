import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, send
import json
from data.helper import get_question, set_up_new_user, id_type, check_answer, get_leaderboard, add_user_online, update_user_online, remove_user_online

my_users = {}
leader_board = []
online = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mycrazyoldcodingsecret'
socketio = SocketIO(app)

SESSION_TYPE = 'filesystem'

app.config.from_object(__name__)
Session(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    session.permanent = True
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
    global leader_board
    if 'username' in session:
        user = session.get('username')
        my_users[user]['game-over'] = True
        leader_board = get_leaderboard(my_users, leader_board)
        
        return redirect(url_for('index'))
    
    
@app.route('/game', methods=['GET', 'POST'])
def game():
    global online
    global leader_board
    
    idType = id_type()
    
    if 'username' in session:
        user = session.get('username')
        print('user in session', user)
        if user in my_users:
            print('user in my_users', user)
            del my_users[user]['username']
            my_users[user] = set_up_new_user(user)
            
            if not user in online:
                print('user not in online', user)
                online = add_user_online(my_users, user, online)
            else:
                print('user in online',user)
                online = remove_user_online(user,online)
                online = add_user_online(my_users,user,online)
            
            leader_board = get_leaderboard(my_users, leader_board)
            print('leader_board',leader_board)
            
            socketio.emit('in_out_game', {'data': online})
            
            return render_template('game.html', username=user, type_id = idType, on_line = online, leader = leader_board)
        else:
            print('user not in my_users adding him',user)
            user = session.get('username')
            my_users[user] = set_up_new_user(user)
            print('my_users',my_users)
            if not user in online:
                print('user not in online addding',user)
                online = add_user_online(my_users, user, online)
                print('ONLINE',online)
            else:
                print('user in online',user)
                online = remove_user_online(user,online)
                online = add_user_online(my_users,user,online)
                print('ONLINE',online)
            print('leader_board',leader_board)
            leader_board = get_leaderboard(my_users, leader_board)
            
            socketio.emit('in_out_game', {'data': online})
            
            return render_template('game.html',username=user, type_id = idType, on_line = online, leader = leader_board)
    else:
        return redirect(url_for('index'))
        
    
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    '''
    Checking if request is a post else send them to home page as they shouldnt
    be typing web address + /questions into browser
    '''
    if request.method == 'POST':
        data = request.get_json()
        '''
        As im using permanent sessions and memory only storage and heroku sleeps
        Its possible for a user to get here
        
        if 'username' in session:
            if session.get('username') not in my_users:
                user = session.get('username')
                my_users[user] = set_up_new_user(user)
        '''
        
        my_quest = get_question(data['quest_id'])
        
        my_users[session.get('username')]['answered'].append(data['quest_id'])
        
        return jsonify(my_quest)
    else:
        return redirect(url_for('index'))
    
@app.route('/answer', methods=['GET', 'POST'])
def answer():
    global online
    global leader_board
    '''
    Checking if request is a post else send them to home page as they shouldnt
    be typing web address + /answer into browser
    '''
    
    if request.method == 'POST':
        data = request.get_json()
        user = session.get('username')
        result = check_answer(data['questionId'],data['answer'])
       
        if result[0]['result'] == 'correct':
            online = update_user_online(user, online)
            my_users[session.get('username')]['score'] = my_users[session.get('username')]['score']+1
        else:
            my_users[user]['wrong'].append([result[0]['id'],result[0]['answer']])
            
        socketio.emit('in_out_game', {'data': online})
        score = my_users[user]['score']
        socketio.emit('my_score',{'score': score,'user':user})
        
        answered_count = len(my_users[user]['answered'])  
        if answered_count == 2:
            my_users[user]['game-over'] = True
            
            data = {'msg': result,'game-over': True}
            return jsonify(data)
        else:
            data = {'msg': result}
            return jsonify(data)
    else:
        return redirect(url_for('index'))
   
    
@app.route('/leaderboard')
def leaderboard():
    global leader_board
    if 'username' in session:
        print('USERNAME',session.get('username'))
        user = session.get('username')
        my_users[user]['game-over'] = True
        leader_board = get_leaderboard(my_users, leader_board)
        print('Leaderboard',leader_board)
        
        return render_template('leaderboard.html', leaders=leader_board)
    else:
        leader_board = get_leaderboard(my_users, leader_board)
        return render_template('leaderboard.html', leaders=leader_board)


@socketio.on('message')
def handleMessage(msg):
    socketio.emit('message', {'data': msg}, broadcast=True)

@socketio.on('exitgame')
def exitgame(user):
    global online
    if user in online:
        online = remove_user_online(user, online)
        socketio.emit('in_out_game', {'data': online})


if __name__ == "__main__":
    socketio.run(app,host=os.getenv('IP'), port=int(os.getenv('PORT')))