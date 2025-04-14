import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_two import connTwo


def deleteGinnies():
    connTwo.autocommit = True
    cursorTwo = connTwo.cursor()

    # so how to I get this date...

    # delete Ginnies from cmos database
    sql = """
        TRUNCATE ginnies;

        """

    cursorTwo.execute(sql)

    connTwo.commit()

    print("deleted ginnies")


# deleteGinnies()
