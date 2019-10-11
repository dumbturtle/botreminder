
from datetime import datetime, timedelta


def check_date(date):
	today_date = datetime.today()
	try:
		date_for_check = datetime.strptime(date, "%d-%m-%Y %H:%M")
		if date_for_check > today_date:
			return True
		else:
			return 'False: date in paste'
	except ValueError as error:
		return 'Error:{}'.format(error)

if __name__ == "__main__":
	pass