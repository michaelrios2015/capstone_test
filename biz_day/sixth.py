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

date = "202503"

fed_date = "2025-04-02"

# db_date = date_c.date_conv(date)
# so on the 6th business day

# # we calculate FHAVA
# fhava.fhavaAll(date)

# print("calculated FHAVA")

# # Download pool date, pasre it add it to the database
# getFiles.download_parse_db("monthlySFPS_" + date)

# # caluclate 6th day cprs
# cpr6th.cprs6thAll(date)

##############################################


# load predicated CPRS
# predCPRS.pred_cprs(date)

###########################################

# Run both new FHAVA stuff
# prepay.prepayAll(date)

# streamline.streamlinerAll(date)

###################################################

# make fake platimuns

# procEarlyPlats.proc_early_plats(db_date)

###################################################

# get fed data... I have nothing for this

#   fedAll.fed_all(fed_date)

# #################################################

# recalulate fed data.... I need to write this

###############################################

# CMOS

# allcmostoredprocedure( currentmonth DATE )

# Call allcmostoredprocedure( '2025-03-01' );

##############################################

# process data for the web

# Call processdataforweb(currentmonth DATE, feddate DATE)

##############################################
# start loading data

# TRUNCATE ginnies;

# truncate.deleteGinnies()

# ##########################################################################################

# ginnies.addGinnies()

# ######################################################

# Calculate float

# Call get_float_sum(date DATE)

# call get_float_sum('2025-03-01');

###################################################

# erease and reload cmos

# TRUNCATE cmos;


# \COPY cmos FROM 'C:\Users\Public\cmodataforweb' DELIMITER ',' CSV HEADER;


###############################################

# ideally call an unwritten function that gets new pools
# and adds them
