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

# so on the 8th business day

# we download the new platinums


def eigthAll(date, fed_date):

    # download platinums

    getFiles.download_parse_db("platmonPPS_" + date)

    # download platcolls

    getFiles.download_parse_db("platcoll_" + date)

    db_date = date_c.date_conv(date)

    # print(db_date)

    ###########################################################

    # process platinums, it's frustrating not seeing what is happening but it seems to work

    procPlats.proc_plats(db_date)

    ##############################################################

    # process platfhavas

    procPlatFhas.proc_plat_fhas(db_date)

    # ##################################################

    # pocess data for the web

    procGinnies.proc_ginnies(db_date, fed_date)

    ##################################################

    # CMOS

    procCmos.proc_cmos(db_date)

    # ##############################################
    # # start loading data

    # TRUNCATE ginnies;

    truncate.deleteGinnies()

    # ##########################################################################################
    # add back ginnies for float

    ginnies.addGinnies()

    # ######################################################

    # # Calculate float

    floatSum.float_sum(db_date)

    # ###################################################

    # # erease and reload cmos

    addCMO.add_cmos()

    # ###############################################

    # add back dailies

    dailys.addDailies()


date = "202503"

fed_date = "2025-04-02"

eigthAll(date, fed_date)
