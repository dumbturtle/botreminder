import unittest
from datetime import datetime, timedelta

from bothandlers.utils import (convert_date, check_date, 
                               add_user_to_database, 
                               get_information_about_user, 
                               delete_user_from_database)


class BotHandlersTestCheckDate(unittest.TestCase):
    def test_convert_date(self):
        date = {}
        date['date'] = datetime.strftime(datetime.now() + timedelta(days=1), '%d-%m-%Y')
        date['hours'] = datetime.now().hour
        date['minutes'] = datetime.now().minute
        self.assertIsInstance(convert_date(date), datetime)

    def test_current_date(self):
        date = (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0)
        self.assertEqual(check_date(date), True)

    def test_past_date(self):
        date = (datetime.now() - timedelta(days=1)).replace(second=0, microsecond=0)
        self.assertFalse(check_date(date), False)
    
    def test_convert_error_date(self):
        date = {'date': 'TestTest', 'hours': '15', 'minutes': '35'}
        self.assertEqual(convert_date(date), None)


class BotHandlersTestAddUserToDatabase(unittest.TestCase):
   
    @classmethod
    def setUpClass(cls):
        if delete_user_from_database(1111):
            print("User for testing deleted")
    
    @classmethod
    def tearDownClass(cls):
        print(get_information_about_user(1111))
        if delete_user_from_database(1111):
            print("User for testing is delete")
        else:
            print("Error")
    
    def test_add_user_to_database(self):
        self.assertTrue(add_user_to_database(1111,'Test_name', 'Test_surname', 'Test_nickname', 1111))


class BotHandlersTestDeleteUserFromDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if add_user_to_database(1111,'Test_name', 'Test_surname', 'Test_nickname', 1111):
            print("User for testing  added")
   
    @classmethod
    def tearDownClass(cls):
        if get_information_about_user(1111) is None:
            print("User for testing deleted")
    
    def test_delete_user_from_database(self):
        self.assertTrue(delete_user_from_database(1111))


class BotHandlersTestCheckUserInDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if add_user_to_database(1111,'Test_name', 'Test_surname', 'Test_nickname', 1111):
            print("User for testing added")
    
    @classmethod
    def tearDownClass(cls):
       if delete_user_from_database(1111):
            print("User for testing deleted")
    
    def test_check_user_in_database_good(self):
        self.assertTrue(get_information_about_user(1111))

    def test_check_user_in_database_none(self):
        self.assertIsNone(get_information_about_user(2222))
    
    def test_check_user_in_database_bad_request(self):
        self.assertIsNone(get_information_about_user('dsfsdfs'))

       
if __name__ == '__main__':
    unittest.main()
