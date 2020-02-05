# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 16:47:07 2020

@author: batra
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

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

############################
OtherInfo['DType']=""
for i in range(0,len(OtherInfo)):
    if OtherInfo['Data Type'][i].find("Listed securities") == 0 :
        OtherInfo['DType'][i] = "Listed securities"
    else:
        OtherInfo['DType'][i] = OtherInfo['Data Type'][i]


DTypes = pd.DataFrame(OtherInfo[['DType','Data Columns']])
DTypes = DTypes.drop_duplicates(subset="DType")
DTypes = DTypes.reset_index(drop=True)

# Look for unknown table types
TableTypes = ['Foreign registrations','Name history', 'Reorganised from', \
              'Listed securities', 'Domicile history', 'Holdings']
for i in DTypes['DType']:
    if i not in TableTypes:
        print(i)
        print("Unknown table type found!")
        

# Create new dataframes for storing OtherInfo
ForReg = pd.DataFrame(columns = DTypes.loc[DTypes['DType']==\
                                           "Foreign registrations"]\
                                        ['Data Columns'][0])
ForReg.insert(0, "CompanyCode","")

NamHist = pd.DataFrame(columns = DTypes.loc[DTypes['DType']==\
                                                    "Name history"]\
                                         ['Data Columns'][1])
NamHist.insert(0, "CompanyCode","")

ReFrom = pd.DataFrame(columns = DTypes.loc[DTypes['DType']==\
                                                   "Reorganised from"]\
                                        ['Data Columns'][2])
ReFrom.insert(0, "CompanyCode","")

LisSec = pd.DataFrame(columns = DTypes.loc[DTypes['DType']==\
                                                   "Listed securities"]\
                                        ['Data Columns'][3])
LisSec.insert(0, 'Type',"")
LisSec.insert(0, "CompanyCode","")

Holds = pd.DataFrame(columns = DTypes.loc[DTypes['DType']==\
                                                    "Holdings"]\
                                         ['Data Columns'][4])
Holds.insert(0, "CompanyCode", "")

DomHist = pd.DataFrame(columns = DTypes.loc[DTypes['DType']==\
                                                    "Domicile history"]\
                                          ['Data Columns'][5])
DomHist.insert(0, "CompanyCode","")


for i in range(len(OtherInfo)):
    if OtherInfo['DType'][i] == "Foreign registrations":
        col1 = OtherInfo.loc[i][0]
        for k in range(0,int(len(OtherInfo.loc[i][3])/(len(ForReg.columns)-1))):
            col2 = OtherInfo.loc[i][3][4*k+0]
            col3 = OtherInfo.loc[i][3][4*k+1].replace("\n","").replace("\r","").\
                replace("\t","").replace(" ","")
            col4 = OtherInfo.loc[i][3][4*k+2]
            col5 = OtherInfo.loc[i][3][4*k+3]
            ForReg = ForReg.append(pd.DataFrame\
                               ({"CompanyCode":[col1],"Place":[col2], \
                                 "ID":[col3],"Registered":[col4],"Ceased":[col5]}))
    elif OtherInfo['DType'][i] == "Name history":
        col1 = OtherInfo.loc[i][0]
        for k in range(0,int(len(OtherInfo.loc[i][3])/(len(NamHist.columns)-1))):
            col2 = OtherInfo.loc[i][3][3*k+0]
            col3 = OtherInfo.loc[i][3][3*k+1]
            col4 = OtherInfo.loc[i][3][3*k+2]
            NamHist = NamHist.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Old English name":[col2], \
                             "Old Chinese name":[col3],"Until":[col4]}))
    elif OtherInfo['DType'][i] == "Reorganised from":
        col1 = OtherInfo.loc[i][0]
        for k in range(0,int(len(OtherInfo.loc[i][3])/(len(ReFrom.columns)-1))):
            col2 = OtherInfo.loc[i][3][3*k+0]
            col3 = OtherInfo.loc[i][3][3*k+1]
            col4 = OtherInfo.loc[i][3][3*k+2]
            ReFrom = ReFrom.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Current English name":[col2], \
                             "Chinese name":[col3],"Effective":[col4]}))
    elif OtherInfo['DType'][i] == "Listed securities":
        col1 = OtherInfo.loc[i][0]
        col2 = OtherInfo.loc[i][1][19:-1]
        for k in range(0,int(len(OtherInfo.loc[i][3])/(len(LisSec.columns)-2))):
            col3 = OtherInfo.loc[i][3][6*k+0]
            col4 = OtherInfo.loc[i][3][6*k+1]
            col5 = OtherInfo.loc[i][3][6*k+2]
            col6 = OtherInfo.loc[i][3][6*k+3]
            col7 = OtherInfo.loc[i][3][6*k+4]
            col8 = OtherInfo.loc[i][3][6*k+5]
            LisSec = LisSec.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Type":[col2], \
                             "Market":[col3],"Code":[col4],"List":[col5],\
                                 "Last trade":[col6],"Delist":[col7],"Notes":[col8]}))
    elif OtherInfo['DType'][i] == "Holdings":
        col1 = OtherInfo.loc[i][0]
        for k in range(0,int(len(OtherInfo.loc[i][3])/(len(Holds.columns)-1))):
            col2 = OtherInfo.loc[i][3][7*k+0]
            col3 = OtherInfo.loc[i][3][7*k+1]
            col4 = OtherInfo.loc[i][3][7*k+2]
            col5 = OtherInfo.loc[i][3][7*k+3]
            col6 = OtherInfo.loc[i][3][7*k+4]
            col7 = OtherInfo.loc[i][3][7*k+5]
            col8 = OtherInfo.loc[i][3][7*k+6]
            Holds = Holds.append(pd.DataFrame\
                                 ({"CompanyCode":[col1],"Issuer":[col2],\
                                   "🌐":[col3],"Formed":[col4], "Issue":[col5]\
                                       , "Shares":[col6], "Stake":[col7],\
                                           "Holding date":[col8]}))
    elif OtherInfo['DType'][i] == "Domicile history":
        col1 = OtherInfo.loc[i][0]
        for k in range(0,int(len(OtherInfo.loc[i][3])/(len(DomHist.columns)-1))):
            col2 = OtherInfo.loc[i][3][2*k+0]
            col3 = OtherInfo.loc[i][3][2*k+1]
            DomHist = DomHist.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Old domicile":[col2], \
                             "Until":[col3]}))
    
    ForReg = ForReg.reset_index(drop=True)
    NamHist = NamHist.reset_index(drop=True)
    DomHist = DomHist.reset_index(drop=True)
    LisSec = LisSec.reset_index(drop=True)
    ReFrom = ReFrom.reset_index(drop=True)
    Holds = Holds.reset_index(drop=True)
    
Holds.insert(2,"URL","")

for i in range(0,len(Holds)):
    url = "https://webb-site.com/dbpub/"+ re.findall("\(orgdata\.asp\?.*\)",Holds['Issuer'][i])[0][1:-1]
    Holds['URL'][i] = url
    Holds['Issuer'][i] = Holds['Issuer'][i][:(re.search("\(orgdata.*\)",Holds['Issuer'][i]).start(0)-1)]
    

ForReg.to_csv("Output Files/ForReg.csv", index=None)
NamHist.to_csv("Output Files/NamHist.csv", index=None)
DomHist.to_csv("Output Files/DomHist.csv", index=None)
LisSec.to_csv("Output Files/LisSec.csv", index=None)
ReFrom.to_csv("Output Files/ReFrom.csv", index=None)
Holds.to_csv("Output Files/Holds.csv", index=None)