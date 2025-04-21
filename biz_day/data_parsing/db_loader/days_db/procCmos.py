import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_dets import conn


# uses stored procedure to process cmos
def proc_cmos(date):

    conn.autocommit = True
    cursor = conn.cursor()

    # so how to I get this date...

    date = "'" + date + "'"

    # addes in ming plat data
    sql = (
        """
            call  allcmostoredprocedure("""
        + date
        + """);

        """
    )

    cursor.execute(sql)

    conn.commit()

    print("processed cmos")
