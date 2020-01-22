# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 00:32:19 2020

@author: batra
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://webb-site.com/dbpub/SFClicount.asp"
page = requests.get(url)
page.encoding = 'utf8'
soup = BeautifulSoup(page.text, 'lxml')
tables = soup.find_all('table')
tr = tables[0].find_all('tr')

leaguetable = pd.DataFrame()

for i in range(0, len(tr)):
    values = []
    td = tr[i].find_all('td')
    if td:
        for k in range(0,len(td)):
            values.append(td[k].get_text())
            if td[k].find_all('a'):
                values.append(td[k].find('a').get("href"))
        leaguetable = leaguetable.append([values])

    
leaguetable.columns = ['Row', 'Name', 'SFCLink','ROs', 'Reps', 'Total', 'Reps v total%', 'LicenseStats','Licensed']
leaguetable = leaguetable.drop(columns='Row').reset_index(drop=True)
leaguetable = leaguetable.reset_index(drop=True)

leaguetable.to_csv("Output Files/LeagueTable.csv",index=None)