# this opens and downloads the desired ginnie mae file for me

# importing webdriver from selenium
from selenium import webdriver
from selenium.webdriver.common.by import By


# all the other libraries
import os
import sys

# This is so it can find secrets
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
from secret import passwords

####################################################################################################
####################################################################################################


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
    email_input.send_keys(passwords.email)

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
    answer.send_keys(passwords.answer)

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
# # function ended just some test stuff

# # # url_base = "https://bulk.ginniemae.gov/protectedfiledownload.aspx?dlfile=data_bulk/"
# url_head = "monthlySFPS_202412.zip"

# # seemes to work fine
# get_file_gm(url_head)
