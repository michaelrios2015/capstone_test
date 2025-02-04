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

print("---------")
print(sys.path[0])


sys.path.append("C:/Users/micha/capstoneTest/classwork")

print("---------")

import congestion

print(sys.path)


ddd
# sys.path.insert(1, "capstoneTest")


# import capstoneTest.password.passwords.email

import passwords as p


####################################################################################################
####################################################################################################


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
    get_file_gm(url_head)

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
# url_head = "platmonPPS_202412.zip"

for url in url_heads:
    # print(url)
    download_unzip_gm(url)


# seems to work fine
