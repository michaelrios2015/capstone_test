import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def add_prepay(date):

    # connects to database
    from conn_dets import conn

    # connecting to database
    # what is autocommit
    conn.autocommit = True
    cursor = conn.cursor()

    date = "'" + date + "'"

    # delete FHAVA_CPR this is only done so I can rerun the program for testing purposes
    sql = (
        """
    DELETE FROM fhava_cpr
    WHERE date = """
        + date
        + """;
    """
    )

    cursor.execute(sql)

    # read in fhava_cpr's
    csv_file_name = "biz_day/data/output/fhava_cpr.cvs"
    sql = "COPY fhava_cpr FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    ########################################################
    # 2nd part
    #################################################

    print("fhava_cpr")
    print("----------------------------------")
    sql = """
    SELECT * FROM fhava_cpr order by date desc limit 5;
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        for column in row:
            print(column, end=", ")
        print()

    sql = (
        """
    SELECT COUNT(*) FROM fhava_cpr where date =  """
        + date
        + """;
    """
    )
    cursor.execute(sql)
    records = cursor.fetchall()

    print("\ncount = ", records[0][0])

    conn.commit()


########################################################################################
########################################################################################

# date = "2025-07-1"
# add_prepay(date)
