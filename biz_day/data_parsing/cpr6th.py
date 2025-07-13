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


# all the 6th day stuff
def cprs6thAll(date):

    # download the files, we should already have some but does not seem to hurt to download them again
    # I guess ideally you would check first... may add that later
    if not (os.path.exists("biz_day/data/input/nimonSFPS_" + date + ".txt")):
        gm_extractor.download_unzip_gm("nimonSFPS_" + date)

    # need a better way to check both monthlySPFS
    gm_extractor.download_unzip_gm("monthlySFPS_" + date)

    prev_month = month.prev_month(date)

    gm_extractor.download_unzip_gm("monthlySFPS_" + prev_month)

    # process the data
    cprsFinal.cprs6th(date)

    # add to database
    date_db = date_c.date_conv(date)
    db_cpr6th.add_cprs6th(date_db)


# cprs6thAll("202503")
