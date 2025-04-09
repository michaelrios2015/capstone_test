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
    gm_extractor.download_unzip_gm("llmonliq_" + date)
    gm_extractor.download_unzip_gm("nimonSFPS_" + date)

    # we should already have this but including it just in case
    prev_month = month.prev_month(date)
    gm_extractor.download_unzip_gm("monthlySFPS_" + prev_month)

    # here we process the data
    cprsIntial.cprs4th(date)

    # date for the database
    date_db = date_c.date_conv(date)

    # the database part will only run once
    db_cpr4th.add_cprs4th(date_db)


# cprs4thAll("202503")


# all the 6th day stuff
def cprs6thAll(date):

    # download the files, we should already have some but does not seem to hurt to download them again
    # I guess ideally you would check first... may add that later
    gm_extractor.download_unzip_gm("nimonSFPS_" + date)
    gm_extractor.download_unzip_gm("monthlySFPS_" + date)

    prev_month = month.prev_month(date)
    gm_extractor.download_unzip_gm("monthlySFPS_" + prev_month)

    # process the data
    cprsFinal.cprs6th(date)

    # add to database
    date_db = date_c.date_conv(date)
    db_cpr6th.add_cprs6th(date_db)


# cprs6thAll("202503")


def fhavaAll(date):

    gm_extractor.download_unzip_gm("dailyllmni")
    # ideally I would tell these last two to wait
    gm_extractor.download_unzip_gm("llmon1_" + date)
    gm_extractor.download_unzip_gm("llmon2_" + date)

    # process data
    fhava_file.fhava(date)

    # add to database
    date_db = date_c.date_conv(date)
    db_fhava.add_fhava(date_db)


# fhavaAll("202503")


############################################

# streamline


def streamlinerAll(date):

    # see if we have files, if not get them
    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_001.txt")):
        gm_extractor.download_unzip_gm("llmon1_" + date)

    if not (os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + date + "_002.txt")):
        gm_extractor.download_unzip_gm("llmon2_" + date)

    # this can only be the newest one...
    if not (os.path.exists("biz_day/data/input/dailyllmni.txt")):
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


# streamlinerAll("202502")


############################################

# prepay

date = "202502"

# step one get files

# we need previous month

prev_month = month.prev_month(date)

print(prev_month)

if not (
    os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + prev_month + "_001.txt")
):
    gm_extractor.download_unzip_gm("llmon1_" + prev_month)


if not (
    os.path.exists("biz_day/data/input/GNMA_MBS_LL_MON_" + prev_month + "_002.txt")
):
    gm_extractor.download_unzip_gm("llmon2_" + prev_month)


# data_url_2 = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/llmon1_202502.zip"


# data_url_3 = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/llmon2_202502.zip"

# mLoanFileOld = {
#     # two from the past month
#     "GNMA_MBS_LL_MON_202501_001.txt",
#     "GNMA_MBS_LL_MON_202501_002.txt",
#     # this is the current month
#     "dailyllmni.txt",
# }

# # Files published 6th business day of month n+1
# # current month
# mLoanFile = {"GNMA_MBS_LL_MON_202502_001.txt", "GNMA_MBS_LL_MON_202502_002.txt"}
