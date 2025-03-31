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


# cprs4thAll("202502")


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


# cprs6thAll("202502")


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


# fhavaAll("202502")
