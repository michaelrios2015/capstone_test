import month


def cprs6th(date):

    mOutputDir = "biz_day/data/output/"

    # current month for monthlySFPS
    mPoolFile = "monthlySFPS_" + date + ".txt"
    # past month for monthlySFPS
    prev_month = month.prev_month(date)

    mPoolFileOld = {"nimonSFPS_" + date + ".txt", "monthlySFPS_" + prev_month + ".txt"}

    oFilename = "SMMTest.txt"

    mDir = "biz_day/data/input/"
    #
    #    Program 2
    print("Running...")

    # starting david's stuff

    cusipMap = {}
    NameMap = {}
    Count = 0.0
    mMissingCusipSet = {""}

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


###################################################################################################
###################################################################################################
# TEST

# cprs6th("202502")
