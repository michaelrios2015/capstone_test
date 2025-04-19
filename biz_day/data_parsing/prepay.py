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


def prepayAll(date):

    # step one get files

    # we need previous month

    prev_month = month.prev_month(date)

    # print(prev_month)
    # get files
    if not (
        os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + prev_month + "_001.txt")
    ):
        gm_extractor.download_unzip_gm("llmon1_" + prev_month)

    if not (
        os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + prev_month + "_002.txt")
    ):
        gm_extractor.download_unzip_gm("llmon2_" + prev_month)

    # so unless I want to start dating this file I cannot be sure it is up to date and should just
    # download it again
    gm_extractor.download_unzip_gm("dailyllmni")

    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_001.txt")):
        gm_extractor.download_unzip_gm("llmon1_" + date)

    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_002.txt")):
        gm_extractor.download_unzip_gm("llmon2_" + date)

    # process the files and fet date for database
    next_month = prepay_file.prepay(date)

    # print(next_month)

    # add to database
    db_prepay.add_prepay(next_month)


# test

# date = "202503"
# prepayAll(date)
