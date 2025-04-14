import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_two import connTwo


# just here for testing
import truncate

truncate.deleteGinnies()


# def addGinnies():


connTwo.autocommit = True
cursorTwo = connTwo.cursor()


# delete Ginnies from cmos database
sql = """
    COPY ginnies FROM 'C:\\Users\\Public\\test_ginnieplatswithcurrfloatM' DELIMITER ','  CSV HEADER; 

    COPY ginnies FROM 'C:\\Users\\Public\\test_ginnieplatswithcurrfloatX' DELIMITER ','  CSV HEADER;

    COPY ginnies FROM 'C:\\Users\\Public\\test_poolswithcurrfloatM' DELIMITER ','  CSV HEADER;   

    COPY ginnies FROM 'C:\\Users\\Public\\test_poolswithcurrfloatX' DELIMITER ','  CSV HEADER;

    COPY ginnies FROM 'C:\\Users\\Public\\test_poolswithcurrfloatJM' DELIMITER ','  CSV HEADER;

    COPY ginnies FROM 'C:\\Users\\Public\\test_poolswithcurrfloatRG' DELIMITER ','  CSV HEADER; """

cursorTwo.execute(sql)

connTwo.commit()

print("ginnies added")
