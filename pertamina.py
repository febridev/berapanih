import time
import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
from sqlalchemy import create_engine

# PERTAMINA
def get_bbm_scrap_pertamina():
    url = "https://mypertamina.id/fuels-harga.html"
    # hdr = {'User-Agent': 'Mozilla/5.0'}
    # req = Request(url,headers=hdr)
    # page = urlopen(req)
    page = requests.get(url)
    soup = BeautifulSoup(page,'html.parser')
    lll = soup.find_all("div",class_ ="card mx-3 slick-slide slick-cloned")
    

    # table1 = soup.find('div')
    print(lll[0])
    # response = requests.get(url)
    # return response.text
    # page = urlopen(url)
    # html = page.read().decode("utf-8")
    # shellsoup = BeautifulSoup(html, 'lxml')
    # print(shellsoup)

if __name__ == '__main__':
    get_bbm_scrap_pertamina()