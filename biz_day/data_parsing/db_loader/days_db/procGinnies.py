# used for first day to add daily pools

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_dets import conn


# will take in date and a boolen for first business day or not
# just uses stored procedure to process the new daily pools
def proc_ginnies(date, fed_date):

    conn.autocommit = True
    cursor = conn.cursor()

    # so how to I get this date...

    date = "'" + date + "'"

    fed_date = "'" + fed_date + "'"

    # delete FHAVA_2 this is only done so I can rerun the program for testing purposes
    sql = (
        """
            call  processdataforweb("""
        + date
        + """, """
        + fed_date
        + """);

        """
    )

    cursor.execute(sql)

    conn.commit()

    print("processed ginnies")


# testing

# date = "2025-03-01"
# fed_date = "2025-04-02"
# proc_ginnies(date, fed_date)
