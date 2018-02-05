import datetime


def date_from_post(post_data):
    return (
        datetime.date(int(post_data['first_date_year']), int(post_data['first_date_month']),
                      int(post_data['first_date_day'])),
        datetime.date(int(post_data['last_date_year']), int(post_data['last_date_month']),
                      int(post_data['last_date_day']))
    )


def get_sum_pcs_price(qs):
    sum_pcs = 0
    sum_price = 0
    for item in qs:
        sum_pcs += item.pcs
        sum_price += item.price_roz*item.pcs
    return {'sum_pcs': sum_pcs, 'sum_price': sum_price}
