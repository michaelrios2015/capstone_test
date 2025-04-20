import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_two import connTwo


# # just here for testing
# import truncate

# truncate.deleteGinnies()


def add_cmos():

    connTwo.autocommit = True
    cursorTwo = connTwo.cursor()

    # deleting cmos
    sql = """ TRUNCATE cmos; """

    cursorTwo.execute(sql)

    #################################################################

    # add them back
    sql = """
            COPY cmos FROM 'C:\\Users\\Public\\cmodataforweb' DELIMITER ',' CSV HEADER;
        """

    cursorTwo.execute(sql)

    connTwo.commit()

    print("cmos trincated and re-added")


# testing
