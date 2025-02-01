# so I want to automate the downloading of the ginnie mae files
# for the code I wrote I use pools, platinums, platcols...these are all super simple since they are simnply
# download then moved from the download file to the file i need them in I mean technically they could stay in the download folder
# dailySPFS are the only hard one, I will usually have a bunch of tehse saved, so I need to find the newest on, unzip that
# then rename to the correct date


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

# so lets see we have a couple of options here so for all but the daily files
# all I need to do is run get file, i give it the url, which give me the name of the file
# it will always go to downloads, and then it always gets put in the same place so tercnically
# I can just hard coe those in, though if it were on a server maybe not....abs

# but on this computer I can do a couple of things.... I can just check to see if it ends with daily whatever and if it does
# i believe I can just check the date and renaem it after whatever month I am on... that should work... I can also pass in a field
# but I think checking on it's own is better..


# so apperently the renaming is super simple wont give me two files, so probably combine this with the extract function

# so this is alll designed to deal with the dailySFPS which is a bit annoying as all the other downloads are pretty freaking simple
# just download the file, and move it from downloads to the folder i want, daily i need to download it, then fine the most recent one
# then move that to the folder i want then rename that based on what month it is but if I can do that then this function can handle
# all the ginnie mae files, cmos are there own thing.... not a clue if that can be standardized would need to ask david, fed data works fine
# with the easier method, david still gives me some data but i can probably just get the code, oh wel this whole thing is just going to be a slow
# and how often do i need a try fail and is that the only thing i am supposed to use


import os
import glob
import time
import datetime


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

    # here we are getting ready to unzip
    dest = "C:/Users/micha/capstoneTest/"

    # then just unzipfile and place it where we want
    with zipfile.ZipFile(most_recent_file, "r") as zip_ref:
        # this file will still be called dailySFPS.txt
        zip_ref.extractall(dest)

    # get todays date and time
    now = datetime.datetime.now()

    # get YYYYMM
    formatted_datetime = now.strftime("%Y%m")

    # make entire title
    new_title = "monthlySFPS_" + formatted_datetime + ".txt"

    # check to see if the file already exists
    if os.path.exists(new_title):
        # if so it should be an oldre version remove it
        os.remove(new_title)
    # then we just need to be able to rename it correctly
    os.rename("dailySFPS.txt", new_title)


# function 2 so

import zipfile
import os

# putting it all together


def download_unzip_gm(url_head):
    # so this downloads the file to C:/Users/micha/Downloads/
    get_file_gm(url_head)

    # so the source and destionation should never change, well the source changes a bit
    # but we are given the change
    src = "C:/Users/micha/Downloads/" + url_head
    # NEED TO CHANGE THIS WHEN PUT BACK WITH REGULAR CODE
    dest = "C:/Users/micha/capstoneTest/"

    # check to see if it the dailySFPS
    if url_head == "dailySFPS.zip":
        # if so need to call it's own special function
        dailys()
    # if not we can just unzip and
    else:
        # then just unzipfile and place it where we want
        with zipfile.ZipFile(src, "r") as zip_ref:
            zip_ref.extractall(dest)


# url_head = "dailySFPS.zip"
url_head = "platmonPPS_202412.zip"

download_unzip_gm(url_head)


# seems to work fine
