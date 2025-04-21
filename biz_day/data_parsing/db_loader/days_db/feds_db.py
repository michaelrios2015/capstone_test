import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_dets import conn


# the fed current face is processed in two differnt way
# the third varibale, called first, is a boolen to choose which way
def proc_feds(date, fed_date, first):

    conn.autocommit = True
    cursor = conn.cursor()

    date = "'" + date + "'"

    fed_date = "'" + fed_date + "'"

    # addes in ming plat data
    if first:
        sql = (
            """    
            Call fedholdingscurrface("""
            + date
            + """, """
            + fed_date
            + """);
            """
        )
        print("before 15th")
    else:
        sql = (
            """    
            Call fedholdingsCurrfaceGinnie2("""
            + date
            + """, """
            + fed_date
            + """);
            """
        )
        print("After 15th")

    cursor.execute(sql)

    conn.commit()

    print("processed feds")
