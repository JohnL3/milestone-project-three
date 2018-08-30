from data.questions_answers import my_q_a
import operator

'''
id_type function returns all the keys and the value of type field in questions_answers file
this data is then passed and used in game.html file ... key as a id for question div and type as a text discription describing
what subject the question is based on eg javascript 
'''
def id_type():
    id_Type = []
    for key in my_q_a:
       id_Type.append([key, my_q_a[key]['type']])
       
    return id_Type

'''
The function get_question is used to return a question when user clicks a panel on the game page. When panel is clicked a id which
is a key in the questions_answers file is sent to backend and this is used then to display the question. Also other information is
filtered out before being sent back.
'''
def get_question(id):
    q = {}
    q_a = my_q_a[id]
    for key in q_a:
        if key != 'answer' and key != 'type':
            q[key] = q_a[key]
            
    return q
    
'''
The check_answer function is used to compare the the answer to a question sent back to backend with the actual answer
in the quest_answer file.
'''
def check_answer(id, answer):
    quest_answer = my_q_a[id]['answer']
    
    quest_answer = [item.lower() for item in quest_answer]
    ans = [item.lower() for item in answer]
    
    if len(ans) == len(quest_answer):
        if set(ans) == set(quest_answer):
            return [{'id':id,'result': 'correct'}]
        else:
            return [{'id': id,'result':'You answered wrong','answer': answer}]
    else:
        return [{'id': id,'result':'You answered wrong', 'answer': answer}]
    

'''
This function is used to set up details on each user
and add them to a dictionary of all users
So I can store which question he has answered
and which question he has got wrong.
and scores.
'''
def set_up_new_user(name):
    update_my_users = {}
    update_my_users['username'] = name
    update_my_users['answered'] = []
    update_my_users['wrong'] = []
    update_my_users['score'] = 0
    update_my_users['game-over'] = False
    return update_my_users

'''
The get_leaderboard function is used to store all users who make it on to the leaderboard, it also sorts them from highest score
to lowest score. passes them through a set to remove duplicate username and score eg if tom played twice and scored 4 twice i only want
to see username tom score 4 once .. if tom played again and got a score of 3 tom would then appear twice as score is different
'''
def get_leaderboard(all_users, leaderboard):
    '''Return allusers with a score > 0'''
    l = []
    if len(leaderboard) > 0:
        l = leaderboard
        for user,score in all_users.items():
            if score['score'] != 0 and score['game-over'] == True:
                r =(user,score['score'])
                l.append(r)
        l = list(set(l))
        l.sort(key = operator.itemgetter(1), reverse = True)
        
    else:
        for user,score in all_users.items():
            if score['score'] != 0:
                r =(user,score['score'])
                l.append(r)
        
    l.sort(key = operator.itemgetter(1), reverse = True)
   
    return l

'''
The add_user_online function is to create a dict of users online on game page, so i can show what users are online playing the game.The
opposed to all users which stores all users in game or not.
'''
def add_user_online(all_users,user, all_online):
        
    add_user = {}
    add_user['username'] = all_users[user]['username']
    add_user['score'] = all_users[user]['score']
    
    all_online[user] = add_user
    return all_online

'''
The remove_user_online is used to remove user from online when he leaves the game page
'''
def remove_user_online(user, all_online):
   del all_online[user]

   return all_online
'''
The update_user_online is used to update users score if he is online ... so if user answers a question right this function is called
'''
def update_user_online(user, all_online):
    update = all_online[user]
    update['score'] = update['score']+1
    all_online[user] = update
    return all_online
        
