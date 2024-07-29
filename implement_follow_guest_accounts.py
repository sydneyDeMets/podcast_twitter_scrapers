import pickle
from pathlib import Path
from datetime import datetime
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy as np
import json
import pandas as pd
import random

path1 =  'file_path_to_complete_list_of_guest_accounts'
path2 =  'path_to_those_already_followed'
links = grab_links_df(path1, path2)

driver= webdriver.Chrome()
driver.get("https://twitter.com")

#if you need to save cookies
#pickle.dump( driver.get_cookies() , open("cookies.pkl","wb")) # saving cookies
#driver.close()

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
    
driver.refresh()

already_followed = make_followed_list_original(path2)

for index, link in enumerate(links):
    try:
        follow_user(link, driver=driver)
        already_followed.append(link)
        counter = 0
        print(index)
        if index % 20 == 0:
            df = pd.DataFrame(already_followed, columns=["twitter_link"])
            df.to_csv('/Users/sydneydemets/Desktop/twitter_HOST_data 2/already_followed.csv', index=False, mode='w')
    except:
        print(index)
        error = "error"
        already_followed.append(error)
        counter +=1
        if index % 20 == 0:
            df = pd.DataFrame(already_followed, columns=["twitter_link"])
            df.to_csv('/Users/sydneydemets/Desktop/twitter_HOST_data 2/already_followed.csv', index=False, mode='w')
        print(counter)
        if index % 121 == 0:
            df = pd.DataFrame(already_followed, columns=["twitter_link"])
            df.to_csv('/Users/sydneydemets/Desktop/twitter_HOST_data 2/already_followed.csv', index=False, mode='w')
            driver.quit()
            driver= webdriver.Chrome()
            driver.get("https://twitter.com")
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh(

