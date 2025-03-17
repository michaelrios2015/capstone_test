# Every month the input files change slightly

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:27:12 2021

@author: gabri
"""

import csv
import psycopg2
from zipfile import ZipFile
import io
import requests

mDir = "data/poolFiles/"

data_url_1 = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/dailyllmni.zip"

# *********************
#
# CHANGE
#
# *************************

data_url_2 = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/llmon1_202502.zip"


data_url_3 = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/llmon2_202502.zip"


# LoanFile = 'GNMA_MBS_LL_MON_202103_002.txt'
LoanFile = {
    "dailyllmni.txt",
    "GNMA_MBS_LL_MON_202502_002.txt",
    "GNMA_MBS_LL_MON_202502_001.txt",
}
# LoanFile = {'dailyll_new.txt', 'GNMA_MBS_LL_MON_202110_002.txt', 'GNMA_MBS_LL_MON_202110_001.txt' }

# mPoolFile2 = 'dailySFPS.txt'
# should jusr be for output
directory = "output/2025-02/"

# SpeedFile = "D:\Mortgage Project\Dolan\\ginnie_202102_monthly_predictions_roll.csv"  Speed File

oFilename = "FHAVATest_202502.txt"

# print(date)
# *********************
#
# NO MORE CHANGE
#
# *************************

date = "'" + directory[-8:-1] + "-01" + "'"


# r = requests.get(data_url_1)  # create HTTP response object
# # extract file
# z = ZipFile(io.BytesIO(r.content))
# # send it to data
# z.extractall("data\poolFiles")

# r = requests.get(data_url_2)  # create HTTP response object
# # extract file
# z = ZipFile(io.BytesIO(r.content))
# # send it to data
# z.extractall("data\poolFiles")

# r = requests.get(data_url_3)  # create HTTP response object
# # extract file
# z = ZipFile(io.BytesIO(r.content))
# # send it to data
# z.extractall("data\poolFiles")


#
#    Program 2
print("Running...")

cusipMap = {}
Count = 0
Count2 = 0

Total = 0

# cusipMap : key -> cusip , val -> [cpr, cprNext]
for i in LoanFile:
    ginnieFile = open(mDir + i, "r")
    for line in ginnieFile:
        if line[0] == "P":
            cusip = line[1:10]
            cusipMap[cusip] = [0, 0, 0, 0]
        if line[0] == "T":
            cusip = ""
        if line[0] == "L":
            # This should change for the secondary file

            try:  # Older loans
                balance = float(line[67:78])
            except:  # Less than 6 month age
                if line[56:67].isdigit():
                    balance = float(line[56:67])
                else:
                    Count += 1

            if line[21] == "N":
                cusipMap[cusip][3] += balance
            elif line[21] == "R":
                cusipMap[cusip][2] += balance
            elif line[21] == "F":
                cusipMap[cusip][1] += balance
            elif line[21] == "V":
                cusipMap[cusip][0] += balance
            else:
                print("oh no Mr Bill")
    ginnieFile.close()

print(Count)

oFile = open(directory + oFilename, "w")
for i in cusipMap:
    Total = cusipMap[i][0] + cusipMap[i][1] + cusipMap[i][2] + cusipMap[i][3]
    if Total > 0:
        mString = i + ","
        oFile.write(mString)
        formatted_float = "{:.5f}".format(cusipMap[i][0] / Total)
        oFile.write(formatted_float + ",")
        formatted_float = "{:.5f}".format(cusipMap[i][1] / Total)
        oFile.write(formatted_float + ",")
        formatted_float = "{:.5f}".format(cusipMap[i][2] / Total)
        oFile.write(formatted_float + ",")
        formatted_float = "{:.5f}".format(cusipMap[i][3] / Total)
        oFile.write(formatted_float + "\n")
oFile.close()


# david'd program ends I am adding

# connects to database
conn = psycopg2.connect(
    database="cmos_builder",
    user="postgres",
    password="JerryPine",
    host="localhost",
    port="5432",
)

# magic stuff I don't really undertand and I should learn
conn.autocommit = True
cursor = conn.cursor()

# create the temp table
# apperntly the va are in the second column, and fha in the third... since the table was built the opposite
# way I read them in va, fha and then switch them later
sql = """
create temporary table tempfhava (cusip varchar, va double precision, fha double precision, rural double precision, indian double precision);
"""
cursor.execute(sql)

# should read in the newly created cvs doc inot our temp table
csv_file_name = directory + oFilename
sql = "COPY tempfhava FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


# use temp table to insert info into real table
sql = (
    """
INSERT INTO poolfhavas (cusip, fha, va, rural, indian, date)
SELECT cusip, fha, va, rural, indian, """
    + date
    + """
FROM tempfhava;

DROP TABLE tempfhava;
"""
)

cursor.execute(sql)

sql = """
SELECT * FROM poolfhavas order by date desc limit 5;
"""
cursor.execute(sql)
records = cursor.fetchall()

for row in records:
    for column in row:
        print(column, end=", ")
    print()


sql = (
    """
SELECT COUNT(*) FROM poolfhavas where date =  """
    + date
    + """ ;
"""
)
cursor.execute(sql)
records = cursor.fetchall()

print("\ncount = ", records[0][0])


conn.commit()
conn.close()
