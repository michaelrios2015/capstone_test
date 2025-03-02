import sys
import os


# so I need to tell it to work... so I have a subfolder
sys.path.append(os.path.join(os.path.dirname(__file__), "ginnie_extract"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader"))

# print(sys.path)

from ginnie_extract import *
from local_parser import *
from db_loader import *

# import ginnie_extract

imported_modules = sys.modules.keys()
# print(imported_modules)


# print(sys.path)


# gm_extractor.download_unzip_gm("platcoll_202501")
# platcolls.parser_platcolls("202501")
# db_platcolls.add_platcoll("2025-01")

# gm_extractor.download_unzip_gm("monthlySFPS_202501")
# pools.parse_pools("202501")
# db_pools.add_pools("2025-01")

# gm_extractor.download_unzip_gm("platmonPPS_202501")
# platinums.parse_plats("202501")
# db_plats.add_plats("2025-01")


# so I will supply a file and then the program should do the rest...abs

file = "monthlySFPS_202501"
