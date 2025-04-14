import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from conn_dets import conn


def add_cprs6th(date):
    print("-------------------------------")
    print("Starting database stuff")

    # magic stuff I don't really undertand and I should learn
    conn.autocommit = True
    cursor = conn.cursor()

    date = "'" + date + "'"

    # delete old cprs
    sql = (
        """
    DELETE FROM actualcprs
    WHERE date = """
        + date
        + """;
    """
    )

    cursor.execute(sql)

    # create temp table
    sql = """
    create temporary table cpr (cusip varchar, cpr double precision );
    """
    cursor.execute(sql)

    # should read in the newly created cvs doc inot our temp table
    csv_file_name = "biz_day\data\output\SMMTest.txt"

    sql = "COPY cpr FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    # use temp table to insert info into real table
    # why is it cpr/100
    sql = (
        """
    INSERT INTO actualcprs (cusip, actualcpr, date)
    SELECT cusip, cpr/100, """
        + date
        + """
    FROM cpr;

    DROP table cpr
    """
    )

    cursor.execute(sql)

    sql = """
    SELECT * FROM actualcprs order by date desc limit 5;
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        for column in row:
            print(column, end=", ")
        print()

    sql = (
        """
    SELECT COUNT(*) FROM actualcprs where date =  """
        + date
        + """ ;
    """
    )
    cursor.execute(sql)
    records = cursor.fetchall()

    print("\ncount = ", records[0][0])

    conn.commit()
    # conn.close()

    print("intial CPRs ereased official cprs added")


#########################################################################################################
#########################################################################################################
# testing

# add_cprs6th("2025-02-01")
