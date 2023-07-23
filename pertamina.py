import time
import os
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from sqlalchemy import create_engine,text

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def bbmtype(var1):
    match var1:
        case 0:
            return "Pertamax Turbo"
        case 1:
            return "Pertamax"
        case 2:
            return "Pertalite"
        case 3:
            return "Pertamina Dex"
        case 4:
            return "Pertamina Dexlite"
        case 5:
            return "Bio Solar"
        case default:
            return "none"

def get_bbm_pertamina(params):

    seleniumserver = params.serverurl
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Remote(
        command_executor=seleniumserver+'/wd/hub',options=options
    )
    # options.add_argument('--no-sandbox')
    # options.add_argument('headless')
    # options.add_argument('--disable-infobars')
    # options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome()
    driver.get("https://mypertamina.id/fuels-harga")
    pertaminashoup = driver.page_source
    pshoup = BeautifulSoup(pertaminashoup,'lxml')

    user = params.user
    password = params.passdb
    host = params.host
    port = params.port
    dbname = params.dbname
    tblname = params.tblname

    opendb = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    opendb.connect()

    # truncate the table before insert
    sqltext="truncate table "+tblname+";"
    opendb.engine.execute(sqltext)
    # opendb.close()


    # GET TIMESTAMP
    now = time.time()

    # HARD CODE loop for get data
    nvalue = range(0,6)
    for nll in nvalue:
        lsprov=[]
        lsharga=[]
        d ={}
        bbmtipe = bbmtype(nll)
        fdiv = str(pshoup.find_all("div",{"data-slick-index": nll}))
        getlabel = BeautifulSoup(fdiv,'lxml')
        provinsi = getlabel.find_all("label",{"class":"text-sm"})
        harga = getlabel.find_all("label",{"class":"text-danger"})

        # Make List Provinsi
        for lprov in provinsi:
            lsprov.append(lprov.text)
        
        for lharga in harga:
            lsharga.append(lharga.text)
        
        # remove prefix Prov.
        clean1 = [i.replace('Prov. ', '') for i in lsprov]
        # remove prefix Rp.
        clean2 = [h.replace('Rp ', '') for h in lsharga]

        # remove prefix comma separator ,
        clean3 = [c.replace(',', '') for c in clean2]

        # remove prefix -
        clean4 = [c3.replace('‐', '0') for c3 in clean3]

        # Set schema data frame
        d = {'tipebbm':bbmtipe, 'provinsi':clean1, 'harga':clean4, 'created_date':now}
        # set option disable max_rows
        pd.set_option('display.max_rows', None)
        # assign dataframe 
        df = pd.DataFrame(d)
        # insert from dataframe to table on database
        df.to_sql(name=tblname, con=opendb, if_exists="append", index=False)
        print("insert data "+ str(nll))
        # print(df)

    # # Make Dict
    # mpertamina = dict(zip(clean1, clean3))
    # print(mpertamina)


    # Make Data Frame


    # print(lsprov)
    # print(pshoup.find_all("img",{"class":"img-fluid"}))
    # print(help(fdiv))

    # driver.implicitly_wait(60) # 10 second wait
    # bbmprice = driver.find_element(By.CLASS_NAME,"card")
    # jsjsj = bbmprice.find_element(By.CLASS_NAME,"card-body")
    # kkk = jsjsj.find_element(By.CLASS_NAME,"d-flex")
    # lllll = driver.find_element(By.XPATH,'//div[@class="d-flex justify-content-between"]')

    # for i in kkk:
    #     print(i.text)


    # assert "Python" in driver.title
    # elem = driver.find_element(By.NAME, "q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source

    # CLOSE SESSION SELENIUM
    # driver.close()
    driver.quit()
    # CLOSE SESSION DATABASE
    opendb.dispose()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parameter for pertamina bbm')
    parser.add_argument('--user',help='user name for database')
    parser.add_argument('--passdb',help='password  for database')
    parser.add_argument('--host',help='ip or dns for database')
    parser.add_argument('--port',help='port for database')
    parser.add_argument('--dbname',help='dbname for database')
    parser.add_argument('--tblname',help='tblname for the table where we will write the results')
    parser.add_argument('--serverurl',help='dns or url for selennium server')


    # put all parameter to one variable 
    args = parser.parse_args()
    get_bbm_pertamina(args) 

