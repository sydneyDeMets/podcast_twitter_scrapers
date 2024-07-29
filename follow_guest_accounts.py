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

def grab_links(conn):
    #returns a unique list of twitter accounts that have NOT been followed
    q = "select twitter_link from {table} where followed is False"
    df = read_table_by_pandas(conn, q)
    return df['twitter_link'].tolist()

def grab_links_df(path1, path2):
    #returns a unique list of twitter accounts that have NOT been followed
    #path =  '/Users/sydneydemets/Desktop/twitter_handles_guests.csv'
    data_original = pd.read_csv(path1)
    data_followed = pd.read_csv(path2)
    df1 = data_original[(data_original['was_searched']==True) & (data_original['twitter_link']!= 'https://x.com/')]
    df2 = df1[~df1.twitter_link.isin(data_followed.twitter_link)].drop_duplicates()
    return df2['twitter_link'].tolist()

def update_was_followed(conn, twitter_link):
    #indicates that this name was run through the SerpAPI after it has been searched
    cursor = conn.cursor()
    cursor.execute("UPDATE {table} SET was_followed = True WHERE twitter_link = %s", (twitter_link,))
    conn.commit()

def start_driver(url:str):
    driver=webdriver.Chrome()
    driver.get(url)
    return(driver)

def load_cookies(path, driver):
    cookies_file = open(path, 'rb')
    cookies = pickle.load(cookies_file)
    return(driver, cookies)

def follow_user(target_url, driver):    
    driver.get(target_url)
    t = random.randint(1, 7)
    time.sleep(t)
    #wait = WebDriverWait(driver, t)
    #wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/button')))
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div/div[1]/button').click()
    time.sleep(t)
    return(True)

def make_followed_list_original(path):
    #path = '/Users/sydneydemets/Desktop/twitter_HOST_data 2/already_followed.csv'
    df = pd.read_csv(path)
    already_followed = df['twitter_link'].tolist()
    return(already_followed)
    
    
