import sys
import os
import time


# oh so you always need to include the below folder
sys.path.append(os.path.join(os.path.dirname(__file__), "data_parsing"))
sys.path.append(os.path.join(os.path.dirname(__file__), "data_parsing", "local_parser"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader", "days_db"))

# print(sys.path)

from data_parsing import *
from days_db import *
from db_loader import *
from local_parser import *


def fourthAll(date, fed_date):

    # so on the 4th business day
    # we calcalulate the intial CPRS and add them to the database
    cpr4th.cprs4thAll(date)

    # convert date to date for database
    date = date_c.date_conv(date)

    # Then process our data for the website, this is a stored procedure in my database
    procGinnies.proc_ginnies(date, fed_date)

    # Erase the ginnes
    truncate.deleteGinnies()

    # ##########################################################################################
    # ADD THE ginnies back

    ginnies.addGinnies()

    dailys.addDailies()

    firstDay.addFirstDay()


date = "202503"
# will just calculate this by hand for now
fed_date = "2025-04-02"

fourthAll(date, fed_date)
