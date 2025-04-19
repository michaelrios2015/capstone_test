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


# streamline


def streamlinerAll(date):

    # see if we have files, if not get them
    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_001.txt")):
        gm_extractor.download_unzip_gm("llmon1_" + date)

    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_002.txt")):
        gm_extractor.download_unzip_gm("llmon2_" + date)

    # this can only be the newest one...
    gm_extractor.download_unzip_gm("dailyllmni")

    # this last file is from the previouys month
    prev_month = month.prev_month(date)

    if not (os.path.exists("biz_day/data/input/llpaymhist_" + prev_month + ".txt")):
        gm_extractor.download_unzip_gm("llpaymhist_" + prev_month)

    # process data and get next month
    next_month = streamline_file.streamline(date)

    # print(next_month)

    # put it into the database as one month ahead,
    # not sure if this is completely right but is how the database is currently set up
    db_streamliner.add_streamliner(next_month)


# streamlinerAll("202503")
