import sys
sys.path.append('..')
import unittest
from data.helper import id_type, set_up_new_user, get_question, check_answer, get_leaderboard, add_user_online, remove_user_online, update_user_online
from data.questions_answers import my_q_a

class test_get_id_and_type(unittest.TestCase):
    '''Test to ensure i get all question ids and question type'''
    
    def test_function_returns_list(self):
        '''Test function returns a list'''
        
        result = id_type()
        self.assertTrue(type(result) == list)
        
    def test_returned_list_contains_lists(self):
        '''Returned list should contain lists'''
        
        result = id_type()
        self.assertTrue(type(result[0]) == list)
        
    def test_length_of_list(self):
        '''Test length of list is equal to length of questions and answers in questions_answers file'''
        
        result = id_type()
        self.assertEqual(len(result), len(my_q_a))
        
    def test_inner_lists_length(self):
        '''Test list inside list has length of 2'''
        result = id_type()
        
        self.assertTrue(len(result[0]) == 2)
        
class Test_setup_users(unittest.TestCase):
    
    def test_returns_a_dictionary(self):
        '''Test is to ensure we return a dictionary'''
        
        user = 'John_L3'
        users = set_up_new_user(user)
        self.assertTrue(type(users) is dict)
        
    def test_it_sets_username_to_user(self):
        ''' Test to ensure user passed to function is the value for key username'''
        
        user = 'John_L3'
        users = set_up_new_user(user)
        self.assertEqual(users['username'],'John_L3')
        
    def test_returns_dict_length_4(self):
        '''Test to check the size of dict returned is 4'''
        
        user = 'John_L3'
        new_user = set_up_new_user(user)
        self.assertEqual(len(new_user),5)
        
    def test_has_key_answered_and_wrong_score(self):
        '''Test to see it has key answered and wrong score'''
        
        user = 'John_L3'
        new_user = set_up_new_user(user)
        
        self.assertIn('answered',new_user)
        self.assertIn('wrong',new_user)
        self.assertIn('score', new_user)
        self.assertIn('game-over', new_user)
        
    def test_key_answered_and_wrong_are_lists(self):
        '''Test to ensure key values answered and wrong are of type list'''
        
        user = 'John_L3'
        new_user = set_up_new_user(user)
        
        self.assertTrue(type(new_user['answered']) is list)
        self.assertTrue(type(new_user['wrong']) is list)
        
class Test_my_get_question(unittest.TestCase):
    
    def test_returns_a_dictionary(self):
        '''Test is to ensure we return a dictionary'''
        
        quest = get_question('0')
        
        self.assertTrue(type(quest) is dict)
        
    def test_keys_not_in_dict(self):
        '''Returned dict should not have keys answer and type'''
        
        quest = get_question('0')
            
        self.assertNotIn('answer',quest)
        self.assertNotIn('type',quest)
        
class Test_my_get_answer(unittest.TestCase):
    '''Tests to ensure my check_answer function works'''
    
    def test_id_passed_to_function(self):
        '''ensure id passed to function returns a list'''
        
        result = check_answer('0', ['Dictionary', 'List', 'Set', 'Tuple'])
        
        self.assertTrue(type(result) == list)
        
        
        
    def test_valid_return_for_correct_answer(self):
        '''Ensure a valid answer is not missed 
        if more than one part to answer, even if order or results is mixed'''
        
        result = check_answer('0', ['Tuple', 'List', 'Set', 'Dictionary'])
        
        self.assertEqual(result[0]['result'],'correct')
        
    def test_valid_return_for_incorrect_answer(self):
        '''Ensure a wrong answer if picked up'''
        
        result = check_answer('0', ['Tuple', 'Set', 'Dictionary']) 
        
        self.assertEqual(result[0]['result'],'You answered wrong')
        
        
    def test_valid_length_of_answer_but_wrong_answer(self):
        '''Ensure for multiple parts to answer if any are wrong it is picked up'''
        
        result = check_answer('0', ['Tuple', 'Set', 'Dictionary','array'])
        
        self.assertEqual(result[0]['result'],'You answered wrong')
    
    
    def test_for_wrong_answers_players_answers_are_returned(self):
        '''Wrong answers should return list containg players answer/s'''
        
        answer = ['Tuple', 'Set']
        result = check_answer('0', answer)
        
        
        self.assertEqual(answer, result[0]['answer'])
        
class Test_setup_leaderboard(unittest.TestCase):
    '''Tests for my leaderboard function'''
    
    def test_get_leaderboard_returns_list(self):
        '''Ensure get_leaderboard returns a list'''
        
        my_users = {
            'j':{'username':'j','ans':[],'wrong':[],'score':2},
            'e':{'username':'e','ans':[],'wrong':[],'score':5},
            'a':{'username':'a','ans':[],'wrong':[],'score':9},
            'b ':{'username':'b','ans':[],'wrong':[],'score':6},
            'c':{'username':'c','ans':[],'wrong':[],'score':2},
            'd':{'username':'d','ans':[],'wrong':[],'score':7}
        }
        leader_board = []
        result = get_leaderboard(my_users, leader_board)
        
        self.assertTrue(type(result) == list)
        
    def test_returns_list_length_greater_than_0(self):
        '''Should return a list of length of at least one if a user has played game and answered a question correctly'''
        
        my_users = {
            'j':{'username':'j','ans':[],'wrong':[],'score':1},
        }
        leader_board = []
        
        result = get_leaderboard(my_users, leader_board)
        
        self.assertEqual(1,len(result))
        
    def test_returns_list_length_0_if_no_one_answers_correctly(self):
        '''Should return an empty list if user/s played game and have answered no questions correctly'''
        
        my_users = {
            'j':{'username':'j','ans':[],'wrong':[],'score':0},
        }
        leader_board = []
        result = get_leaderboard(my_users, leader_board)
        
        self.assertEqual(0,len(result))
        
    
    def test_return_list_length(self):
        '''Should return a list of length 5 as 5 users score greater than 0'''
        
        my_users = {
            'j':{'username':'j','ans':[],'wrong':[],'score':2},
            'e':{'username':'e','ans':[],'wrong':[],'score':5},
            'a':{'username':'a','ans':[],'wrong':[],'score':9},
            'b ':{'username':'b','ans':[],'wrong':[],'score':6},
            'c':{'username':'c','ans':[],'wrong':[],'score':2},
            'd':{'username':'d','ans':[],'wrong':[],'score':0}
        }
        leader_board = []
        
        result = get_leaderboard(my_users, leader_board)
        
        self.assertEqual(5,len(result))
        
    def test_returns_usernames_score(self):
        '''Should return tuples with username and score and highest score/username pair should be first in list'''
        
        my_users = {
            'j':{'username':'j','ans':[],'wrong':[],'score':2},
            'e':{'username':'e','ans':[],'wrong':[],'score':5},
            'a':{'username':'a','ans':[],'wrong':[],'score':9},
            'b':{'username':'b','ans':[],'wrong':[],'score':6},
            'c':{'username':'c','ans':[],'wrong':[],'score':2},
            'd':{'username':'d','ans':[],'wrong':[],'score':7}
        }
        leader_board = []
        
        result = get_leaderboard(my_users, leader_board)
        
        self.assertEqual(9,result[0][1])
        self.assertEqual('a',result[0][0])
        self.assertTrue(type(result[0]) == tuple)
        
class test_add_user_online(unittest.TestCase):
    '''Test for adding user to online'''
    
    def test_return_dict_online_users(self):
        ''' Should return a dict for user in online dict'''
        
        online = {
            'john':{'username':'john','ans':[],'wrong':[],'score':2}
        }
        my_users = {
            'john':{'username':'john','ans':[],'wrong':[],'score':2},
            'emily':{'username':'emily','ans':[],'wrong':[],'score':0}
           
        }
        user = 'emily'
        online = add_user_online(my_users,user,online)
        
        self.assertTrue(type(online[user]) == dict)
        
    def test_should_add_to_online(self):
        ''' User should be added to the online dict'''
        
        online = {
            'john':{'username':'john','score':2}
        }
        my_users = {
            'john':{'username':'john','ans':[],'wrong':[],'score':2},
            'emily':{'username':'emily','ans':[],'wrong':[],'score':0}
           
        }
        user = 'emily'
        online = add_user_online(my_users,user,online)
        
        self.assertIn('emily',online)
        
class test_remove_user_online(unittest.TestCase):
    '''Test my remove_user_online function'''
    
    def test_i_can_remove_user(self):
        '''Should remove user from online dict'''
        
        online = {
            'emily':{'username':'emily','score':2}
        }
        user = 'emily'
        
        online = remove_user_online(user, online)
        
        self.assertNotIn('emily',online)
        
class test_update_user_online_function(unittest.TestCase):
    '''Test my update_user_online function'''
    
    def test_can_update_user_online(self):
        '''Test function updates score of user in online dict'''
        
        online = {
            'emily':{'username':'emily','score':0}
        }
        user = 'emily'
        
        online = update_user_online(user, online)
        
        self.assertEqual(online[user]['score'],1)
  