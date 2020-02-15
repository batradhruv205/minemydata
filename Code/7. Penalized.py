import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time


driver = webdriver.Firefox(executable_path = "..\..\..\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe")

penalized = pd.read_csv("Output Files/Penalized.csv")
DiscAct = pd.DataFrame()

for licensee in range(232, len(penalized)):
    print(licensee)
    if isinstance(penalized['SFC Link'][licensee], str):
        pass
    else:
        continue
    url = penalized['SFC Link'][licensee][0:-13] + "disciplinaryAction"
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    div = soup.find_all('div', id='griddisremark-body')
    if len(div) == 0:
        continue
    tables = div[0].find_all('table', attrs={'class':'x-grid-table x-grid-table-resizer'})
    td = tables[0].find_all('td')
    values = []
    values.append(penalized['Company'][licensee])
    values.append(penalized['Name'][licensee])
    values.append(penalized['SFC Link'][licensee])
    n = 0
    for cells in td:
        values.append(cells.text)
        if cells.find_all('a'):
            for links in cells.find_all('a'):
                values.append(links.get('href'))
        n = n + 1
        if n == 3:
            DiscAct = DiscAct.append([values])
            n = 0
            values = []
            values.append(penalized['Company'][licensee])
            values.append(penalized['Name'][licensee])
            values.append(penalized['SFC Link'][licensee])
    
DiscAct.columns = ['Company', 'Name', 'SFC Link', 'Date', 'Action', 'Lang', 'Eng Release', 'Ch Release']
DiscAct = DiscAct.drop(columns = 'Lang')
DiscAct = DiscAct.reset_index(drop = True)
DiscAct.insert(7, 'Temp', "")
for i in range(0, len(DiscAct)):
    DiscAct.at[i,'Temp'] = DiscAct['Name'][i] + DiscAct['Action'][i]
DiscAct = DiscAct.drop_duplicates(subset = 'Temp')
DiscAct = DiscAct.drop(columns = 'Temp')
DiscAct.to_csv("Output Files/DiscAct.csv", index = None)