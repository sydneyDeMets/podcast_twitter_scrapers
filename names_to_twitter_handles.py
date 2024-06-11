import pandas as pd
import datapy
import wget
import requests
import os
import time
import datapy
import serpapi
from serpapi import GoogleSearch
from datapy.dbconn import get_connection, run_sql_fetch_one, run_sql_fetch_all, read_table_by_pandas

def grab_names(conn):
    #returns names that have NOT been searched
    q = "select final_name from {table} where was_searched is False"
    df = read_table_by_pandas(conn, q)
    return df['final_name'].tolist()

def update_was_searched(conn, name):
    #indicates that this name was run through the SerpAPI after it has been searched
    cursor = conn.cursor()
    cursor.execute("UPDATE {table} SET was_searched = True WHERE final_name = %s", (name,))
    conn.commit()
    
def add_handle(conn, name, twitter_handle):
    #adding the twitter handle to the db
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table} SET twitter_handle = %s WHERE final_name = %s", (twitter_handle, name))
    conn.commit()
    
def add_link(conn, name, twitter_link):
    #adding the twitter link to the db
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table} SET twitter_link = %s WHERE final_name = %s", (twitter_link, name))
    conn.commit()

#use the google search from SerpAPI
def search_name(name, conn):
    search_term = name + " twitter account"
    print(search_term)
    params = {
        "api_key": api_key,
        "engine": "google",
        "q": search_term,
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en"}
    search = GoogleSearch(params)
    update_was_searched(conn, name)
    result = search.get_dict()
    return(result)

#extract the handles from the API results dict
def extract_handles(d):
    try:
        r1=d['twitter_results']['title']
    except KeyError:
        r1= d['organic_results']
    return(r1)

#getting the handle with the most follows, which is returned first
def grab_top_handle(dt):
    if type(dt)==list:
        r = len(dt)
        iz = []
        lz = []
        for i in range(0,r):
            if dt[i]['title'].endswith("X"):
                iz.append(dt[i]['title'])
                #print(dt[i]['title'])
                ix = iz[0]
                #print(ix)
                lz.append(ix)
            else: 
                if dt[i]['source'].startswith("X"):
                    iz.append(dt[i]['source'])
                    ix = iz[0]
                    lz.append(ix)#do nothing
                else:
                    lz.append("na")
        top_handle = lz[0]
    else:
        top_handle = dt
    return(top_handle)

#cleaning up the string
def clean_handle(handle):
    if handle.startswith("X"):
        h = handle[handle.find("X")+4:len(handle)]
    else:
        h = handle[handle.find("(")+2:handle.find(")")]
    return(h)

#function to make the link so Lia doesn't kill me if I try to do this using SQL
def make_x_link(h):
    link = "https://x.com/" + h
    return(link)
