import calendar
from datetime import datetime, timedelta

import pytest

from bothandlers.utils import (add_user_to_database, check_date, convert_date,
                               day_remaining, delete_user_from_database,
                               get_information_about_user, hour_remaining,
                               minute_remaining, month_remaining)

#Variables
telegram_user_id = 1111
wrong_telegram_user_id = 2222
wrong_format_telegram_user_id = 'sdsds'
first_name = 'Test_name'
last_name = 'Test_surname'
username = 'Test_nickname'
chat_id = 1111

user_in_database = {'telegram_user_id': telegram_user_id, 
                    'first_name': first_name, 
                    'last_name': last_name, 
                    'username': username, 
                    'chat_id': chat_id}


class TestBotHandlersCheckDate:
    def test_convert_date(self):
        """The conversion of time from a dictionary to datetime is tested.
        """
        date = {
                'date': datetime.strftime(datetime.now() + timedelta(days=1), '%d-%m-%Y'),
                'hours': datetime.now().hour,
                'minutes': datetime.now().minute}
        assert isinstance(convert_date(date), datetime)


    def test_convert_date_time(self):
        """Check the date conversion from the dictionary 
           to the list. The function should return the date 
           and time in the format datetime.        
        """
        date = {
                'date': datetime.strftime(datetime.now() + timedelta(days=1), '%d-%m-%Y'),
                'hours': datetime.now().hour,
                'minutes': datetime.now().minute}
        processed_date = (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0)
        assert convert_date(date) == processed_date
    
    
    def test_convert_error_date(self):
        """Check the error when converting dates from the dictionary 
           to the list. If an error occurs during conversion, 
           the function should return None.
        """
        date = {'date': 'TestTest', 
                 'hours': '15', 
                 'minutes': '35'}
        assert convert_date(date) == None


    def test_current_date(self):
        """Check the date in the future.
           If the date and time is in the future, 
           the function will return True.
        """
        date = (datetime.now() + timedelta(days=1)).replace(second=0, microsecond=0)
        assert check_date(date) == True


    def test_past_date(self):
        """Check the date in the past. If the date and 
           time is in the past, the function should return False.
        """
        date = (datetime.now() - timedelta(days=1)).replace(second=0, microsecond=0)
        assert check_date(date) == False
    

class TestBotHandlersWorkWithUser:
    @pytest.fixture
    def user_add_before(self):
        """The user is added before the start of the verification.
        """
        if add_user_to_database(telegram_user_id, first_name, last_name, username, chat_id):
            print("User for testing added")
        else:
            print("Error")


    @pytest.fixture
    def user_delete_before(self):
        """The user is deleted before the start of the verification.
        """
        if delete_user_from_database(telegram_user_id):
            print("User for testing deleted")
        else:
            print("Error")


    @pytest.yield_fixture
    def user_add_after(self):
        """The user is added after the verification.
        """
        yield
        if add_user_to_database(telegram_user_id, first_name, last_name, username, chat_id):
            print("User for testing added")
        else:
            print("Error")
   

    @pytest.yield_fixture
    def user_delete_after(self):
        """The user is deleted after the verification.
        """
        yield
        if delete_user_from_database(telegram_user_id):
            print("User for testing deleted")
        else:
            print("Error")


    def test_add_user_to_database(self, user_delete_after):
        """Testing adding a user to the database. 
           If the user is added without errors, the function returns True.
        """
        assert add_user_to_database(telegram_user_id, first_name, last_name, username, chat_id) == True


    def test_delete_user_from_database(self, user_add_before):
        """Testing deleting a user from the database. 
           If the user is deleted without errors, the function returns True.
        """
        assert delete_user_from_database(telegram_user_id) == True


    def test_check_user_in_database_good(self, user_add_before, user_delete_after):
        """Testing the user presence in the database. 
           If such a user is in the database, the function returns True.
        """
        assert get_information_about_user(telegram_user_id) == user_in_database

    
    def test_check_user_in_database_none(self):
        """Testing the user presence in the database. 
           If such a user is no in the database, the function returns None.
        """
        assert get_information_about_user(wrong_telegram_user_id) == None
    
    
    def test_check_user_in_database_bad_request(self):
        """Testing the user presence in the database. 
           If the error is in the format or username, 
           the function returns None.
        """
        assert get_information_about_user(wrong_format_telegram_user_id) == None


class TestBotHandlersTimeRemaining:
    def test_check_minutes_remaining(self):
        """The function should return the current minutes with the given 
           step when transmitting a dictionary containing the "date" field
           and date-today.
           In the current example, step 5.
           If the current time is 10:02, the function should return 5, 
           if the time is 11:28, then the function should return 30.
        """
        today_date = datetime.now()
        source_data = {'date': datetime.strftime(today_date, '%d-%m-%Y'),
                       'hours': datetime.now().hour}
        step = 5
        convert_minute = (((datetime.now().minute // step) + 1) * step)
        assert minute_remaining(source_data, step) == convert_minute
    
    
    def test_check_minutes_remaining_manual(self):
        """The function should return the current minutes with the given 
           step when transmitting a dictionary containing the 
           "day", "month", "year", "hours" field and date-today.
           In the current example, step 5.
           If the current time is 10:02, the function should return 5, 
           if the time is 11:28, then the function should return 30.
        """
        source_data = {'day': datetime.now().day,
                       'month': datetime.now().month,
                       'year': datetime.now().year,
                       'hours': datetime.now().hour}
        step = 5
        convert_minute = (((datetime.now().minute // step) + 1) * step) 
        assert minute_remaining(source_data, step) == convert_minute
    
    
    def test_check_minutes_remaining_tommorow(self):
        """The function should return 0 if tomorrow's date is passed.
        """
        source_data = {'day': (datetime.now() + timedelta(days=1)).day,
                       'month': datetime.now().month,
                       'year': datetime.now().year,
                       'hours': datetime.now().hour}
        assert minute_remaining(source_data, 5) == 0
    
    
    def test_check_minutes_remaining_error(self):
        """
        The function should return 0 if an error occurred during processing.
        """
        today_date = datetime.now()
        source_data = {'date': datetime.strftime(today_date, '%d-%M-%Y'),
                       'hours': datetime.now().hour}
        assert minute_remaining(source_data, 5) == 0
    
    def test_check_hours_remaining(self):
        """The function should return the current hour if today's date 
           is passed.
        """
        today_date = datetime.now()
        source_date = datetime.strftime(today_date, '%d-%m-%Y')
        convert_hour = datetime.now().hour
        assert hour_remaining(source_date) == convert_hour
    

    def test_check_hours_remaining_tommorow(self):
        """
        The function should return 0 if tomorrow's date is passed.
        """
        today_date = datetime.now() + timedelta(days=1)
        source_date = datetime.strftime(today_date, '%d-%m-%Y')
        assert hour_remaining(source_date) == 0
    
    
    def test_check_hours_remaining_tommorow_error(self):
        """
        The function should return 0 if an error occurred during processing.
        In the current example, the date transfer format 
        has been changed: '%d-%m-%Y' -> '%d-%M-%Y'
        """
        today_date = datetime.now()
        source_date = datetime.strftime(today_date, '%d-%M-%Y')
        assert hour_remaining(source_date) == 0
    

    def test_check_month_remaining(self):
        """The function returns the current month with the current 
           year transfer.
        """
        source_date = datetime.now().year
        convert_month = datetime.now().month
        assert month_remaining(source_date) == convert_month

    def test_check_month_remaining_next_year(self):
        """The function returns 1 with the next year transfer.
        """
        source_date = (datetime.now()+ timedelta(days=365)).year
        assert month_remaining(source_date) == 1

    
    def test_check_days_remaining(self):
        """The function returns the current date and the number 
           of days in the month if the current month is transmitted.
        """
        source_date = {'year': datetime.now().year,
                       'month': datetime.now().month}
        convert_date = {'start': datetime.now().day,
                        'end': calendar.monthrange(source_date['year'], source_date['month'])[1]}
        assert day_remaining(source_date) == convert_date 

    def test_check_days_remaining_error(self):
        """The function returns [1;31] if if an error occurred 
           during processing.
        """
        source_date = {'year': 'sdsdsd',
                       'month': datetime.now().month}
        convert_date = {'start': 1,
                        'end': 31}
        assert day_remaining(source_date) == convert_date 