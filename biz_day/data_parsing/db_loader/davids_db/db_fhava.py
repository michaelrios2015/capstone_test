import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# connects to database
from conn_dets import conn


def add_fhava(date):
    # magic stuff I don't really undertand and I should learn
    conn.autocommit = True
    cursor = conn.cursor()

    date = "'" + date + "'"

    # delete FHAVAs this is only done so I can rerun the program for testing purposes
    sql = (
        """
    DELETE FROM poolfhavas
    WHERE date = """
        + date
        + """;
    """
    )

    cursor.execute(sql)

    # create the temp table
    # apperntly the va are in the second column, and fha in the third... since the table was built the opposite
    # way I read them in va, fha and then switch them later
    sql = """
    create temporary table tempfhava (cusip varchar, va double precision, fha double precision, rural double precision, indian double precision);
    """
    cursor.execute(sql)

    # should read in the newly created cvs doc inot our temp table
    csv_file_name = "biz_day/data/output/FHAVATest.txt"
    sql = "COPY tempfhava FROM STDIN DELIMITER ',' CSV HEADER"
    cursor.copy_expert(sql, open(csv_file_name, "r"))

    # use temp table to insert info into real table
    sql = (
        """
    INSERT INTO poolfhavas (cusip, fha, va, rural, indian, date)
    SELECT cusip, fha, va, rural, indian, """
        + date
        + """
    FROM tempfhava;

    DROP TABLE tempfhava;
    """
    )

    cursor.execute(sql)

    sql = """
    SELECT * FROM poolfhavas order by date desc limit 5;
    """
    cursor.execute(sql)
    records = cursor.fetchall()

    for row in records:
        for column in row:
            print(column, end=", ")
        print()

    sql = (
        """
    SELECT COUNT(*) FROM poolfhavas where date =  """
        + date
        + """ ;
    """
    )
    cursor.execute(sql)
    records = cursor.fetchall()

    print("\ncount = ", records[0][0])

    conn.commit()
    # conn.close()


#########################################################################################################
#########################################################################################################
# testing

# add_fhava("2025-02-01")
