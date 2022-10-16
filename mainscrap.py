from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

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
    
judul[0] = "lokasi"
judul[1] = "shell_super"
judul[2] = "shell_v_power"
judul[3] = "shell_v_power_diesel"
judul[4] = "shell_diesel_extra"
judul[5] = "shell_v_power_nitro_plus"


print(judul)

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

print(mydata)

# print(judul)
# print(table1)
# print(shellsoup.get_text())

# hasil = shellsoup.find_all("td")

# for data in hasil:
    