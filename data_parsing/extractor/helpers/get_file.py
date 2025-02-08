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


###########################################################################################
###########################################################################################
# function ended just some test stuff

# # url_base = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/"
# url_head = "monthlySFPS_202412.zip"

# # seemes to work fine
# get_file_gm(url_head)
