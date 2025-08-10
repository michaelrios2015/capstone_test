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
def fhava4thAll(date):
    # get data

    # so it was august will probably give it july...

    prev_month = month.prev_month(date)

    # the two older files, should have them
    if not (
        os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + prev_month + "_001.txt")
    ):
        gm_extractor.download_unzip_gm("/llmon1_" + prev_month)

    if not (
        os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + prev_month + "_002.txt")
    ):
        gm_extractor.download_unzip_gm("/llmon2_" + prev_month)

    # this can only be the newest one...
    gm_extractor.download_unzip_gm("dailyllmni")

    # our one current file
    if not (os.path.exists("biz_day/data/input/llmonliq_" + date + ".txt")):
        gm_extractor.download_unzip_gm("llmonliq_" + date)

    # here we process the data
    fhavaInitial.fhava_4th(date)

    # date for the database
    date_db = date_c.date_conv(date)

    # add to database
    db_prepay.add_prepay(date_db)


###########################################

# TEST
# fhava4thAll("202507")
