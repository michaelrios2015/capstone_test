import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# the connection to the database I was able to centralize
from conn_dets import conn


def add_platcoll(date):

    # connecting to database
    # what is autocommit
    conn.autocommit = True
    cursor = conn.cursor()

    sql = """
    create temporary table platcollstemp (cusip varchar, poolname varchar, indicator varchar, faceinplatinum double precision, active varchar, date date);
    """
    cursor.execute(sql)

    csv_file_name = "biz_day\data\output\platcolls.cvs"
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
    # conn.close()


###############################################################################
###############################################################################
# testing

# add_platcoll("2025-01-01")
