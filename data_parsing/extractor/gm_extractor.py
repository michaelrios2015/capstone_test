# so I want to automate the downloading of the ginnie mae files
# for the code I wrote I use pools, platinums, platcols...these are all super simple since they are simnply
# download then moved from the download file to the file i need them in I mean technically they could stay in the download folder
# dailySPFS are the only hard one, I will usually have a bunch of tehse saved, so I need to find the newest on, unzip that
# then rename to the correct date


# importing webdriver from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


# all the other libraries
import os
import glob
import time
import datetime
import zipfile

import sys

# get the file above so I can search thropugh parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from helpers import get_file

# from helpers import passwords

print(sys.path)

####################################################################################################
####################################################################################################


####################################################################################


# just a small helper function to extract data from downloads and put in in my data file
def extract_file(src):
    with zipfile.ZipFile(src, "r") as zip_ref:
        # hardcoding in destintation as it is only used in this program
        dest = "C:/Users/micha/capstoneTest/data"
        zip_ref.extractall(dest)


######################################################################################
######################################################################################

# so this is alll designed to deal with the dailySFPS which is a bit annoying as all the other downloads are pretty freaking simple
# just download the file, and move it from downloads to the folder i want, daily i need to download it, then find the most recent one
# then move that to the folder i want then rename that based on what month it is


# so here we are dealing with the dailySFPS
def dailys():
    directory = "C:/Users/micha/Downloads/"
    partial_name = "dailySFPS"

    # make the path to file of all dailySPFS zip files
    path = directory + partial_name + "*" + ".zip"

    # put them in an array or list I guess
    files = glob.glob(path)

    # get the most recemt one
    most_recent_file = max(files, key=os.path.getmtime)

    # then just unzipfile and place it where we want
    extract_file(most_recent_file)

    # get todays date and time
    now = datetime.datetime.now()

    # get YYYYMM
    formatted_datetime = now.strftime("%Y%m")

    # make entire title
    new_title = "data\monthlySFPS_" + formatted_datetime + ".txt"

    # check to see if the file already exists
    if os.path.exists(new_title):
        # if so it should be an oldre version remove it
        os.remove(new_title)
    # then we just need to be able to rename it correctly
    os.rename("data\dailySFPS.txt", new_title)


##################################################################################################################
##################################################################################################################

# putting it all together this is the only file that other programs will use


def download_unzip_gm(url_head):
    # so this downloads the file to C:/Users/micha/Downloads/
    get_file.get_file_gm(url_head)
    # h.get_file.get_file_gm(url_head)

    # here we look at the file we want
    src = "C:/Users/micha/Downloads/" + url_head

    # check to see if it the dailySFPS
    if url_head == "dailySFPS.zip":
        # if so need to call it's own special function
        dailys()
    # if not we can just unzip and
    else:
        # then just unzipfile and place it where we want
        extract_file(src)


url_heads = [
    "dailySFPS.zip",
    "platmonPPS_202412.zip",
    "monthlySFPS_202412.zip",
    "platcoll_202412.zip",
]

url = "platmonPPS_202412.zip"
download_unzip_gm(url)

# for url in url_heads:
#     # print(url)
#     download_unzip_gm(url)


# seems to work fine
