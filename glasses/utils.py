import datetime

def date_from_post(post_data):
  	return (
   		datetime.date(int(post_data['first_date_year']), int(post_data['first_date_month']), int(post_data['first_date_day'])),
   		datetime.date(int(post_data['last_date_year']), int(post_data['last_date_month']), int(post_data['last_date_day'])+1)
   	)