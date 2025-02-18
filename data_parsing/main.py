import sys
import os

# from local_parser import *

# import parser

# is there a better way to do this...

# daily.dailys()

# so I need to tell it to work... so I have a subfolder
sys.path.append(os.path.join(os.path.dirname(__file__), "ginnie_extract"))
print(sys.path)

from ginnie_extract import *

# import ginnie_extract

imported_modules = sys.modules.keys()
print(imported_modules)


# print(sys.path)

# platcolls.parser_platcolls("202412")

# gm_extractor.download_unzip_gm("platcoll_202412")
# extract.gm_extractor.download_unzip_gm("platcoll_202412")
# pools.parse_pools("202412")
