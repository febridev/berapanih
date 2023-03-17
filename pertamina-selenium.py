import time
import os
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from sqlalchemy import create_engine

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://mypertamina.id/fuels-harga")
pertaminashoup = driver.page_source
pshoup = BeautifulSoup(pertaminashoup,'lxml')
fdiv = pshoup.find_all("div",{"class": "card-body"})

print(fdiv)
driver.implicitly_wait(60) # 10 second wait
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
driver.close()