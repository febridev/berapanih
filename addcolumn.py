import time
import os
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from sqlalchemy import create_engine


def get_bbm_scrap(): 
    url = "https://www.shell.co.id/in_id/pengendara-bermotor/bahan-bakar-shell/how-shell-price-fuel.html"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    shellsoup = BeautifulSoup(html, 'lxml')

    
    # print(shellsoup)
    table1 = shellsoup.find('table')
    judul=[]
    for dd in table1.find_all('th'):
        title = dd.text
        judul.append(title)

    # set title to lower
    judul[0] = "lokasi"
    judul[1] = "shell_super"
    judul[2] = "shell_v_power"
    judul[3] = "shell_v_power_diesel"
    judul[4] = "shell_diesel_extra"
    judul[5] = "shell_v_power_nitro_plus"

    print(judul)
    
    # get data and cleansing 
    mydata = pd.DataFrame(columns=judul) 
    for j in table1.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        clean1 = [s.replace("IDR","") for s in row]
        clean2 = [dd.replace(",","") for dd in clean1]
        clean3 = [ll.replace("N/A","0") for ll in clean2]
        length = len(mydata)
        mydata.loc[length] = clean3
        # print(clean3)
    

    #add created_date
    now = time.time()
    nemydata = mydata.assign(created_date=now)
    print(nemydata)
    # print(nemydata)
    # Export Dataframe
    # mydata.to_csv('export/bbm_shell.csv', index=False)

if __name__ == '__main__':
    get_bbm_scrap()