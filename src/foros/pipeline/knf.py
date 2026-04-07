import pandas as pd
import requests
from bs4 import BeautifulSoup

def knf_warning() -> pd.DataFrame:
    # URL for scraping
    url = "https://www.knf.gov.pl/dla_konsumenta/ostrzezenia_publiczne"

    # Scraping data from knf warnings lists using pandas read_html
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    dfs = pd.read_html(
        response.text
      , encoding='utf-8'
      , attrs={'class':'warning-list-table'}
      , flavor='lxml'
     )

    # Creating list of headers
    headers = [
         h.get_text(strip=True)
         for h in soup.find_all('p', class_='text-sm font-semibold text-white text-center max-w-[872px]')
    ]

    # If length of both lists are even assigning headers to each list containing warning data
    if len(headers) != len(dfs):
        raise ValueError("Header list and data list are not the same length. Chech the source data.")
    
    # Creating list of data frames with warnings for each header
    dfs_list = [
        df.assign(Nazwa_listy=header)
        for df, header in zip(dfs, headers)
    ]

    return pd.concat(dfs_list, axis=0, ignore_index=True)