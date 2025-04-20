import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "ginnie_extract"))
sys.path.append(os.path.join(os.path.dirname(__file__), "local_parser"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader", "indiv_db"))

import getFed
import feds
import db_feds


def fed_all(date):

    # get data from feds
    getFed.get_fed(date)

    # # parse the data
    feds.pasre_feds(date)

    # # Put it in the database
    db_feds.add_feds(date)


############# TESTING ####################

# fed_all("2025-04-02")
