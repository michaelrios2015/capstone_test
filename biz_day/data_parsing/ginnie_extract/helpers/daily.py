import os
import glob
import datetime
import zipfile
import sys


# just a small helper function to extract data from downloads and put in in my data file
def extract_file(src):
    with zipfile.ZipFile(src, "r") as zip_ref:
        # hardcoding in destintation as it is only used in this program
        dest = "C:/Users/micha/capstoneTest/biz_day/data/input"
        zip_ref.extractall(dest)


######################################################################################################################################
######################################################################################################################################


# so here we are dealing with the dailySFPS or dailyllmni
# both of whihc do not come with dates
def dailys(file):
    # this first part is the same
    directory = "C:/Users/micha/Downloads/"

    # make the path to file of all dailySPFS or dailyllmni zip files
    path = directory + file + "*" + ".zip"

    # put them in an array or list I guess
    files = glob.glob(path)
    # print(files)

    # get the most recemt one
    most_recent_file = max(files, key=os.path.getmtime)
    # print(most_recent_file)

    # then just unzipfile and place it where we want
    extract_file(most_recent_file)

    # get todays date and time
    now = datetime.datetime.now()

    # get YYYYMM
    formatted_datetime = now.strftime("%Y%m")

    # so if it is dailySFPS we need to do a bunch of stuff to rename it
    if file == "dailySFPS":

        # make entire title
        new_title = "biz_day/data/input/monthlySFPS_" + formatted_datetime + ".txt"

        # check to see if the file already exists
        if os.path.exists(new_title):
            # if so it should be an oldre version remove it
            os.remove(new_title)
        # then we just need to be able to rename it correctly
        os.rename("biz_day/data/input/dailySFPS.txt", new_title)

    return formatted_datetime


###########################################################################################
###########################################################################################
# TEST

# dailys("dailyllmni")
