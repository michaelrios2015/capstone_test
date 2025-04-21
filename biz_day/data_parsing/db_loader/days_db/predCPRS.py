# used for first day to add daily pools

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "davids"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "local_parser"))


# biz_day\data_parsing\davids\month.py
# connects to database
from conn_dets import conn
import month
import date_c


# this just loads everything as 0 for the moment
def pred_cprs(date):

    # gives us YYYYMMDD for next month
    next_month = month.next_month(date) + "01"

    # print(next_month)

    # so I can delete the predictions, and rerun the script for testing purposes
    next_month_2 = next_month[0:4] + "-" + next_month[4:6] + "-" + next_month[6:]

    # print(next_month_2)

    # turns data into  database date
    date = date_c.date_conv(date)

    # print(date)

    conn.autocommit = True
    cursor = conn.cursor()

    # making dates ready for sql
    date = "'" + date + "'"

    next_month = "'" + next_month + "'"

    next_month_2 = "'" + next_month_2 + "'"

    # this just lets me retest the program by deleting ones I have just added
    sql = (
        """
        DELETE FROM poolpredictions where date = """
        + next_month_2
        + """;
        """
    )

    cursor.execute(sql)

    # # adding poredictions
    sql = (
        """
            INSERT INTO poolpredictions (cusip, "totalOutstanding", vpr, "vprNext", cdr, "cdrNext", cpr, "cprNext", date)
            SELECT DISTINCT cusip, 0, 0, 0, 0, 0, 0, 0, TO_DATE("""
        + next_month
        + """,'YYYYMMDD')
            FROM poolbodies p
            WHERE p.date = """
        + date
        + """;
        """
    )

    cursor.execute(sql)

    conn.commit()

    print("predictions added")


# date = "202503"
