import sys
sys.path.append('..')
import unittest
from data.helper import id_type #, set_up_new_user, get_question, check_answer, get_leaderboard, add_user_online, remove_user_online, update_user_online
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