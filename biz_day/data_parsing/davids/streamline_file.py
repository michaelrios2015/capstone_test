import month
import csv
import os
import sys

# david's code for some of the new fhava stuff

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "local_parser"))

import date_c


def streamline(date):

    # where we get the input
    mDir = "biz_day/data/input/"

    # where we put the output
    mOutputDir = "biz_day/data/output/"

    mLoanFile = {
        "GNMA_MBS_LL_MON_" + date + "_002.txt",
        "GNMA_MBS_LL_MON_" + date + "_001.txt",
        "dailyllmni.txt",
    }

    prev_month = month.prev_month(date)

    mLoanDQFile = {"llpaymhist_" + prev_month + ".txt"}

    oFilename = "GNMAStreamliner.txt"

    data_path = mOutputDir + oFilename

    # need to check on this month.... well probably not... it will just be a month ahead of time when did I work
    # this into my stored procedures... have a bague memory of it

    next_month = month.next_month(date)

    next_month = date_c.date_conv(next_month)

    # print(next_month)

    #########################################################

    MissingLoan = 0
    #
    #    Program 2
    print("Running...")

    NameMap = {}
    PoolMap = {}
    Count = 0.0
    mCount = 0.0
    MissingWalaCount = 0.0
    MissingWacCount = 0.0

    mMissingCusipSet = {""}

    mCount2 = 0
    mBuffer = 0
    mCount3 = 0
    mCount4 = 0

    LoanSet = set()

    for i in mLoanDQFile:
        ginnieFile = open(mDir + i, "r")

        lines = ginnieFile.readlines()[1:]

        for line in lines:

            mInclude = True
            if line[0:2] == "LL":
                mCount2 += 1
                mLine = line.split("|")

                #            if mLine[1] not in LoanMap  :
                #               #I Removed 1st 2 columns
                #              LoanMap[mLine[1]] = [0]

                # Need to decide something regarding Jumbos
                mNoStreamLine = False
                # Below 6 months can not refi
                if len(mLine[4]) < 10:
                    mNoStreamLine = True
                    Count += 1
                # Need to check that last 5 months are clean
                else:
                    mString = mLine[4]
                    mString = mString[0:10]
                    if float(mString) != 0:
                        mCount3 += 1
                        mNoStreamLine = True
                # If we got here than at least 5 months clean
                mLen = len(mLine[4])
                if mNoStreamLine == False and mLen > 11:
                    mTot = 0
                    mBuffer = 12
                    mString = mLine[4]
                    if mLen > 22:
                        mLen = 22
                    while mBuffer < mLen - 1:
                        mTot += float(mString[mBuffer : mBuffer + 2])
                        mBuffer += 2
                    if mTot > 1:
                        mCount4 += 1
                        mNoStreamLine = True
                if mNoStreamLine:
                    LoanSet.add(mLine[2])
            else:
                mCount += 1

        ginnieFile.close()

    # If the loan is DQ or less than 6month can't streamline

    print("Intial Month Done.")

    print("Not a loan")
    print(mCount)

    print("Total Loan Count")
    print(mCount2)

    print("Number of no stream line loans")
    print(len(LoanSet))

    print("Less than 6 months old")
    print(Count)

    print("One missed in last 6")
    print(mCount3)

    print("One missed in last 6-12")
    print(mCount4)

    print("Math check")
    print(len(LoanSet) - mCount4 - mCount3 - Count)

    # Missing
    # Figure out how to grab balances for 0-6 wala
    # Compute the CPRs
    mCount = 0
    for i in mLoanFile:
        ginnieFile = open(mDir + i, "r")

        lines = ginnieFile.readlines()[1:]

        for line in lines:
            if line[0:1] == "L":
                mPool = line[1:7]
                mAgy = line[21:22]
                mID = line[7:17]

                mAgy = line[21:22]

                cBal = 0
                try:
                    # This number is left blank for the first 6 months.
                    cBal = float(line[67:78])
                except:
                    cBal = 0
                    #                mMissingBal1 += 1
                    # The back up number is missing for 3 loans
                    try:
                        # Back up number in case
                        cBal = float(line[56:67])
                    except:
                        cBal = 0
                        mCount += 1

                if mPool not in PoolMap:
                    PoolMap[mPool] = [0, 0, 0, 0, 0, 0, 0, 0]
                if mAgy == "F":
                    mBuffer = 0
                if mAgy == "V":
                    mBuffer = 1
                if mAgy == "R":
                    mBuffer = 2
                if mAgy == "N":
                    mBuffer = 3

                mNoStreamLine = False
                if line[87:88] != "0":
                    mNoStreamLine = True
                if mID in LoanSet:
                    mNoStreamLine = True

                mAge = 100
                try:
                    mAge = float(line[81:84])
                except:
                    mAge = 100
                if mAge < 7:
                    mNoStreamLine = True

                PoolMap[mPool][mBuffer] += cBal
                if mNoStreamLine:  # or line[87:88] != '0' or  float(line[81:84]) < 1 :
                    PoolMap[mPool][mBuffer + 4] += cBal
        ginnieFile.close()

    print("Loan Files Complete.")
    print("Missing Loan Bal")
    print(mCount2)

    print("Program Complete.")

    outputFile = open(mOutputDir + oFilename, "w")

    for key in PoolMap:
        valList = [str(elem) for elem in PoolMap[key]]
        print(str(key) + "," + ",".join(valList), file=outputFile)

    outputFile.close()

    outputFile = open(mOutputDir + "Mikey_" + oFilename, "w")

    print("Pool ID, FHA, VA", file=outputFile)

    for key in PoolMap:
        if PoolMap[key][0] > 0:
            mFHA = PoolMap[key][4] / PoolMap[key][0]
        else:
            mFHA = -1
        if PoolMap[key][1] > 0:
            mVA = PoolMap[key][5] / PoolMap[key][1]
        else:
            mVA = -1
        print(str(key) + ",%.3f , %.3f" % (mFHA, mVA), file=outputFile)

    outputFile.close()

    #################################################################

    # 1st file read in, getting it ready for the database

    with open(mOutputDir + "Mikey_" + oFilename, newline="") as csvfile:
        next(csvfile)
        data = list(csv.reader(csvfile, delimiter=","))

        head = []

        for row in data:

            name = row[0]
            fha = row[1].strip()
            va = row[2].strip()

            head.append([name, fha, va, next_month])

    headfields = ["name", "fha_2", "va_2", "date"]

    # spit out

    with open(mOutputDir + "fhava_2.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(headfields)

        # writing the data rows
        csvwriter.writerows(head)

    return next_month


# ##################################################################
# #######################################################################

# streamline("202502")
