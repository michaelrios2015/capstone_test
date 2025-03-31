import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# the connection to the database I was able to centralize
from conn_dets import conn


def add_plats(date):

    # connecting to database
    conn.autocommit = True
    cursor = conn.cursor()

    # getting rid of the fake platniums
    sql = (
        """
    DELETE FROM platinumbodies
    WHERE date = """
        + "'"
        + date
        + "'"
        + """;
    """
    )

    cursor.execute(sql)

    # reading in platinum bodies, very simple
    csv_file_name = "biz_day\data\output\platinumbodies.cvs"
    sql = "COPY platinumbodies FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    # creating temp file for platinum heads
    sql = """
    create temporary table platinumstemp (cusip varchar, name varchar , type varchar, issuedate integer, maturitydate integer, originalface double precision);
    """
    cursor.execute(sql)

    # Putting plat heads into temp file
    csv_file_name = "biz_day\data\output\platinums.cvs"
    sql = "COPY platinumstemp FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    # adding new plat heads ignoring dupes
    sql = """
    INSERT INTO platinums (cusip, name, type, issuedate, maturitydate, originalface)
    SELECT cusip, name, type, issuedate, maturitydate, originalface
    FROM platinumstemp
    ON CONFLICT (cusip)
    DO NOTHING;

    DROP TABLE platinumstemp;
    """

    cursor.execute(sql)

    # printing some so i know they are in there
    print("5 new platinum bodies\n")
    sql = """
    SELECT * FROM platinumbodies order by date desc limit 5;
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        for column in row:
            print(column, end=", ")
        print()

    # the count of the new ones I added
    sql = (
        """
    SELECT COUNT(*) FROM platinumbodies where date =  """
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


###############################################################################
###############################################################################
# testing

# add_plats("2025-01-01")
