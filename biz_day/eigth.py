import sys
import os
import time


# oh so you always need to include the below folder
sys.path.append(os.path.join(os.path.dirname(__file__), "data_parsing"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader", "days_db"))


print(sys.path)

from data_parsing import *
from days_db import *
from db_loader import *

# so on the first business day

# we download the brand new pools

# which would be the dailySFSPS files


file = "dailySFPS"
# download the new dailys
getFiles.download_parse_db(file)

print("downloaded new data")

# process the new dailies
procDaily.proc_daily("2025-03-01", "true")


# Then add this to rge other database

# ech of these can be a function seems a little like overkill but do mix and match them a bit
# TRUNCATE ginnies;

truncate.deleteGinnies()

##########################################################################################

ginnies.addGinnies()

dailys.addDailies()

firstDay.addFirstDay()
