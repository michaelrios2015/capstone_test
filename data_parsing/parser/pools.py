import csv
import psycopg2
from zipfile import ZipFile
import io
import requests
from datetime import datetime

# connects to database
conn = psycopg2.connect(
    database="cmos_builder",
    user="postgres",
    password="JerryPine",
    host="localhost",
    port="5432",
)

# change this monthly #######################################################

# this one for the monthly one
# data_url = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/monthlySFPS_202412.zip"

# this for the daily
# data_url = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/dailySFPS.zip"

data_path = "data/input/monthlySFPS_202502.txt"


# r = requests.get(data_url)  # create HTTP response object

# z = ZipFile(io.BytesIO(r.content))

# zipinfos = z.infolist()


# # so for the dailys i need to rename it  #################################################
# zipinfos[0].filename = "monthlySFPS_202310.txt"

# ###########################################################################
# z.extract(zipinfos[0], "data/input")


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
                int(maturitydate[0:4]), int(maturitydate[4:6]), int(maturitydate[6:8])
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


# connecting to database
# what is autocommit
conn.autocommit = True
cursor = conn.cursor()

# so if first need to delete the poolbodies from the current month, this will usually do nothing
# but is needed as I add the daily files
sql = (
    """
DELETE FROM poolbodies
WHERE date = """
    + "'"
    + date
    + "'"
    + """;
"""
)
cursor.execute(sql)

# then just read new poolbodies
csv_file_name = "data\output\poolbodies.cvs"
sql = "COPY poolbodies FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))

# make a temp table for the pools
sql = """
create temporary table poolstemp (cusip varchar, name varchar , indicator varchar, type varchar, issuedate integer, maturitydate integer, originalface double precision, istbaelig boolean);
"""
cursor.execute(sql)

# read in new pools into the temp file
csv_file_name = "data\output\pools.cvs"
sql = "COPY poolstemp FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


# add new ones update old ones even though for the most part the update will be the same
# so before we could just ignore duplicates because nothing changed but with the daily files things can change so I am just updating everything
# it's not elegent but it does not take very long
sql = """
INSERT INTO pools (cusip, name, indicator, type, issuedate, maturitydate, originalface, istbaelig)
SELECT cusip, name, indicator, type, issuedate, maturitydate, originalface, istbaelig
FROM poolstemp
ON CONFLICT (cusip) DO UPDATE
SET name = EXCLUDED.name, indicator = EXCLUDED.indicator, type = EXCLUDED.type,
issuedate = EXCLUDED.issuedate, maturitydate = EXCLUDED.maturitydate, originalface = EXCLUDED.originalface,
istbaelig = EXCLUDED.istbaelig;

DROP TABLE poolstemp;
"""

cursor.execute(sql)


sql = """
SELECT * FROM poolbodies order by date desc limit 5;
"""
cursor.execute(sql)
records = cursor.fetchall()

for row in records:
    for column in row:
        print(column, end=", ")
    print()


sql = (
    """
SELECT COUNT(*) FROM poolbodies where date =  """
    + "'"
    + date
    + "'"
    + """;
"""
)
cursor.execute(sql)
records = cursor.fetchall()

print("\ncount = ", records[0][0])


conn.commit()
conn.close()
