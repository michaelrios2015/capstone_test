import sys
import os
import time


# oh so you always need to include the below folder
sys.path.append(os.path.join(os.path.dirname(__file__), "data_parsing"))
sys.path.append(os.path.join(os.path.dirname(__file__), "data_parsing", "local_parser"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader", "days_db"))
sys.path.append(os.path.join(os.path.dirname(__file__), "data_parsing", "davids"))

# print(sys.path)

from data_parsing import *
from days_db import *
from db_loader import *
from local_parser import *
from davids import month


def fourthAll(date, fed_date):

    # so on the 4th business day
    # we calcalulate the intial CPRS and add them to the database
    cpr4th.cprs4thAll(date)

    fhava4th.fhava4thAll(date)

    # still processing from the previous month
    prev_month = month.prev_month(date)

    # convert date to date for database
    prev_month = date_c.date_conv(prev_month)

    # Then process our data for the website, this is a stored procedure in my database
    procGinnies.proc_ginnies(prev_month, fed_date)

    # Erase the ginnes
    truncate.deleteGinnies()

    # ##########################################################################################
    # ADD THE ginnies back

    ginnies.addGinnies()

    dailys.addDailies()

    firstDay.addFirstDay()


# date is the month we are getting data, which is month-1 like normal
date = "202507"
# will just calculate this by hand for now
fed_date = "2025-07-02"

fourthAll(date, fed_date)
