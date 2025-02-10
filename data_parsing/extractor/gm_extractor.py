# we have automated teh downloading of the ginnie mae files
# most were straight forward but the dailySPFS required a bit of work

# importing webdriver from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


# all the other libraries
import os
import sys

# get the file above so I can search thropugh parent directory
# not sure if I am still using this need to test
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

print(sys.path)


# so now my helper functions are all in a seperate folder
# from secret import passwords
from helpers import *


# So my one main function.. should it be called main I am not entirely sure
def download_unzip_gm(url_head):
    # so this downloads the file to C:/Users/micha/Downloads/
    get_file.get_file_gm(url_head)

    # here we look at the file we want
    src = "C:/Users/micha/Downloads/" + url_head

    # check to see if it the dailySFPS
    if url_head == "dailySFPS.zip":
        # if so need to call it's own special function
        daily.dailys()
    # if not we can just unzip and
    else:
        # then just unzipfile and place it where we want
        daily.extract_file(src)


url_heads = [
    "dailySFPS.zip",
    "platmonPPS_202412.zip",
    "monthlySFPS_202412.zip",
    "platcoll_202412.zip",
]

url = "dailySFPS.zip"
download_unzip_gm(url)

# for url in url_heads:
#     # print(url)
#     download_unzip_gm(url)


# seems to work fine
