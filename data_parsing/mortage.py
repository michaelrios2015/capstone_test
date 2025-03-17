import sys
import os
import datetime

# so I need to tell it to work... so I have a subfolder
sys.path.append(os.path.join(os.path.dirname(__file__), "ginnie_extract"))
sys.path.append(os.path.join(os.path.dirname(__file__), "db_loader"))
sys.path.append(os.path.join(os.path.dirname(__file__), "local_parser"))

# print(sys.path)
# we import everything from the subfolders
from ginnie_extract import *
from local_parser import *
from db_loader import *

# so these are working fine
# gm_extractor.download_unzip_gm("llmonliq_202502")
# gm_extractor.download_unzip_gm("nimonSFPS_202502")
