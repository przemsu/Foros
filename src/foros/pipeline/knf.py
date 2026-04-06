import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

def knf_warning():
    # URL for scraping
    url = "https://www.knf.gov.pl/dla_konsumenta/ostrzezenia_publiczne"

    # Scraping data from knf warnings lists using pandas read_html
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")
    df_pandas = pd.read_html(url, encoding='utf-8', attrs={'class':'warning-list-table'}, flavor='lxml')

    # Scraping table header for each table
    table_header_name = soup.find_all('p', class_='text-sm font-semibold text-white text-center max-w-[872px]')

    # Creating list of headers
    table_headers_list = []
    for h in table_header_name:
        h_text = h.get_text(strip=True)
        table_headers_list.append(h_text)

    # Creating list of data frames with warnings for each header
    dfs_list = [df_pandas[i] for i in range(len(df_pandas))]

    # If length of both lists are even assigning headers to each list containing warning data
    if len(table_headers_list) != len(dfs_list):
        raise NameError("Header list and data list are not the same length. Chech the source data.")
    else:
        for i in range(len(dfs_list)):
            dfs_list[i]['Nazwa_listy'] = table_headers_list[i]
    
    return dfs_list