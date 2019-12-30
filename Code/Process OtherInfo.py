# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 23:46:28 2019

@author: batra
"""

import pandas as pd

OtherInfo = pd.read_csv("Output Files/OtherInfo.csv")

DTypes = pd.DataFrame(OtherInfo[['Data Type','Data Columns']])
DTypes = DTypes.drop_duplicates()
DTypes = DTypes.reset_index(drop=True)
DTypes['Type'] = ""

for i in range(0,len(DTypes)):
    if DTypes['Data Type'][i].find("Listed securities") == 0 :
        DTypes['Type'][i] = "Listed securities"
    else:
        DTypes['Type'][i] = DTypes['Data Type'][i]

DTables = pd.DataFrame(DTypes[['Type','Data Columns']])
DTables = DTables.drop_duplicates()
DTables = DTables.reset_index(drop=True)

# Look for unknown table types
TableTypes = ['Foreign registrations','Name history', 'Reorganised from', \
              'Listed securities', 'Domicile history']
for i in DTables['Type']:
    if i not in TableTypes:
        print(i)
        print("Unknown table type found!")

# Create new dataframes for storing OtherInfo
cols = DTables.loc[DTables['Type']=="Foreign registrations"]['Data Columns'][0].replace("'","")
ForReg = pd.DataFrame(columns = cols[1:len(cols)-1].split(","))
ForReg.insert(0, "CompanyCode","")

cols = DTables.loc[DTables['Type']=="Name history"]['Data Columns'][1].replace("'","")
NamHist = pd.DataFrame(columns = cols[1:len(cols)-1].split(","))
NamHist.insert(0, "CompanyCode","")

cols = DTables.loc[DTables['Type']=="Reorganised from"]['Data Columns'][2].replace("'","")
ReFrom = pd.DataFrame(columns = cols[1:len(cols)-1].split(","))
ReFrom.insert(0, "CompanyCode","")

cols = DTables.loc[DTables['Type']=="Listed securities"]['Data Columns'][3].replace("'","")
LisSec = pd.DataFrame(columns = cols[1:len(cols)-1].split(","))
LisSec.insert(0, 'Type',"")
LisSec.insert(0, "CompanyCode","")

cols = DTables.loc[DTables['Type']=="Domicile history"]['Data Columns'][4].replace("'","")
DomHist = pd.DataFrame(columns = cols[1:len(cols)-1].split(","))
DomHist.insert(0, "CompanyCode","")

# Loop through OtherInfo to populate OtherInfo Tables
# covert 'Data' from OtherInfo to a readable version
# include company codes
# manage listed securities type