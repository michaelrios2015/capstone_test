import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_two import connTwo


# just here for testing
# import truncate

# truncate.deleteGinnies()


# adding the first day pools to the website database
def addFirstDay():

    connTwo.autocommit = True
    cursorTwo = connTwo.cursor()

    # delete Ginnies from cmos database
    sql = """
    COPY ginnies FROM 'C:\\Users\\Public\\1stbddailypoolswithcurrfloatM' DELIMITER ','  CSV HEADER;


    COPY ginnies FROM 'C:\\Users\\Public\\1stbddailypoolswithcurrfloatX' DELIMITER ','  CSV HEADER;


    COPY ginnies FROM 'C:\\Users\\Public\\1stbddailypoolswithcurrfloatJM' DELIMITER ','  CSV HEADER;


    COPY ginnies FROM 'C:\\Users\\Public\\1stbddailypoolswithcurrfloatRG' DELIMITER ','  CSV HEADER;
        """

    cursorTwo.execute(sql)

    connTwo.commit()

    print("first day added")


# TESTING

# addFirstDay()
