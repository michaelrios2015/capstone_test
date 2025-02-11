import sys

from local_parser import *

# import parser

# is there a better way to do this... 
from extractor.helpers import *

from extractor import *

imported_modules = sys.modules.keys()
print(imported_modules)

print(sys.path)

# platcolls.parser_platcolls("202412")
gm_extractor.download_unzip_gm("platcoll_202412")
pools.parse_pools("202412")
