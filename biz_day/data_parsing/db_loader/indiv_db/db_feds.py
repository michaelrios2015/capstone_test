import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# the connection to the database I was able to centralize
from conn_dets import conn


def add_feds(date):

    conn.autocommit = True
    cursor = conn.cursor()

    # deleting do I can reun for testing purposes
    sql = (
        """
        DELETE FROM fedholdings where asofdate =  """
        + "'"
        + date
        + "'"
        + """;
    """
    )
    cursor.execute(sql)

    csv_file_name = "biz_day/data/output/fed.cvs"
    sql = "COPY fedholdings FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    sql = """
    SELECT * FROM fedholdings order by asofdate desc limit 5;
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        for column in row:
            print(column, end=", ")
        print()

    sql = (
        """
    SELECT COUNT(*) FROM fedholdings where asofdate =  """
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


############## TESTING ####################

# date = "2025-04-02"

# add_feds(date)
