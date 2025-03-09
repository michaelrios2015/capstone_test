from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# from get_file import get_file_gm
# from daily import dailys, extract_file

from helpers import *


# So this will download my ginnie mae fill and put it in the right folder
def download_unzip_gm(url_head):
    # so this downloads the file to C:/Users/micha/Downloads/
    url_head += ".zip"
    get_file.get_file_gm(url_head)

    # here we look at the file we want
    src = "C:/Users/micha/Downloads/" + url_head

    # check to see if it the dailySFPS
    if url_head == "dailySFPS.zip":
        # if so need to call it's own special function
        date = daily.dailys()
        return date
    # if not we can just unzip and
    else:
        # then just unzipfile and place it where we want
        daily.extract_file(src)


################################################################################################
################################################################################################

# just some tests

url_heads = [
    "dailySFPS",
    "platmonPPS_202501",
    "monthlySFPS_202501",
    "platcoll_202501",
]

# url = "dailySFPS"
# download_unzip_gm(url)

# for url in url_heads:
#     # print(url)
#     download_unzip_gm(url)


# seems to work fine
