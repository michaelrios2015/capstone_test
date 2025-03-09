import sys
import os
import datetime

# so I need to tell it to work... so I have a subfolder
sys.path.append(os.path.join(os.path.dirname(__file__), "ginnie_extract"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader"))
sys.path.append(os.path.join(os.path.dirname(__file__), "local_parser"))

# print(sys.path)
# we import everything from the subfolders
from ginnie_extract import *
from local_parser import *
from db_loader import *


# putting them all togther
def download_parse_db(file):

    # so if it's a dailySPFS we will get the date from the daily function
    date = gm_extractor.download_unzip_gm(file)

    # here we just check and if it is not daily then we get the name and date from the file
    if file != "dailySFPS":
        name, date = file.split("_")
        # print(name, date)
    # it is a daily so just intailize name to monthSFPS, and it will be fine because date is different
    else:
        name = "monthlySFPS"
        # print(name, date)

    # date for the database
    date_db = date_c.date_conv(date)

    # and we have three options
    if name == "platmonPPS":
        # we parse the data,
        platinums.parse_plats(date)
        # then put data into database
        db_plats.add_plats(date_db)
    elif name == "monthlySFPS":
        # should work for dailys as well same thing just different dates
        pools.parse_pools(date)
        db_pools.add_pools(date_db)
    elif name == "platcoll":
        platcolls.parser_platcolls(date)
        db_platcolls.add_platcoll(date_db)


# seems to work, not sure why it did noty work when just put in a for loop..
# that may come back to haught me at some point
file = "monthlySFPS_202501"
# file = "platmonPPS_202501"
# file = "platcoll_202501"
# file = "dailySFPS"

# download_parse_db(file)
