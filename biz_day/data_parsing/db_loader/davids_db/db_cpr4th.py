import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# need to send date and probably change it
from conn_dets import conn


def add_cprs4th(date):
    date = "'" + date + "'"

    # magic stuff I don't really undertand and I should learn
    conn.autocommit = True
    cursor = conn.cursor()

    # ereasing so I can test
    sql = (
        """
    DELETE FROM actualcprs
    WHERE date = """
        + date
        + """;
    """
    )

    cursor.execute(sql)

    #################################################

    sql = (
        """
    DELETE FROM actualcdrs
    WHERE date = """
        + date
        + """;
    """
    )

    cursor.execute(sql)

    # create the temp table
    sql = """
    create temporary table cprandcdr (cusip varchar, cpr double precision, cdr double precision );
    """
    cursor.execute(sql)

    # should read in the newly created cvs doc inot our temp table
    csv_file_name = "biz_day\data\output\GNMASMMPrelim.txt"

    sql = "COPY cprandcdr FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    # use temp table to insert info into real table
    sql = (
        """
    INSERT INTO actualcprs (cusip, actualcpr, date)
    SELECT cusip, cpr/100, """
        + date
        + """
    FROM cprandcdr;

    INSERT INTO actualcdrs (cusip, cdr, date)
    SELECT cusip, cdr/100, """
        + date
        + """
    FROM cprandcdr;

    DROP table cprandcdr
    """
    )

    cursor.execute(sql)

    # so this should work fine... but it's hard to test
    # ok so this is for the 4th buisiness day so we don't have the plats yet and
    # we just store them in column called cprnext..
    sql = (
        """
    call actualcprandcdrnext("""
        + date
        + """);
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

    sql = """
    SELECT * FROM platinumbodies order by date desc limit 5;
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        for column in row:
            print(column, end=", ")
        print()

    conn.commit()


#################################################################################################
#################################################################################################

# testing!!!

# add_cprs4th("2025-02-01")
