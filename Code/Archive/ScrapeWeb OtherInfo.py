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
companydata = pd.read_csv("Input Files/Company List.csv", dtype = {'SearchQ':str})

OtherInfo = pd.DataFrame()

def nextsib (elem, num):
    for i in range(0, num):
        elem = elem.next_sibling
    return(elem)

for comp in range(0,len(companydata)):
    print (comp)
    code = companydata['SearchQ'][comp]
    url = "https://webb-site.com/dbpub/orgdata.asp?code=" + code + "&Submit=current"
    # setup the page
    page = requests.get(url)
    page.encoding='utf8'
    soup = BeautifulSoup(page.text, 'lxml')
    tables = soup.find_all('table')
    holdings = soup.find_all('h3', id="D0")
    
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
    
    for hld in holdings:
        if nextsib(hld, 10).name == "table":
            holdtbl = nextsib(hld, 10)
            fields =[]
            values=[]
            
            for k in holdtbl.find_all("th"):
                fields.append(k.get_text())
            for k in holdtbl.find_all("td"):
                content = k.get_text()
                if k.find("a"):
                    content = content + " (" + k.find("a").get("href") + ")"
                elif k.find("span"):
                    content = content[0:2]
                values.append(content)
                
        OtherTables.append([code,"Holdings",fields,values])

    OtherInfo = OtherInfo.append(pd.DataFrame(OtherTables))
 
    
OtherInfo.columns=['Company Code','Data Type','Data Columns','Data']
OtherInfo = OtherInfo.reset_index(drop=True)
OtherInfo.to_csv("Output Files/OtherInfo.csv", index = None)

        

    