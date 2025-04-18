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

# so on the first business day
# we download the brand new pools
# which would be the dailySFSPS files

# so for the time being I will just put in the date


def firstAll(date):

    # convert the date to form needed for database
    date = date_c.date_conv(date)

    # print(date)

    file = "dailySFPS"
    # download the new dailys
    getFiles.download_parse_db(file)

    print("downloaded new data")

    # process the new dailies
    # this date is the only one I need... and actually the program can make it
    procDaily.proc_daily(date, "true")

    print("processed new daily pools")

    # Then add this to rge other database

    # ech of these can be a function seems a little like overkill but do mix and match them a bit
    # TRUNCATE ginnies;

    truncate.deleteGinnies()

    print("truncated ginnies")

    ##########################################################################################

    # add all the ginnies to the website database
    ginnies.addGinnies()

    dailys.addDailies()

    firstDay.addFirstDay()

    # print("added all ginnies")


date = "202502"
firstAll(date)
