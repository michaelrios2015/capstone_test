import sys
import os
import datetime

# so I need to tell it to work... so I have a subfolder

sys.path.append(os.path.join(os.path.dirname(__file__), "ginnie_extract"))
# so need this but don't seem to need to import from db_loader for conn_dets
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader"))
sys.path.append(os.path.join(os.path.dirname(__file__), "local_parser"))
sys.path.append(os.path.join(os.path.dirname(__file__), "davids"))


# print(sys.path)
# we import everything from the subfolders
from ginnie_extract import *
from local_parser import *
from davids import *
from davids_db import *


# so here I have all the elements of a function for the four day cprs


# we want to just give it a date and the program does the rest!!
def cprs4thAll(date):
    # get data
    # so these are working fine, technically we also need the
    if not (os.path.exists("biz_day/data/input/llmonliq_" + date + ".txt")):
        gm_extractor.download_unzip_gm("llmonliq_" + date)

    if not (os.path.exists("biz_day/data/input/nimonSFPS_" + date + ".txt")):
        gm_extractor.download_unzip_gm("nimonSFPS_" + date)

    # we should already have this but including it just in case
    prev_month = month.prev_month(date)

    # need a better way to check
    gm_extractor.download_unzip_gm("monthlySFPS_" + prev_month)

    # here we process the data
    cprsIntial.cprs4th(date)

    # date for the database
    date_db = date_c.date_conv(date)

    # the database part will only run once
    db_cpr4th.add_cprs4th(date_db)


# cprs4thAll("202503")
