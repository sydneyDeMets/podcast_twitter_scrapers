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

def grab_links_df(path1, path2):
    #returns a unique list of twitter accounts whose data has not been scraped
    #path =  '/Users/sydneydemets/Desktop/twitter_handles_guests.csv'
    data_original = pd.read_csv(path1)
    data_followed = pd.read_csv(path2)
    df1 = data_original[(data_original['was_searched']==True) & (data_original['twitter_link']!= 'https://x.com/') & (data_original['twitter_link'].str.contains(' ') == False)]
    df2 = df1[~df1.twitter_link.isin(data_followed.twitter_link)].drop_duplicates()
    return df2['twitter_link'].tolist()

def navigate_to_page_get_payload(d, target_url):
    d.get(target_url)
    d.refresh()
    reqs = d.requests
    route_name = "UserByScreenName"
    notes_reqs = [req for req in reqs if route_name in req.url]
    req = notes_reqs[-1]
    payload = json.loads(gzip.decompress(req.response._body))
    return(payload)

def grab_user_attributes(payload):
    d = {}  
    core_object = payload['data']['user']['result']
    d['screen_name'] = core_object['legacy']['screen_name']
    d['name'] = core_object['legacy']['name']
    d['rest_id'] = core_object['rest_id']
    d['favourites'] = core_object['legacy']['favourites_count']
    d['followers'] = core_object['legacy']['followers_count']
    d['description'] = core_object['legacy']['description']
    return(d)
