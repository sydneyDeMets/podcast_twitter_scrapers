from names_to_twitter_handles.py import *

conn = get_connection(refresh=True)
api_key = 'xxxxxx'

names = grab_names(conn) #grabbing unsearched names
for name in names:
    init_result = search_name(name, conn) #use SerpAPI to look up first name last name twitter account
    full_handles = extract_handles(init_result) #Identifying any Twitter handles in the returned results
    top_handle = grab_top_handle(full_handles) #grabbing the first handle to appear in google search results
    ch = clean_handle(top_handle) #cleaning the string
    add_handle(conn, name, ch) #pushing the handle to db
    link = make_x_link(ch) #making a link to X
    add_link(conn, name, link) #pushing the link to db
