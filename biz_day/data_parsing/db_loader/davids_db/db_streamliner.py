import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# connects to database
from conn_dets import conn


def add_streamliner(date):

    # connecting to database
    # what is autocommit
    conn.autocommit = True
    cursor = conn.cursor()

    # so how to I get this date...

    date = "'" + date + "'"

    # delete FHAVA_2 this is only done so I can rerun the program for testing purposes
    sql = (
        """
    DELETE FROM fhava_2
    WHERE date = """
        + date
        + """;
    """
    )

    cursor.execute(sql)

    # read in fhava_2's 1st one
    csv_file_name = "biz_day/data/output/fhava_2.cvs"

    sql = "COPY fhava_2 FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    # Just want to make sure it's there
    print("fhava_2")
    print("----------------------------------")
    sql = """
    SELECT * FROM fhava_2 order by date desc limit 5;
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        for column in row:
            print(column, end=", ")
        print()

    sql = (
        """
    SELECT COUNT(*) FROM fhava_2 where date =  """
        + date
        + """;
    """
    )
    cursor.execute(sql)
    records = cursor.fetchall()

    print("\ncount = ", records[0][0])


# ##################################################################
# #######################################################################

# add_streamliner("2025-03-01")
