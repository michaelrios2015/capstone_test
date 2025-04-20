import csv


def pasre_feds(date):

    data_path = "biz_day/data/input/fedHoldings" + date + ".csv"

    with open(data_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        output = []

        for row in reader:
            isaggregated = False

            if row["is Aggregated"] == "Y":
                isaggregated = True
            output.append(
                [
                    row["As Of Date"],
                    eval(row["CUSIP"]),
                    row["Current Face Value"],
                    isaggregated,
                ]
            )

    fields = ["asofdate", "cusip", "currentfacevalue", "isaggregated"]

    with open("biz_day/data/output/fed.cvs", "w", newline="") as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(output)


############# TESTING #################

# date = "2025-04-02"
# pasre_feds(date)
