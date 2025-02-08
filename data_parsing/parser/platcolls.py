import csv
import psycopg2
from zipfile import ZipFile
import io
import requests

# connects to database
conn = psycopg2.connect(
    database="cmos_builder",
    user="postgres",
    password="JerryPine",
    host="localhost",
    port="5432",
)

#  So I seem to be able to read in the platcolls just fine
# but inserting it might be a bit trickier.. that will be seen in laoding scripts section


# change these two monthly
data_url = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/platcoll_202412.zip"

file = "data\input\platcoll_202412.txt"

############################################################################

# # this gets the data and saves it
# r = requests.get(data_url)  # create HTTP response object

# # print(r.content)
# # extract file
# z = ZipFile(io.BytesIO(r.content))
# # send it to data
# z.extractall("data\input")

# # z.extractall()

# this extraxts what we needs
# Using readlines()
file1 = open(file, "r")
Lines = file1.readlines()

data = []

# date = (sys.argv[1])[-10:-6] + '-' + (sys.argv[1])[-6:-4] + '-01'
date = file[-10:-6] + "-" + file[-6:-4] + "-01"

# print(date)

i = 0


for row in Lines:
    # print(row)
    # print(row[0:9], row[19:25], row[25:26], row[53:68], row[79:80], date)
    data.append([row[0:9], row[19:25], row[25:26], row[53:68], row[79:80], date])


# so seems to work would put in a temp table then switch to

fields = ["cusip", "poolname", "indicator", "faceinplatinum", "active", "date"]

with open("data/output/platcolls.cvs", "w", newline="") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(data)


# connecting to database
# what is autocommit
conn.autocommit = True
cursor = conn.cursor()

sql = """
create temporary table platcollstemp (cusip varchar, poolname varchar, indicator varchar, faceinplatinum double precision, active varchar, date date);
"""
cursor.execute(sql)

csv_file_name = "data\output\platcolls.cvs"
sql = "COPY platcollstemp FROM STDIN DELIMITER ',' CSV HEADER"
cursor.copy_expert(sql, open(csv_file_name, "r"))


sql = """
INSERT INTO platcolls(cusip, poolname, indicator, faceinplatinum, active, born)
SELECT cusip, poolname, indicator, faceinplatinum, active, date
FROM platcollstemp
ON CONFLICT DO NOTHING;
"""
cursor.execute(sql)

# should not be necessay but does not hurt
sql = """
UPDATE platcolls
SET terminated = born
WHERE active = 'T'
AND terminated IS NULL;
"""
cursor.execute(sql)

sql = """
UPDATE platcolls
SET terminated = date,
    active = 'T'
FROM platcollstemp
WHERE platcolls.cusip = platcollstemp.cusip
AND platcolls.poolname = platcollstemp.poolname
AND platcolls.indicator = platcollstemp.indicator
AND platcolls.active = 'A'
AND platcollstemp.active = 'T';


DROP table platcollstemp;
"""

cursor.execute(sql)

sql = """
SELECT * FROM platcolls where terminated is not null order by terminated desc limit 5;
"""
cursor.execute(sql)
records = cursor.fetchall()

for row in records:
    for column in row:
        print(column, end=", ")
    print()


sql = """
SELECT * FROM platcolls where born is not null order by born desc limit 5;
"""
cursor.execute(sql)
records = cursor.fetchall()

for row in records:
    for column in row:
        print(column, end=", ")
    print()


conn.commit()
conn.close()
