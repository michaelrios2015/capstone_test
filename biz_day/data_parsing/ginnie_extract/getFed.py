import requests


# change this weekly


def get_fed(date):

    data_url = (
        "https://markets.newyorkfed.org/api/soma/agency/get/mbs/asof/" + date + ".csv"
    )

    data_path = "biz_day/data/input/fedHoldings" + date + ".csv"

    r = requests.get(data_url)  # create HTTP response object

    with open(data_path, "w") as f:
        f.write(r.text)


# ######### TESTING ##############

# date = "2025-04-02"
# get_fed(date)
