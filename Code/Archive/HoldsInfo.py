# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 19:28:35 2020

@author: batra
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

Holds = pd.read_csv("Output Files/Holds.csv")
HoldsInfo = pd.DataFrame()

for i in range(0, len(Holds)):
    print(Holds['CompanyCode'][i])
    url = Holds['URL'][i]
    # setup the page
    page = requests.get(url)
    page.encoding = 'utf8'
    soup = BeautifulSoup(page.text, 'lxml')
    tables = soup.find_all('table')
    
    # setup empty lists to store information
    fields = []
    values = []
    
    # Basic Info
    # [BUG] /n pops up around links.
    # Will have to update counter names when the loop is nested into the parent loop.

    # Company Name
    fields.append('Company Name')
    values.append(soup.h2.get_text())

    # First Table
    table0 = tables[0].find_all('td')
    j=0
    for k in range(0,int(len(table0)/2)):
        fields.append(table0[j].get_text())
        j=j+1
        values.append(table0[j].get_text().strip())
        j=j+1

    BasicInfoTemp = pd.DataFrame([values])
    BasicInfoTemp.columns = fields
    
    # Apppend BasicInfoTemp to Basic Info.
    # If there are new columns, then BasicInfo should add that column and set values for other rows as NA
    HoldsInfo=HoldsInfo.append(BasicInfoTemp)
    
HoldsInfo = HoldsInfo.reset_index(drop=True)
HoldsInfo = HoldsInfo.rename(columns={'Company Name':'Issuer'})

HoldsTable = Holds.merge(HoldsInfo, left_index=True, right_index=True)
HoldsTable = HoldsTable.drop(columns=['Issuer_x','🌐','CompanyCode_y'])

HoldsTable = HoldsTable[['CompanyCode_x','Issuer_y','Domicile:','Shares','Stake','Holding date','Formed','Issue','Dissolved date:','Formed','Incorporation number:','Last check on companies registry:','PIBA ID:', 'Primary Listing:', 'SFC ID:', 'Status:', 'Type:','Web sites:', 'Year-end:','URL']]
HoldsTable = HoldsTable.rename(columns={'CompanyCode_x':'CompanyCode','Issuer_y':'Issuer'})

HoldsTable.to_csv("Output Files/HoldsInfo.csv", index = None)
