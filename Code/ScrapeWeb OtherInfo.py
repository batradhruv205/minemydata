# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:29:18 2019

@author: batra
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
# This is the mac Command
#companydata = pd.read_csv("Company List.csv", dtype = {'SearchQ':str})
# This is the Win Command
companydata = pd.read_csv("G:/My Drive/Academics/HKU/Misc/Alan's Work/Company List.csv", dtype = {'SearchQ':str})

OtherInfo = pd.DataFrame()

for comp in range(0,len(companydata)):
#    # These lines are controlling the parent loop
#    if comp > 0:
#        print (comp)
#        del comp
#        break
#    comp = 3
    print (comp)
    code = companydata['SearchQ'][comp]
    url = "https://webb-site.com/dbpub/orgdata.asp?code=" + code + "&Submit=current"
    # setup the page
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    tables = soup.find_all('table')
    heading3s = soup.find_all('h3')
    heading4s = soup.find_all('h4')
    
    OtherTables =[]
    
    for tb in tables:
        fields =[]
        values=[]
    
        tbprev = tb.previous_sibling.previous_sibling
        tbprev2 = tbprev.previous_sibling.previous_sibling
        
        if tbprev.name == 'h3':
            for k in tb.find_all('th'):
                fields.append(k.get_text())
            for k in tb.find_all('td'):
                values.append(k.get_text())
            OtherTables.append([code,tbprev.get_text(),fields,values])
        
        elif tbprev.name =='h4':
            if tbprev2.name == 'h3':
                parentheading = tbprev2.get_text()
            datatype = parentheading + ": " + tbprev.get_text()
            
            for k in tb.find_all('th'):
                fields.append(k.get_text())
            for k in tb.find_all('td'):
                values.append(k.get_text())
            OtherTables.append([code,datatype,fields,values])
        
        else:
            continue
    OtherInfo = OtherInfo.append(pd.DataFrame(OtherTables))
 
    
OtherInfo.columns=['Company Code','Data Type','Data Columns','Data']
OtherInfo = OtherInfo.reset_index(drop=True)
OtherInfo.to_csv("C:/Users/batra/Documents/GitHub/minemydata/Output Files/OtherInfo.csv", index = None)
# Need to convert OtherInfo into more readable tables
        

    
    