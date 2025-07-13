# david's code for the regular fhava stuff


def fhava(date):

    mDir = "biz_day/data/input/"

    # LoanFile = 'GNMA_MBS_LL_MON_202103_002.txt'
    LoanFile = {
        "dailyllmni.txt",
        "GNMA_MBS_LL_MON_" + date + "_002.txt",
        "GNMA_MBS_LL_MON_" + date + "_001.txt",
    }
    # LoanFile = {'dailyll_new.txt', 'GNMA_MBS_LL_MON_202110_002.txt', 'GNMA_MBS_LL_MON_202110_001.txt' }

    # mPoolFile2 = 'dailySFPS.txt'
    # should jusr be for output
    directory = "biz_day/data/output/"

    # SpeedFile = "D:\Mortgage Project\Dolan\\ginnie_202102_monthly_predictions_roll.csv"  Speed File

    oFilename = "FHAVATest.txt"

    # print(date)
    # *********************
    #
    # NO MORE CHANGE
    #
    # *************************

    # date = "'" + "2025-02" + "-01" + "'"

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


#############################################################################################
#############################################################################################
# test

# fhava("202502")
