import time
import os
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from sqlalchemy import create_engine

# PERTAMINA
def get_bbm_scrap_pertamina(params):
    url = "https://mypertamina.id/fuels-harga"
    page = urlopen(url)
    

# SHELL
def get_bbm_scrap(params): 
    user = params.user
    password = params.passdb
    host = params.host
    port = params.port
    dbname = params.dbname
    tblname = params.tblname

    url = "https://www.shell.co.id/in_id/pengendara-bermotor/bahan-bakar-shell/how-shell-price-fuel.html"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    shellsoup = BeautifulSoup(html, 'lxml')

    opendb = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    opendb.connect()
    print(opendb)
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
    mydata = mydata.assign(created_date=now)

    # Export Dataframe
    mydata.to_csv('export/bbm_shell.csv', index=False)

    # Insert into table 
    mydata.to_sql(name=tblname, con=opendb, if_exists='replace', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='data bbm shell')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--passdb', help='password name for postgres')
    parser.add_argument('--host', help='host name for postgres')
    parser.add_argument('--port', help='port name for postgres')
    parser.add_argument('--dbname', help='db name for postgres')
    parser.add_argument('--tblname', help='name of the table where we will write the results to')
    

    args = parser.parse_args()
    while True:
        print("Prepare..")
        get_bbm_scrap(args)
        print("Refresh Until 1 Hours ..")
        time.sleep(3600)