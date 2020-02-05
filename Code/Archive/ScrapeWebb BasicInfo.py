# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:01:21 2019

@author: batra
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
# This is the mac Command
#companydata = pd.read_csv("Company List.csv", dtype = {'SearchQ':str})
# This is the Win Command
companydata = pd.read_csv("Input Files/Company List.csv", dtype = {'SearchQ':str})

BasicInfo = pd.DataFrame()

# This loop collects basic info for all companies
for comp in range(0,len(companydata)):
    
    code = companydata['SearchQ'][comp]
    print(code)
    url = "https://webb-site.com/dbpub/orgdata.asp?code=" + code + "&Submit=current"
    # setup the page
    page = requests.get(url)
    page.encoding = 'utf8'
    soup = BeautifulSoup(page.text, 'lxml')
    
    # all info is available in tables
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
    fields.append('Company Code')
    values.append(code)

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
    BasicInfo=BasicInfo.append(BasicInfoTemp)

BasicInfo = BasicInfo.reset_index(drop=True)
BasicInfo.to_csv("Output Files/BasicInfo.csv", index=None)
