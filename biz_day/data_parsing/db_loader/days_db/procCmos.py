# used for first day to add daily pools

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_dets import conn


# will take in date and a boolen for first business day or not
# just uses stored procedure to process the new daily pools
def proc_cmos(date):

    conn.autocommit = True
    cursor = conn.cursor()

    # so how to I get this date...

    date = "'" + date + "'"

    # addes in ming plat data
    sql = (
        """
            call  allcmostoredprocedure("""
        + date
        + """);

        """
    )

    cursor.execute(sql)

    conn.commit()
    # conn.close()

    print("processed cmos")
