from datetime import datetime
from dateutil.relativedelta import relativedelta

# a helper function that gives me the next or pervious month in YYYYMM format, ideally this would probably ne in a different folder


def prev_month(date):

    # turn string into date
    date_object = datetime.strptime(date, "%Y%m")
    # print(date_object)

    # get previous month
    previous_month = date_object - relativedelta(months=1)

    # print(previous_month)

    # turn it back into string
    date_string = previous_month.strftime("%Y%m")
    return date_string


# print(prev_month("202502"))


def next_month(date):

    # turn string into date
    date_object = datetime.strptime(date, "%Y%m")
    # print(date_object)

    # get previous month
    next_month = date_object + relativedelta(months=1)

    # print(previous_month)

    # turn it back into string
    date_string = next_month.strftime("%Y%m")
    return date_string


# print(next_month("202502"))
