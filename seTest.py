# importing webdriver from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# import passwords
import passwords as p


# this will open the ginnie mae urls and which causes them to be downloaded to my downloads
# this only ginnie mae files
def get_file_gm(url_head):

    # this is how all ginne mae files begin
    url_base = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/"
    # this will be our acyual url
    url = url_base + url_head
    # selecting Firefox as the browser
    # for reasons unknow to me Chrome did not work, seemed to work but download failed
    driver = webdriver.Firefox()

    # opening link in the browser
    driver.get(url)

    # find the email input field
    email_input = driver.find_element(
        By.NAME,
        "ctl00$ctl45$g_174dfd7c_a193_4313_a2ed_0005c00273fc$ctl00$tbEmailAddress",
    )

    # enter in email
    email_input.send_keys(p.email)

    # find the submit button
    submit = driver.find_element(
        By.NAME,
        "ctl00$ctl45$g_174dfd7c_a193_4313_a2ed_0005c00273fc$ctl00$btnQueryEmail",
    )

    # click the submit button
    submit.click()

    # we go to the next page
    # find answer field
    answer = driver.find_element(
        By.NAME, "ctl00$ctl45$g_174dfd7c_a193_4313_a2ed_0005c00273fc$ctl00$tbAnswer"
    )

    # enter answer
    answer.send_keys(p.answer)

    # find verify button
    verify = driver.find_element(
        By.NAME,
        "ctl00$ctl45$g_174dfd7c_a193_4313_a2ed_0005c00273fc$ctl00$btnAnswerSecret",
    )

    # click verify button
    verify.click()

    # quit
    driver.quit()


# url_base = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/"
# url_head = "monthlySFPS_202412.zip"

# seemes to work fine
# get_file_gm(url_head)


######################################################################################
######################################################################################

# function 2 so

import zipfile
import os

# it's a simple function not sure if it is really neccessary
# def unzip(src, dest):
#     # # this unzips them and places them in my cvspyreaders
#     with zipfile.ZipFile(src, "r") as zip_ref:
#         zip_ref.extractall(dest)


# # this will work for everything except the dailyspfs
# src = "C:/Users/micha/Downloads/monthlySFPS_202412.zip"
# dest = "C:/Users/micha/capstoneTest/"

# unzip(src, dest)

# so we want to download and unzip the files


def download_unzip_gm(url_head):
    # so this downloads the file to C:/Users/micha/Downloads/
    get_file_gm(url_head)

    # so the source and destionation should never change, well the source changes a bit
    # but we are given the change
    src = "C:/Users/micha/Downloads/" + url_head
    dest = "C:/Users/micha/capstoneTest/"

    # then just unzipfile and place it where we want
    with zipfile.ZipFile(src, "r") as zip_ref:
        zip_ref.extractall(dest)

    # the above works for all the files but if we have dailysfps we need to rename it
    if url_head == "dailySFPS.zip":
        # so this is actually a pain becuase we may have multiople dailysfps in the downloads
        os.rename("dailySFPS.txt", "test.txt")


# url_head = "dailySFPS.zip"
# download_unzip_gm(url_head)


# seems to work fine
##############################################################################
##############################################################################

# so lets see we have a couple of options here so for all but the daily files
# all I need to do is run get file, i give it the url, which give me the name of the file
# it will always go to downloads, and then it always gets put in the same place so tercnically
# I can just hard coe those in, though if it were on a server maybe not....abs

# but on this computer I can do a couple of things.... I can just check to see if it ends with daily whatever and if it does
# i believe I can just check the date and renaem it after whatever month I am on... that should work... I can also pass in a field
# but I think checking on it's own is better..


# so apperently the renaming is super simple wont give me two files, so probably combine this with the extract function

# os.rename("new.txt", "monthlySFPS_202412.txt")

# DIR_PATH = "C:/Users/micha/Downloads/"
# BASENAME = "dailySFPS.txt"

# # def newest(DIR_PATH):
# files = os.listdir(DIR_PATH)
# # print(files)
# FILE_LIST = [
#     os.path.join(DIR_PATH, BASENAME)
#     for BASENAME in files
#     if not BASENAME.endswith("trimmed.json")
# ]
# print(FILE_LIST)
# # return max(FILE_LIST, key=os.path.getctime)


import os
import glob
import time


def find_most_recent_file(directory, partial_name):
    """Finds the most recent file in a directory with a partial name match."""

    print(os.path.join(directory, f"{partial_name}*"))

    path = directory + partial_name + "*"
    print("------")

    files = glob.glob(path)

    print(files)

    print("------")
    if not files:
        return None

    most_recent_file = max(files, key=os.path.getmtime)
    return most_recent_file


# Example usage
directory_path = "C:/Users/micha/Downloads/"
partial_file_name = "dailySFPS"

most_recent = find_most_recent_file(directory_path, partial_file_name)

if most_recent:
    print("Most recent file:", most_recent)
else:
    print("No matching files found.")
