import psycopg2

# connects to database
# conn = psycopg2.connect(
#     database="test_cmo",
#     user="postgres",
#     password="JerryPine",
#     host="localhost",
#     port="5432",
# )

from conn_dets import conn

# change this monthly #######################################################


# data_path = "data/input/monthlySFPS_202501.txt"


# date = data_path[-10:-6] + "-" + data_path[-6:-4] + "-01"

# connection.conn

# connection.conn.autocommit = True
# cursor = connection.conn.cursor()

# conn.autocommit = True
# cursor = conn.cursor()


def add_pools(date):
    # connecting to database
    # what is autocommit
    conn.autocommit = True
    cursor = conn.cursor()

    # conn.autocommit = True
    # cursor = conn.cursor()

    date = date + "-01"
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

    print("five of the new poolbodies\n")

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


###############################################################################
###############################################################################
# testing

add_pools("2025-01")
