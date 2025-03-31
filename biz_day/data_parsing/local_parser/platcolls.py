import csv
import date_c


def parser_platcolls(date):

    file = "biz_day\data\input\platcoll_" + date + ".txt"

    # this extraxts what we needs
    # Using readlines()
    file1 = open(file, "r")
    Lines = file1.readlines()

    data = []

    # this the the date that will go into the database
    date = date_c.date_conv(date)

    # print(date)

    i = 0

    for row in Lines:
        # print(row)
        # print(row[0:9], row[19:25], row[25:26], row[53:68], row[79:80], date)
        data.append([row[0:9], row[19:25], row[25:26], row[53:68], row[79:80], date])

    # so seems to work would put in a temp table then switch to

    fields = ["cusip", "poolname", "indicator", "faceinplatinum", "active", "date"]

    with open("biz_day/data/output/platcolls.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(data)


##############################################################################
################################################################################
#  TESTING STUFF

# parser_platcolls("202501")
