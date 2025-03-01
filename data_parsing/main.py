import sys
import os


# so I need to tell it to work... so I have a subfolder
sys.path.append(os.path.join(os.path.dirname(__file__), "ginnie_extract"))
# print(sys.path)

from ginnie_extract import *
from local_parser import *


# import ginnie_extract

imported_modules = sys.modules.keys()
# print(imported_modules)


# print(sys.path)

# platcolls.parser_platcolls("202412")

# gm_extractor.download_unzip_gm("platcoll_202501")
# platcolls.parser_platcolls("202501")

# gm_extractor.download_unzip_gm("monthlySFPS_202501")
pools.parse_pools("202501")
