# *********************************************************
#       Goal : Use loan level data to find SMM for each pool
#       This means a. Schedule pay from perv. month
#                  b. Actual from this month
#                  c. SMM  calc
#       Note : We really want to use SMM to find next month
#       Month schd. paydown but this helps check the code
#       Can't make full pool report from LLD, still need
#       eMBS for security fields
# *********************************************************


# *********************************************************
#    Errors : Our data is for UPB outstanding of the loan
#    This is different then how it would appear in the pool
#    Hence we when loans are in arrears our current face calc
#    Is off
# *********************************************************


# *********************************************************
#    Some Errors
#    Loans less than 6 age we have rounding issues
#    Loans in forebarence (some are have neg WAM)
#    Loans that pay ahead of schedule and stop paying <--- this is easiest to fix
# *********************************************************


# *********************************************************
#    Big problem :
#    As the filter for mInclude needs to be written 2x its prone to errors
# *********************************************************

# STOP CHANGE
#########################################################


# START CHANGE
###########################################################################


import os
import csv
import psycopg2

# where imput and output files are kept
mDir = "biz_day/data/input/"


# Files published 6th business day of month n and the last file published the last business day of month n
mLoanFileOld = {
    # two from the past month
    "GNMA_MBS_LL_MON_202501_001.txt",
    "GNMA_MBS_LL_MON_202501_002.txt",
    # this is the current month
    "dailyllmni.txt",
}

# Files published 6th business day of month n+1
# current month
mLoanFile = {"GNMA_MBS_LL_MON_202502_001.txt", "GNMA_MBS_LL_MON_202502_002.txt"}

# fine names
oFilename = "GNMAPoolCohortSMMTest.txt"

mOutputDir = "biz_day/data/output/"

# this is a month ahead... because there was some mix up with the months a while back
# should probably revisit at some point
date = "2025-03-01"


# STOP CHANGE
###########################################################################

MissingLoan = 0
#
#    Program 2
print("Running...")

NameMap = {}
LoanMap = {}
Count = 0.0
mCount = 0.0
m6thDay = True

mMissingCusipSet = {""}

# Has everything, missing wala, missing wam, missing wac, missing curr bal, missing both bal
mCount = [0, 0, 0, 0, 0, 0]
mCount2 = 0
mBuffer = 0

LoanSet = set()  # Loans for which we used Orig Balance not Cur Balance

for i in mLoanFileOld:
    ginnieFile = open(mDir + i, "r")

    lines = ginnieFile.readlines()[1:]

    for line in lines:

        mInclude = True
        if line[0] == "L":

            # Paid off this month
            if str(line[134:135]) == "Y":
                mInclude = False

            if mInclude:

                # Build the cohort String
                mCohort = line[1:7] + "_" + line[21:22]
                mCusip = line[7:17]

                try:
                    WALA = float(line[81:84])
                except:
                    mCount[1] += 1
                try:
                    # We are probabily screwing up 10/20 loans but really only care about TBA eligible
                    # I wonder if we are screwing up ARMss
                    # why are we adding wala here?  - We could us OTERM instead
                    OTerm = float(line[84:87])
                    OTerm += WALA
                except:
                    mCount[2] += 1
                try:
                    gWAC = float(line[40:45])
                    gWAC = gWAC / 1000
                except:
                    mCount[3] += 1

                try:
                    # This number is left blank for the first 6 months.
                    cBal = float(line[67:78])
                except:
                    cBal = 0
                    mCount[4] += 1
                if cBal == 0:
                    try:
                        cBal = float(line[56:67])
                        LoanSet.add(line[7:17])
                    except:
                        cBal = 0
                        mCount[5] += 1

                if cBal == 0:
                    mCount2 += 1

                if mCohort not in LoanMap:
                    # Current Balance, Number of Loans, Scheduled, Remaining Bal, CPR
                    LoanMap[mCohort] = [0, 0, 0, 0, 0]

                LoanMap[mCohort][0] += cBal
                LoanMap[mCohort][1] += 1

                Compound = 1 + gWAC / 1200.0
                BnTop = 1 - Compound ** (WALA - OTerm)
                BnBottom = 1 - Compound ** (-1 * OTerm)
                Bn1Top = 1 - Compound ** (WALA + 1 - OTerm)
                Bn = BnTop / BnBottom
                Bn1 = Bn1Top / BnBottom

                if WALA <= OTerm - 2:
                    Schedn = (Bn - Bn1) / Bn
                else:
                    Schedn = 1
                LoanMap[mCohort][2] += (
                    cBal * Schedn
                )  # Scheduled Paydown in what? Remember

        # BuildCohortString

    ginnieFile.close()


print("Missing Wala")
print(mCount[1])
print("Missing WAC")
print(mCount[2])
print("Missing WAC")
print(mCount[3])
print("Missing Curr Bal")
print(mCount[4])
print("Missing Both Bal")
print(mCount[5])


print("Intial Month Done.")
print("Number of loans with no current loan bal")
print(len(LoanSet))


print("Missing Both Current and Orig Loan Bal")
print(mCount2)


# Missing
# Figure out how to grab balances for 0-6 wala
# Compute the CPRs
mCount2 = 0
mCount3 = 0
for i in mLoanFile:
    ginnieFile = open(mDir + i, "r")

    lines = ginnieFile.readlines()[1:]

    for line in lines:
        #        print(line)

        if line[0] == "L":

            mCohort = line[1:7] + "_" + line[21:22]
            try:
                WALA = float(line[81:84]) - 1
            except:
                Count += 1
            try:
                gWAC = float(line[40:45])
            except:
                Count += 1

            mInclude = True
            if str(line[134:135]) == "Y":
                mInclude = False

            if mInclude:
                cBal = 0
                if line[7:17] in LoanSet:
                    try:
                        cBal = float(line[56:67])
                    except:
                        cBal = 0
                        mCount2 += 1
                else:
                    try:
                        cBal = float(line[67:78])
                    except:
                        cBal = 0
                        mCount3 += 1
                        if mCount3 < 100:
                            print(line[24:32])

                if mCohort in LoanMap:
                    LoanMap[mCohort][3] += cBal

    ginnieFile.close()


print("Second Month Done Missing Laons")
print(MissingLoan)


print("Number that should have orig loan but don't")
print(mCount2)
print("Number that should have curr loan but don't")
print(mCount3)

Count = 0
for i in LoanMap:
    SchdRemaining = LoanMap[i][0] - LoanMap[i][2]
    Actual = SchdRemaining - LoanMap[i][3]
    if SchdRemaining > 0:
        SMM = Actual / SchdRemaining
    else:
        SMM = 0
    # CPR
    LoanMap[i][4] = 100 * (1 - (1 - SMM) ** 12)


print("CPRs")


outputFile = open(mDir + oFilename, "w")


for key in LoanMap:
    valList = [str(elem) for elem in LoanMap[key]]
    print(str(key) + "," + ",".join(valList), file=outputFile)


outputFile.close()

print("First outputfile Complete.")


for key in LoanMap:
    mTemp = key.split("_")
    if mTemp[0] not in NameMap:
        NameMap[mTemp[0]] = [0, 0]
    if mTemp[1] == "F":
        NameMap[mTemp[0]][0] = LoanMap[key][4]
    if mTemp[1] == "V":
        NameMap[mTemp[0]][1] = LoanMap[key][4]


outputFile = open(mOutputDir + "Mikey_" + oFilename, "w")
print("Pood ID, FHA CPR, VA CPR", file=outputFile)
for key in NameMap:
    valList = [str(elem) for elem in NameMap[key]]
    print(str(key) + "," + ",".join(valList), file=outputFile)

outputFile.close()


print("Program Complete.")


# 1st file

with open(mOutputDir + "Mikey_" + oFilename, newline="") as csvfile:
    next(csvfile)
    data = list(csv.reader(csvfile, delimiter=","))

    head = []

    for row in data:

        name = row[0]
        fha_cpr = row[1].strip()
        va_cpr = row[2].strip()

        head.append([name, fha_cpr, va_cpr, date])


headfields = ["name", "fha_cpr", "va_cpr", "date"]

with open(mOutputDir + "fhava_cpr.cvs", "w", newline="") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(headfields)

    # writing the data rows
    csvwriter.writerows(head)


# #################################################################################
# # database
# ##############################################################################


# #####################################################################
# ######################################################################
# # DATABASE!!


# # connects to database
# conn = psycopg2.connect(
#     database="cmos_builder",
#     user="postgres",
#     password="JerryPine",
#     host="localhost",
#     port="5432",
# )

# ###########################################################
# # change THESE


# # connecting to database
# # what is autocommit
# conn.autocommit = True
# cursor = conn.cursor()


# # read in fhava_cpr's
# csv_file_name = mOutputDir + "fhava_cpr.cvs"
# sql = "COPY fhava_cpr FROM STDIN DELIMITER ',' CSV HEADER"
# cursor.copy_expert(sql, open(csv_file_name, "r"))

# ########################################################
# # 2nd part
# #################################################

# print("fhava_cpr")
# print("----------------------------------")
# sql = """
# SELECT * FROM fhava_cpr order by date desc limit 5;
# """
# cursor.execute(sql)
# records = cursor.fetchall()

# for row in records:
#     for column in row:
#         print(column, end=", ")
#     print()


# sql = (
#     """
# SELECT COUNT(*) FROM fhava_cpr where date =  """
#     + "'"
#     + date
#     + "'"
#     + """;
# """
# )
# cursor.execute(sql)
# records = cursor.fetchall()

# print("\ncount = ", records[0][0])


# conn.commit()
# conn.close()
