import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_two import connTwo

# # just here for testing --- need to remove
# import truncate

# truncate.deleteGinnies()


# this adds regular ginnies to our database for the website
def addGinnies():

    connTwo.autocommit = True
    cursorTwo = connTwo.cursor()

    # delete Ginnies from cmos database
    sql = """
        COPY ginnies FROM 'C:\\Users\\Public\\ginnieplatswithcurrfloatM' DELIMITER ','  CSV HEADER; 

        COPY ginnies FROM 'C:\\Users\\Public\\ginnieplatswithcurrfloatX' DELIMITER ','  CSV HEADER;

        COPY ginnies FROM 'C:\\Users\\Public\\poolswithcurrfloatM' DELIMITER ','  CSV HEADER;   

        COPY ginnies FROM 'C:\\Users\\Public\\poolswithcurrfloatX' DELIMITER ','  CSV HEADER;

        COPY ginnies FROM 'C:\\Users\\Public\\poolswithcurrfloatJM' DELIMITER ','  CSV HEADER;

        COPY ginnies FROM 'C:\\Users\\Public\\poolswithcurrfloatRG' DELIMITER ','  CSV HEADER; """

    cursorTwo.execute(sql)

    connTwo.commit()

    print("ginnies added")


# testing

# addGinnies()
