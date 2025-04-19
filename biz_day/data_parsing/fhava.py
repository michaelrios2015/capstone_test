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


def fhavaAll(date):

    gm_extractor.download_unzip_gm("dailyllmni")
    # ideally I would tell these last two to wait
    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_001.txt")):
        gm_extractor.download_unzip_gm("llmon1_" + date)

    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_002.txt")):
        gm_extractor.download_unzip_gm("llmon2_" + date)

    # process data
    fhava_file.fhava(date)

    # add to database
    date_db = date_c.date_conv(date)
    db_fhava.add_fhava(date_db)


# fhavaAll("202503")
