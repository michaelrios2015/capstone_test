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


def sixthAll(date, fed_date):

    db_date = date_c.date_conv(date)
    # so on the 6th business day

    # # we calculate FHAVA
    fhava.fhavaAll(date)

    # print("calculated FHAVA")

    # probably a better way to do it but here we are ereasing the intial pools so
    # they can be replaced by the offical ones
    if os.path.exists("biz_day/data/input/monthlySFPS_" + date + ".txt"):
        os.remove("biz_day/data/input/monthlySFPS_" + date + ".txt")

    # # Download pool date, pasre it add it to the database
    getFiles.download_parse_db("monthlySFPS_" + date)

    # # caluclate 6th day cprs
    cpr6th.cprs6thAll(date)

    ##############################################

    # load predicated CPRS
    predCPRS.pred_cprs(date)

    ###########################################

    # Run both new FHAVA stuff
    prepay.prepayAll(date)

    streamline.streamlinerAll(date)

    ###################################################

    # make fake platimuns

    procEarlyPlats.proc_early_plats(db_date)

    ###################################################

    # get fed data... I have nothing for this

    fedAll.fed_all(fed_date)

    # #################################################

    # recalulate fed data.... Seems to work

    feds_db.proc_feds(db_date, fed_date, True)

    ###############################################

    # process CMOS hard to test here

    procCmos.proc_cmos(db_date)

    ##############################################

    # process data for the web

    procGinnies.proc_ginnies(db_date, fed_date)

    ##############################################
    # start loading data

    # TRUNCATE ginnies;

    truncate.deleteGinnies()

    # ##########################################################################################

    ginnies.addGinnies()

    # ######################################################

    # Calculate float

    floatSum.float_sum(db_date)

    ###################################################

    # erease and reload cmos

    addCMO.add_cmos()


# the past month
date = "202507"

# the closests fed date
# YYYY-MM-DD
fed_date = "2025-08-06"

sixthAll(date, fed_date)

# then run the after 6th day
