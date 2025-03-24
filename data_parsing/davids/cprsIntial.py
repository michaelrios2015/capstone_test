import month

# *********************************************************
#       Goal : Use the liquidatd loan file to previous pool file to find
#                   a. CDR of a pool
#                   b. CPR of the pool
#       This means a. Schedule pay from perv. month
#                  b. Actual from this month
#                  c. SMM  calc
#       Note : Various inexact results because
#           a. Pool file has WAM and WALA not actual
#           b. Liquidated loans do not have curtailed mortgages
#           c. Some loans have current face blank and we use O.F.
# *********************************************************


# *********************************************************
#    Some Errors
#    Loans less than 6 age we have rounding issues
#    Loans in forebarence (some are have neg WAM)
#    Loans that pay ahead of schedule and stop paying <--- this is easiest to fix
# *********************************************************


# Now in a function
def cprs4th(date):

    mOutputDir = "data/output/"

    prev_month = month.prev_month(date)

    # These should roll every month
    # these files are changed monthly
    mPoolFileOld = {"nimonSFPS_" + date + ".txt", "monthlySFPS_" + prev_month + ".txt"}
    # today is not the 4th business day tomorrow is the 4th business day so this still needs to be changed
    mLoanFile = {"llmonliq_" + date + ".txt"}

    # Results
    oFilename = "GNMASMMPrelim.txt"

    # *********************
    #
    # NO MORE CHANGE
    #
    # *************************

    # nonething else below this should need to be renamed each month
    # When a loan is paid off does WAM / WALA , UBP change?

    mDir = "data/input/"

    # output\2021-12\GNMASMMPrelimDec.txt
    # print(mOutputDir + oFilename)

    #
    #    Program 2
    print("Running...")

    cusipMap = {}
    CFMissingMap = {}
    Count = 0.0
    mMissingLoanCFSet = {""}
    mPaidLoanSet = {""}
    mCol = 0
    mBuffer = 0
    mMissingCusipSet = {""}

    # Get schedule payment from pool level. Not perfect but we don't have
    # Curtailment in Prelim data

    # All we want from this is scheduled paydowns and to estimate CF
    for i in mPoolFileOld:
        ginnieFile = open(mDir + i, "r")

        for line in ginnieFile:
            lineList = line.split("|")
            if lineList[0] == "PS":
                try:
                    mFactor = float(lineList[10 + mBuffer])
                except:
                    print(lineList[1 + mBuffer] + " : Missing Factor")
                    mMissingCusipSet.add(lineList[1 + mBuffer])
                if mFactor > 0:
                    try:
                        #                OTerm = float(lineList[20+mBuffer])   This uses Orginal Term
                        OTerm = float(lineList[18 + mBuffer])
                    except:
                        mMissingCusipSet.add(lineList[1 + mBuffer])
                    try:
                        WALA = float(lineList[19 + mBuffer])
                        # This switchs it to using current OTERM rather than orig
                        OTerm += float(lineList[19 + mBuffer])

                    except:
                        mMissingCusipSet.add(lineList[1 + mBuffer])
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
                        0,
                        0,
                        0,
                    ]

        ginnieFile.close()

    print("Previous Pool Month Done.")

    # This will be dollar amounts
    for i in mLoanFile:
        ginnieFile = open(mDir + i, "r")
        lines = ginnieFile.readlines()[1:]

        for line in lines:
            #        print(line)

            LineList = line.split("|")
            if LineList[0] == "LR":
                mCusip = LineList[1]
                if mCusip not in cusipMap:
                    print("Oh No")

                try:
                    # This number is left blank for the first 6 months.
                    cBal = float(LineList[13])
                    Count += 1
                except:
                    # I really should reduce for WALA / WAM / WAC
                    cBal = float(LineList[11])
                    # This is here so we can reduce by loan level later if we want
                    CFMissingMap[LineList[6]] = [0]

                mCol = 2
                if float(LineList[14]) > 1 and float(LineList[14]) < 6:
                    mCol += 1
                cusipMap[mCusip][mCol] += cBal

                if LineList[6] in CFMissingMap:
                    CFMissingMap[LineList[6]][0] = mCol

        ginnieFile.close()
    print("Liquidated Loans done")

    SchdRemaining = 1

    for i in cusipMap:
        SchdRemaining = cusipMap[i][0] * (1 - cusipMap[i][1])

        if SchdRemaining > 0:
            SMMV = cusipMap[i][2] / SchdRemaining
            SMMD = cusipMap[i][3] / SchdRemaining

        else:
            SMMV = 0
            SMMD = 0

        if i == "36178DST9":
            print("Unsched V")
            print(cusipMap[i][2])
            print("Unsched D")
            print(cusipMap[i][3])
            print("Unsched Total")
            print(cusipMap[i][2] + cusipMap[i][3])

        cusipMap[i][4] = (1 - (1 - SMMV - SMMD) ** 12) * 100
        cusipMap[i][5] = (1 - (1 - SMMV) ** 12) * 100
        cusipMap[i][6] = (1 - (1 - SMMD) ** 12) * 100

    print("CDRs / CPRs calculated")

    outputFile = open(mOutputDir + oFilename, "w")
    for key in cusipMap:
        valList = [str(elem) for elem in cusipMap[key]]
        #   print(str(key) + ',' + ','.join(valList), file = outputFile)
        print(str(key) + "," + valList[4] + "," + valList[6], file=outputFile)
    outputFile.close()

    print("Program Complete.")


# cprs4th("202502")
