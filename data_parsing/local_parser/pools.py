import csv
from datetime import datetime


def parse_pools(date):

    data_path = "data/input/monthlySFPS_" + date + ".txt"

    date = data_path[-10:-6] + "-" + data_path[-6:-4] + "-01"

    with open(data_path, newline="") as csvfile:
        data = list(csv.reader(csvfile, delimiter="|"))
        # reader = csv.DictReader(csvfile, delimiter='|')

        head = []
        body = []

        for row in data:
            if row[0] == "PS":
                maturitydate = row[7]
                issuedate = row[5]

                # print(issuedate)
                # print(int(issuedate[0:4]))
                # print(int(issuedate[4:6]))
                # print(int(issuedate[6:8]))

                end_date = datetime(
                    int(maturitydate[0:4]),
                    int(maturitydate[4:6]),
                    int(maturitydate[6:8]),
                )
                start_date = datetime(
                    int(issuedate[0:4]), int(issuedate[4:6]), int(issuedate[6:8])
                )

                num_months = (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month
                )

                istbaelig = False

                indicator = row[3]
                type = row[4]
                originalface = int(row[8])

                if (
                    originalface >= 250000
                    and type == "SF"
                    and (indicator == "X" or indicator == "M")
                    and num_months >= 336
                ):
                    istbaelig = True

                head.append(
                    [
                        row[1],
                        row[2],
                        indicator,
                        type,
                        row[5],
                        row[7],
                        originalface,
                        istbaelig,
                    ]
                )

                body.append(
                    [row[1], row[6], row[9], row[10], row[17], row[18], row[19], date]
                )

    headfields = [
        "cusip",
        "name",
        "indicator",
        "type",
        "issuedate",
        "maturitydate",
        "originalface",
        "istbaelig",
    ]

    with open("data/output/pools.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(headfields)

        # writing the data rows
        csvwriter.writerows(head)

    bodyFields = [
        "cusip",
        "interestrate",
        "remainingbalance",
        "factor",
        "gwac",
        "wam",
        "wala",
        "date",
    ]

    with open("data/output/poolbodies.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(bodyFields)

        # writing the data rows
        csvwriter.writerows(body)


parse_pools("202412")
