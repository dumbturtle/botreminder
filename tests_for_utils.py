import unittest
from datetime import datetime, timedelta

from bothandlers.utils import (add_user_to_database, check_date,
                               check_user_in_database,
                               delete_user_from_database)


class BotHandlersTestCheckDate(unittest.TestCase):
    def test_formate_date(self):
        date = {}
        date['date'] = datetime.strftime(datetime.now() + timedelta(days=1), '%d-%m-%Y')
        date['hours'] = datetime.now().hour
        date['minutes'] = datetime.now().minute
        self.assertIsInstance(check_date(date), datetime)

    def test_current_date(self):
        date = {}
        date['date'] = datetime.strftime(datetime.now() + timedelta(days=1), '%d-%m-%Y')
        date['hours'] = datetime.now().hour
        date['minutes'] = datetime.now().minute
        check_valid_date = (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0)
        self.assertEqual(check_date(date), check_valid_date)
    
    def test_past_date(self):
        date = {}
        date['date'] = datetime.strftime(datetime.now() - timedelta(days=1), '%d-%m-%Y')
        date['hours'] = datetime.now().hour
        date['minutes'] = datetime.now().minute
        self.assertFalse(check_date(date))
    
    def test_error_date(self):
        date = {'date': 'TestTest', 'hours': '15', 'minutes': '35'}
        function_result = "Error: time data 'TestTest 15:35' does not match format '%d-%m-%Y %H:%M'" 
        self.assertEqual(check_date(date), function_result)


class BotHandlersTestAddUserToDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if check_user_in_database(1111) is not None:
            delete_user_from_database(1111)
            print("User for testing deleted")
    
    @classmethod
    def tearDownClass(cls):
        if delete_user_from_database(1111):
            print("User for testing is delete")
        else:
            print("Error")
    
    def test_add_user_to_database(self):
        self.assertTrue(add_user_to_database(1111,'Test_name', 'Test_surname', 'Test_nickname', 1111))


class BotHandlersTestDeleteUserFromDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if check_user_in_database(1111) is None:
            add_user_to_database(1111,'Test_name', 'Test_surname', 'Test_nickname', 1111)
            print("User for testing  added")
    
    @classmethod
    def tearDownClass(cls):
        if check_user_in_database(1111) is not None:
            delete_user_from_database(1111)
            print("User for testing deleted")
    
    def test_delete_user_from_database(self):
        self.assertTrue(delete_user_from_database(1111))


class BotHandlersTestCheckUserInDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if check_user_in_database(1111) is None:
            add_user_to_database(1111,'Test_name', 'Test_surname', 'Test_nickname', 1111)
            print("User for testing added")
    
    @classmethod
    def tearDownClass(cls):
       if check_user_in_database(1111) is not None:
            delete_user_from_database(1111)
            print("User for testing deleted")
    
    def test_check_user_in_database_good(self):
        self.assertTrue(check_user_in_database(1111))

    def test_check_user_in_database_none(self):
        self.assertIsNone(check_user_in_database(2222))
    
    def test_check_user_in_database_bad_request(self):
        self.assertIsNone(check_user_in_database('dsfsdfs'))
    
       
if __name__ == '__main__':
    unittest.main()
