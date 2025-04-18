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

# so on the 4th business day

# we calcalulate the intial CPRS and add them to the database

mortage.cprs4thAll("202503")

# Then process our data for the sebsite
procGinnies.proc_ginnies("2025-03-01", "2025-04-02")


# Erase the ginnes
truncate.deleteGinnies()

# ##########################################################################################
# ADD THE ginnies back

ginnies.addGinnies()

dailys.addDailies()

firstDay.addFirstDay()
