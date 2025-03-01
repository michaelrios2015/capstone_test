import csv


def parse_plats(date):

    data_path = "data\input\platmonPPS_" + date + ".txt"

    date = data_path[-10:-6] + "-" + data_path[-6:-4] + "-01"

    # reads in ginnie files take what i need and orders it
    with open(data_path, newline="") as csvfile:
        data = list(csv.reader(csvfile, delimiter="|"))
        # reader = csv.DictReader(csvfile, delimiter='|')

        head = []
        body = []

        # i = 0

        for row in data:
            if row[0] == "PS":
                head.append([row[1], row[2], row[4], row[5], row[7], row[8]])

                body.append(
                    [
                        row[1],
                        row[6],
                        row[9],
                        row[10],
                        row[16],
                        row[17],
                        row[18],
                        "",
                        "",
                        "",
                        date,
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ]
                )

    # spits out cvs files
    headfields = ["cusip", "name", "type", "issuedate", "maturitydate", "originalface"]

    with open("data/output/platinums.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(headfields)

        # writing the data rows
        csvwriter.writerows(head)

    # print(body)

    bodyFields = [
        "cusip",
        "interestrate",
        "remainingbalance",
        "factor",
        "gwac",
        "wam",
        "wala",
        "indicator",
        "istbaelig",
        "cpr",
        "date",
        "cdr",
        "predictedcpr",
        "predictedcprnext",
        "predictedcdr",
        "predictedcdrnext",
        "cprnext",
        "cdrnext",
    ]

    with open("data/output/platinumbodies.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(bodyFields)

        # writing the data rows
        csvwriter.writerows(body)


##############################################################################
################################################################################
#  TESTING STUFF

# parse_plats("202412")
