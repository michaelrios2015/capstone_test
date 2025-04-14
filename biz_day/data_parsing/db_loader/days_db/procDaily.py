# used for first day to add daily pools

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_dets import conn


# will take in date and a boolen for first business day or not
def add_daily(date, first):

    conn.autocommit = True
    cursor = conn.cursor()

    # so how to I get this date...

    date = "'" + date + "'"

    # delete FHAVA_2 this is only done so I can rerun the program for testing purposes
    sql = (
        """
            call processdailydataforweb("""
        + date
        + """, """
        + first
        + """);

        """
    )

    cursor.execute(sql)

    conn.commit()
    # conn.close()

    print("processed dailies")


# testing

# date = "2025-02-01"
# add_daily(date, "true")
