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
