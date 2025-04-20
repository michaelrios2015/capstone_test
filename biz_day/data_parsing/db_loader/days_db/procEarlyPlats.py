# used for first day to add daily pools

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_dets import conn


# will take in date and a boolen for first business day or not
# just uses stored procedure to process the new daily pools
def proc_early_plats(date):

    conn.autocommit = True
    cursor = conn.cursor()

    # so how to I get this date...

    date = "'" + date + "'"

    # deleting so I can test
    sql = (
        """
            DELETE FROM platinumbodies where date = """
        + date
        + """;

        """
    )

    cursor.execute(sql)

    # deleting for testing
    sql = (
        """
            DELETE FROM platfhavas where date = """
        + date
        + """;

        """
    )

    cursor.execute(sql)

    # making the fake platinums
    sql = (
        """
            call  earlyplatstuff("""
        + date
        + """);

        """
    )

    cursor.execute(sql)

    conn.commit()
    # conn.close()

    print("processed early plats")
