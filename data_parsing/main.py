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
file = "dailySFPS"
file = "platmonPPS_202501"

# "dailySFPS",
# "platmonPPS_202412",
# "monthlySFPS_202412",
# "platcoll_202412",

# so no matter which file we have it need to be extracted and the extractor
# just needs the file name

# gm_extractor.download_unzip_gm(file)

# step two, check which file we have, so

parts = file.split("_")
print(parts)
# so we just check the first part
if parts[0] == "platmonPPS":
    # then i need to send the date
    # platinums.parse_plats(parts[1])
    # then we need to reformat date
    date = parts[1][:4] + "-" + parts[1][4:]
    print(date)
    # db_plats.add_plats(date)
