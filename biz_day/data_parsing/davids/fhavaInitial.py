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


import os
import month
import csv
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "local_parser"))

import date_c


# this is running on the 4th business day in august I gave it 202507 as the date...
# so that will be my date here

# on the 6th day the new ones will be called 202508... not entirely sure if this is right but at the
# moment it is what it is


def fhava_4th(date):

    # input
    mDir = "biz_day/data/input/"

    # output
    directory = "biz_day/data/output/"

    prev_month = month.prev_month(date)
    print(prev_month)

    # Files published 6th business day of month n and the last file published the last business day of month n
    # we are running this on the 4th day and these seem to be the files till up, so looks like two months back
    # while dailyllmni
    mLoanFileOld = {
        "GNMA_MBS_LL_MON_" + prev_month + "_001.txt",
        "GNMA_MBS_LL_MON_" + prev_month + "_002.txt",
        "dailyllmni.txt",
    }

    # Files published 4th business day of month n+1
    mLiqLoanFile = {"llmonliq_" + date + ".txt"}

    #  will only have 1 of these
    oFilename = "GNMAPoolCohortSMMTest.txt"

    MissingLoan = 0
    #
    #    Program 2
    print("Running...")

    NameMap = {}
    PoolCohortMap = {}
    Count = 0.0
    m6thDay = True

    mMissingCusipSet = {""}

    # Has everything, missing wala, missing wam, missing wac, missing curr bal, missing both bal
    mCount = [0, 0, 0, 0, 0, 0, 0]
    mCount2 = 0
    mBuffer = 0

    LoanSet = set()  # Loans for which we used Orig Balance not Cur Balance

    mPaidCount = [0, 0, 0, 0, 0, 0]

    # Find the list of paid off loans by loan ID
    for i in mLiqLoanFile:
        ginnieFile = open(mDir + i, "r")

        lines = ginnieFile.readlines()[1:]

        for line in lines:
            #        print(line)

            mData = line.split("|")
            if mData[0] == "LR":
                LoanSet.add(mData[6])
                mPaidCount[int(mData[14]) - 1] += 1

        ginnieFile.close()

    print("Paid Counted")
    print(mPaidCount)

    Count = 0.0

    # For each pool find previous and schedule for total pool and for program

    for i in mLoanFileOld:
        ginnieFile = open(mDir + i, "r")

        lines = ginnieFile.readlines()[1:]

        for line in lines:

            mInclude = True
            if line[0] == "L":

                # Paid off this (old) month
                if str(line[134:135]) == "Y":
                    mInclude = False

                if mInclude:

                    # Build the cohort String
                    mCohort = line[1:7] + "_" + line[21:22]
                    mCohort2 = line[1:7]

                    mLoanID = line[7:17]
                    #                mCusip = line[7:17]

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
                        except:
                            cBal = 0
                            mCount[5] += 1

                    if cBal == 0:
                        mCount2 += 1

                    if mCohort not in PoolCohortMap:
                        # Current Balance, Number of Loans, Scheduled, Remaining Bal, CPR
                        PoolCohortMap[mCohort] = [0, 0, 0, 0, 0]

                    if mCohort2 not in PoolCohortMap:
                        # Current Balance, Number of Loans, Scheduled, Remaining Bal, CPR
                        PoolCohortMap[mCohort2] = [0, 0, 0, 0, 0]

                    PoolCohortMap[mCohort][0] += cBal
                    PoolCohortMap[mCohort][1] += 1
                    PoolCohortMap[mCohort2][0] += cBal
                    PoolCohortMap[mCohort2][1] += 1

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

                    PoolCohortMap[mCohort][2] += (
                        cBal * Schedn
                    )  # Scheduled Paydown in what? Remember
                    PoolCohortMap[mCohort2][2] += (
                        cBal * Schedn
                    )  # Scheduled Paydown in what? Remember

                    if mLoanID in LoanSet:
                        PoolCohortMap[mCohort][3] += 0
                        PoolCohortMap[mCohort2][3] += 0
                        Count += 1
                    else:
                        PoolCohortMap[mCohort][3] += (1 - Schedn) * cBal
                        PoolCohortMap[mCohort2][3] += (1 - Schedn) * cBal

        ginnieFile.close()

    print("Number of loans paid")
    print(Count)
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

    for i in PoolCohortMap:
        SchdRemaining = PoolCohortMap[i][0] - PoolCohortMap[i][2]
        Actual = SchdRemaining - PoolCohortMap[i][3]
        if SchdRemaining > 0:
            SMM = Actual / SchdRemaining
        else:
            SMM = 0
        # CPR
        PoolCohortMap[i][4] = 100 * (1 - (1 - SMM) ** 12)

    print("number of pools")
    print(len(PoolCohortMap))

    outputFile = open(mDir + oFilename, "w")

    # This seems ok

    for key in PoolCohortMap:
        mTemp = key.split("_")
        if (len(mTemp)) == 1:
            valList = [str(elem) for elem in PoolCohortMap[key]]
            print(str(key) + "," + ",".join(valList), file=outputFile)
        else:
            if mTemp[0] not in NameMap:
                NameMap[mTemp[0]] = [0, 0]
            if mTemp[1] == "F":
                NameMap[mTemp[0]][0] = PoolCohortMap[key][4]
            if mTemp[1] == "V":
                NameMap[mTemp[0]][1] = PoolCohortMap[key][4]

    outputFile.close()

    print("First outputfile Complete.")

    # for key in PoolCohortMap:
    #   mTemp = key.split("_")
    #  if mTemp[0]  not in NameMap:
    #     NameMap[ mTemp[0]] = [0,0]
    #  if mTemp[1] == "F":
    #      NameMap[ mTemp[0]][0] = PoolCohortMap[key][4]
    #  if mTemp[1] == "V":
    #      NameMap[ mTemp[0]][1] = PoolCohortMap[key][4]

    # I assume this is a good idea to do
    outFileName = directory + "Mikey_" + oFilename

    outputFile = open(outFileName, "w")
    print("Pood ID, FHA CPR, VA CPR", file=outputFile)
    for key in NameMap:
        valList = [str(elem) for elem in NameMap[key]]
        print(str(key) + "," + ",".join(valList), file=outputFile)

    outputFile.close()

    # davids program done, just adding date I am sure there is a better way to do it

    # not sure if I always do this here but why not
    date = date_c.date_conv(date)

    with open(outFileName, newline="") as csvfile:
        next(csvfile)
        data = list(csv.reader(csvfile, delimiter=","))

        head = []

        for row in data:

            name = row[0]

            head.append([name, row[1], row[2], date])

    headfields = ["name", "fha_cpr", "va_cpr", "date"]

    # should be fine to just name them fhava_cpr.. but I added init
    with open("biz_day/data/output/fhava_cpr.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(headfields)

        # writing the data rows
        csvwriter.writerows(head)

    print("Program Complete.")


########################################################################################
########################################################################################

# testing, will get date from 4th day code

# fhava_4th("202507")
