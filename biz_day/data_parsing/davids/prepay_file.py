import os
import csv
import month
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "local_parser"))

import date_c


def prepay(date):
    # where imput and output files are kept
    mDir = "biz_day/data/input/"

    prev_month = month.prev_month(date)

    # Files published 6th business day of month n and the last file published the last business day of month n
    mLoanFileOld = {
        # two from the past month
        "GNMA_MBS_LL_MON_" + prev_month + "_001.txt",
        "GNMA_MBS_LL_MON_" + prev_month + "_002.txt",
        # this is the current month
        "dailyllmni.txt",
    }

    # Files published 6th business day of month n+1
    # current month
    mLoanFile = {
        "GNMA_MBS_LL_MON_" + date + "_001.txt",
        "GNMA_MBS_LL_MON_" + date + "_002.txt",
    }

    # fine names
    oFilename = "GNMAPoolCohortSMMTest.txt"

    mOutputDir = "biz_day/data/output/"

    # this is a month ahead... because there was some mix up with the months a while back
    # should probably revisit at some point

    next_month = month.next_month(date)

    next_month = date_c.date_conv(next_month)

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

            head.append([name, fha_cpr, va_cpr, next_month])

    headfields = ["name", "fha_cpr", "va_cpr", "date"]

    with open(mOutputDir + "fhava_cpr.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(headfields)

        # writing the data rows
        csvwriter.writerows(head)

    # will use for database
    return next_month


# #################################################################################
# # Testing
# ##############################################################################

# prepay("202503")
