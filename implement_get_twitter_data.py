import pickle
from pathlib import Path
from datetime import datetime
import gc
import time
import traceback
import json
import brotli
from seleniumwire.webdriver import Chrome
from seleniumwire.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import numpy as np
import zstandard as zstd
import pandas as pd
import requests
from seleniumwire import webdriver
import gzip
import random

main_path = 'path_to_handles_we_care_about.csv'
output_path = 'path_to_handles_we_already_scraped.csv'

driver= webdriver.Chrome()
driver.get("https://twitter.com")

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
    
driver.refresh()

gh = grab_links_df(main_path, output_path)

user_data = []
for i in range(0, len(gh)):
    t = random.randint(1,3)
    time.sleep(t)
    print(i)
    h = gh[i]
    try:
        pl = navigate_to_page_get_payload(d = driver, target_url=h)
        atts = grab_user_attributes(pl)
        user_data.append(atts)
        if i % 10 == 0:
            dataframe = pd.DataFrame(user_data)
            dataframe.to_csv("output_path.csv", mode = "w")
    except:
        time.sleep(t)
        driver.refresh()
        print(h)
        #payloads.append(h)
        if i % 10 == 0:
            dataframe = pd.DataFrame(user_data)
            dataframe.to_csv("output_path.csv", mode = "w")
