import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_two import connTwo


# # just here for testing
# import truncate

# truncate.deleteGinnies()


def addDailies():

    connTwo.autocommit = True
    cursorTwo = connTwo.cursor()

    # delete Ginnies from cmos database
    sql = """
    COPY ginnies FROM 'C:\\Users\\Public\\test_dailypoolswithcurrfloatM' DELIMITER ','  CSV HEADER;


    COPY ginnies FROM 'C:\\Users\\Public\\test_dailypoolswithcurrfloatX' DELIMITER ','  CSV HEADER;  


    COPY ginnies FROM 'C:\\Users\\Public\\test_dailypoolswithcurrfloatJM' DELIMITER ','  CSV HEADER;


    COPY ginnies FROM 'C:\\Users\\Public\\test_dailypoolswithcurrfloatRG' DELIMITER ','  CSV HEADER;
        """

    cursorTwo.execute(sql)

    connTwo.commit()

    print("dalies added")


# testing

# addDailies()
