import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# connects to database
from conn_two import connTwo


# # just here for testing
# import truncate

# truncate.deleteGinnies()


def float_sum(date):

    connTwo.autocommit = True
    cursorTwo = connTwo.cursor()

    date = "'" + date + "'"

    # deleting not always needed but just easier to include
    sql = (
        """
    DELETE FROM sumoffloats
    WHERE date = """
        + date
        + """;
    """
    )

    cursorTwo.execute(sql)

    #################################################################

    # Calculate the float
    sql = (
        """
        call get_float_sum("""
        + date
        + """);
        """
    )

    cursorTwo.execute(sql)

    connTwo.commit()

    print("float calculated")


# testing
