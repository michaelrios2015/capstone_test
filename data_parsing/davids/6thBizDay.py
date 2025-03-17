import psycopg2
import requests
from zipfile import ZipFile
import io

# The input files need to be rolled one month forward

# -*- coding: utf-8 -*-
"""
Created on Sun May  2 07:01:47 2021

@author: gabri
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 07:12:56 2021

@author: gabri
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 06:09:48 2021

@author: gabri
"""


# *********************************************************
#       Goal : Use Pool level data to find SMM for each pool
#
#
#
# *********************************************************


# *********************************************************
#    We can recombine these for platnums later
# *********************************************************

# *********************************************************
#    For Some Reason We are too Fast, try 36178GKC7 by hand Loan Level
# *********************************************************

# *********************************************************
#    THESE CHANGE MONTHLY
# *********************************************************


# Change monthly


# so thses have to be changed by hand becuase I cannot get requests to work
data_url_1 = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/nimonSFPS_202502.zip"

data_url_2 = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/monthlySFPS_202502.zip"


# it's not very important but here ideally i only change the date once and the rest is don for me
mOutputDir = "output/2025-02/"

# current month for monthlySFPS
mPoolFile = "monthlySFPS_202502.txt"
# past month for monthlySFPS
mPoolFileOld = {"nimonSFPS_202502.txt", "monthlySFPS_202501.txt"}

# mPoolFileOld = 'monthlySFPS_202102.txt'
# mPoolFile2 = 'dailySFPS.txt'

# mPlatFile1 = 'platcoll_202103.txt'

# Change monthly
oFilename = "SMMTest_February.txt"


# *********************************************************
#    END OF MONTHLY CHANGE
# *********************************************************

# this section pulled the files for me... does not work now not sure why

# r = requests.get(data_url_1)  # create HTTP response object

# # print(r.content)
# # extract file
# z = ZipFile(io.BytesIO(r.content))
# # send it to data
# z.extractall("data\poolFiles")


# r = requests.get(data_url_2)  # create HTTP response object

# # print(r.content)
# # extract file
# z = ZipFile(io.BytesIO(r.content))
# # send it to data
# z.extractall("data\poolFiles")

# this is where the files will go

mDir = "data/poolFiles/"
#
#    Program 2
print("Running...")

# date i use for the database

date = "'" + mOutputDir[-8:-1] + "-01" + "'"

# print(date)


# starting david's stuff

cusipMap = {}
NameMap = {}
Count = 0.0
mMissingCusipSet = {""}


# cusipMap : key -> cusip , val -> [cpr, cprNext]
# New to added New Issue Pools as well

mBuffer = 0
mSize = 0

for i in mPoolFileOld:
    ginnieFile = open(mDir + i, "r")
    #
    for line in ginnieFile:
        lineList = line.split("|")
        if lineList[0] == "PS":
            try:
                mFactor = float(lineList[10 + mBuffer])
            except:
                #                print(lineList[1+mBuffer] + " : Missing Factor")
                mMissingCusipSet.add(lineList[1 + mBuffer])
            if mFactor > 0:
                try:
                    #                OTerm = float(lineList[20+mBuffer])   This uses Orginal Term
                    OTerm = float(lineList[18 + mBuffer])
                except:
                    mMissingCusipSet.add(lineList[1 + mBuffer])
                #            mSize += float(lineList[9])
                #                    print(line)
                try:
                    WALA = float(lineList[19 + mBuffer])
                    # This switchs it to using current OTERM rather than orig
                    OTerm += float(lineList[19 + mBuffer])

                except:
                    mMissingCusipSet.add(lineList[1 + mBuffer])
                    mSize += float(lineList[9])
                try:
                    gWAC = float(lineList[17 + mBuffer])
                except:
                    gWAC = float(lineList[6 + mBuffer]) + 0.5

                # Check this is this ok. Not sure if I need to tick up wala by 1
                if WALA < OTerm - 1:
                    WALA += 1

                Compound = 1 + gWAC / 1200.0
                BnTop = 1 - Compound ** (WALA - OTerm)
                BnBottom = 1 - Compound ** (-1 * OTerm)
                Bn1Top = 1 - Compound ** (WALA + 1 - OTerm)
                Bn = BnTop / BnBottom
                Bn1 = Bn1Top / BnBottom

                if WALA <= OTerm - 2:
                    Schedn = (Bn - Bn1) / Bn

                elif WALA == OTerm - 1:
                    Schedn = 1

                else:
                    print("oh boy")

                # Scheduled Paydown in what? Remember
                cusipMap[lineList[1 + mBuffer]] = [
                    float(lineList[9 + mBuffer]),
                    Schedn,
                    0,
                    0,
                ]

    ginnieFile.close()


print("Intial Month Done.")

# print(len(mMissingCusipSet))
# print(mSize/1000000)
# print("36223UKV9")
# print( cusipMap[ "36223UKV9"][0])
# print( cusipMap[ "36223UKV9"][1])


ginnieFile = open(mDir + mPoolFile, "r")
# outputFile = open(mDir + oFilename, 'w')
#
for line in ginnieFile:
    lineList = line.split("|")
    if lineList[0] == "PS":
        mCusip = lineList[1 + mBuffer]
        if mCusip in cusipMap:
            mFace = float(lineList[9 + mBuffer])
            SchdRemaining = cusipMap[mCusip][0] * (1 - cusipMap[mCusip][1])
            Actual = SchdRemaining - mFace
            #            Actual = cusipMap[mCusip][0] - mFace  # + Scheduled
            if SchdRemaining > 0:
                SMM = Actual / SchdRemaining
            else:
                SMM = 0

            cusipMap[mCusip][2] = SMM
            cusipMap[mCusip][3] = (1 - (1 - SMM) ** 12) * 100

        else:
            mMissingCusipSet.add(lineList[1 + mBuffer])


ginnieFile.close()


print("Second Month Done.")


print("Number of pools with bad data")
print(len(mMissingCusipSet))


outputFile = open(mOutputDir + oFilename, "w")


for key in cusipMap:
    valList = [str(elem) for elem in cusipMap[key]]
    print(str(key) + "," + valList[3], file=outputFile)
#    print(str(key) + ',' + ','.join(va lList), file = outputFile)


outputFile.close()


print("Program Complete.")

###########################
# david'd program ends I am adding
###################################

print("-------------------------------")
print("Starting database stuff")

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

# delete old cprs
sql = (
    """
DELETE FROM actualcprs
WHERE date = """
    + date
    + """;
"""
)

cursor.execute(sql)

# create temp table
sql = """
create temporary table cpr (cusip varchar, cpr double precision );
"""
cursor.execute(sql)

# should read in the newly created cvs doc inot our temp table
csv_file_name = mOutputDir + oFilename
sql = "COPY cpr FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))

# use temp table to insert info into real table
sql = (
    """
INSERT INTO actualcprs (cusip, actualcpr, date)
SELECT cusip, cpr/100, """
    + date
    + """
FROM cpr;

DROP table cpr
"""
)

cursor.execute(sql)

sql = """
SELECT * FROM actualcprs order by date desc limit 5;
"""
cursor.execute(sql)
records = cursor.fetchall()

for row in records:
    for column in row:
        print(column, end=", ")
    print()


sql = (
    """
SELECT COUNT(*) FROM actualcprs where date =  """
    + date
    + """ ;
"""
)
cursor.execute(sql)
records = cursor.fetchall()

print("\ncount = ", records[0][0])


conn.commit()
conn.close()

print("intial CPRs ereased official cprs added")
