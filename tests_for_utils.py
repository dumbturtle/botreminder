import unittest
import calendar
from datetime import datetime, timedelta

from bothandlers.utils import (add_user_to_database, check_date, convert_date,
                               delete_user_from_database,
                               get_information_about_user, minute_remaining,
                               hour_remaining, month_remaining, day_remaining)


class BotHandlersTestCheckDate(unittest.TestCase):
    def test_convert_date(self):
        date = {
            'date': datetime.strftime(datetime.now() + timedelta(days=1), '%d-%m-%Y'),
            'hours': datetime.now().hour,
            'minutes': datetime.now().minute}
        self.assertIsInstance(convert_date(date), datetime)


    def test_current_date(self):
        date = (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0)
        self.assertEqual(check_date(date), True)


    def test_past_date(self):
        date = (datetime.now() - timedelta(days=1)).replace(second=0, microsecond=0)
        self.assertFalse(check_date(date), False)
    

    def test_convert_error_date(self):
        date = {'date': 'TestTest', 
                'hours': '15', 
                'minutes': '35'}
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

class BotHandlersTestTimeRemaining(unittest.TestCase):
    def test_check_minutes_remaining(self):
        today_date = datetime.now()
        source_data = {'date': datetime.strftime(today_date, '%d-%m-%Y'),
                       'hours': datetime.now().hour}
        step = 5
        convert_minute = (((datetime.now().minute // step) + 1) * step)
        self.assertEqual(minute_remaining(source_data, step), convert_minute)
    
    
    def test_check_minutes_remaining_manual(self):
        source_data = {'day': datetime.now().day,
                       'month': datetime.now().month,
                       'year': datetime.now().year,
                       'hours': datetime.now().hour}
        step = 5
        convert_minute = (((datetime.now().minute // step) + 1) * step) 
        self.assertEqual(minute_remaining(source_data, step), convert_minute)
    
    
    def test_check_minutes_remaining_tommorow(self):
        source_data = {'day': (datetime.now() + timedelta(days=1)).day,
                       'month': datetime.now().month,
                       'year': datetime.now().year,
                       'hours': datetime.now().hour}
        self.assertEqual(minute_remaining(source_data, 5), 0)
    
    
    def test_check_minutes_remaining_error(self):
        today_date = datetime.now()
        source_data = {'date': datetime.strftime(today_date, '%d-%M-%Y'),
                       'hours': datetime.now().hour}
        self.assertEqual(minute_remaining(source_data, 5), 0)
    
    def test_check_hours_remaining(self):
        today_date = datetime.now()
        source_date = datetime.strftime(today_date, '%d-%m-%Y')
        convert_hour = datetime.now().hour
        self.assertEqual(hour_remaining(source_date), convert_hour)
    

    def test_check_hours_remaining_tommorow(self):
        today_date = datetime.now() + timedelta(days=1)
        source_date = datetime.strftime(today_date, '%d-%m-%Y')
        self.assertEqual(hour_remaining(source_date), 0)
    
    
    def test_check_hours_remaining_tommorow(self):
        today_date = datetime.now()
        source_date = datetime.strftime(today_date, '%d-%M-%Y')
        self.assertEqual(hour_remaining(source_date), 0)
    

    def test_check_hours_remaining_tommorow(self):
        source_date = datetime.now().year
        convert_month = datetime.now().month
        self.assertEqual(month_remaining(source_date), convert_month)
    
    
    def test_check_days_remaining(self):
        source_date = {'year': datetime.now().year,
                       'month': datetime.now().month}
        convert_date = {'start': datetime.now().day,
                        'end': calendar.monthrange(source_date['year'], source_date['month'])[1]}
        self.assertEqual(day_remaining(source_date), convert_date)


if __name__ == '__main__':
    unittest.main()
