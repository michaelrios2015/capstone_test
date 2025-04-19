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

date = "202503"

fed_date = "2025-04-02"

# getFiles.download_parse_db("platmonPPS_" + date)

# download platcolls

# getFiles.download_parse_db("platcoll_" + date)

db_date = date_c.date_conv("202503")

# print(db_date)


###########################################################

# process platinums, it's frustrating not seeing what is happening but it seems to work

# procPlats.proc_plats(db_date)

##############################################################

# platfhavas

# procPlatFhas.proc_plat_fhas(db_date)

# ##################################################

# pocess data for the web

# procGinnies.proc_ginnies(db_date, fed_date)


##################################################

# CMOS

# procCmos.proc_cmos(db_date)

# ##############################################
# # start loading data

# TRUNCATE ginnies;

truncate.deleteGinnies()

# ##########################################################################################

ginnies.addGinnies()

# ######################################################

# # Calculate float
# DELETE FROM sumoffloats where date = '2025-03-01';

# # Call get_float_sum(date DATE)

# # call get_float_sum('2025-03-01');

# ###################################################

# # erease and reload cmos

# # TRUNCATE cmos;


# # \COPY cmos FROM 'C:\Users\Public\cmodataforweb' DELIMITER ',' CSV HEADER;


# ###############################################

# # ech of these can be a function seems a little like overkill but do mix and match them a bit
# # TRUNCATE ginnies;

# truncate.deleteGinnies()

# ##########################################################################################

# ginnies.addGinnies()

# dailys.addDailies()
