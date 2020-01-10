# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 23:46:28 2019

@author: batra
"""

import pandas as pd
import re

# Function to split column names and row contents
def conv2dt(text):
    clean = text.replace("'","").replace("\\n","").replace("\\r","").\
        replace("\\t","").replace(" ","")
    split = clean[1:len(clean)-1].split(",")
    return(split)

def conv2dt2(text):
    clean = re.findall("'.*?'",text.replace("\\n","").replace("\\r","").\
        replace("\\t",""))
    for i in range(len(clean)):
        clean[i] = clean[i][1:-1]
    return(clean)
    
OtherInfo = pd.read_csv("Output Files/OtherInfo.csv")
# Look at the types of data tables
OtherInfo['DType']=""
for i in range(0,len(OtherInfo)):
    if OtherInfo['Data Type'][i].find("Listed securities") == 0 :
        OtherInfo['DType'][i] = "Listed securities"
    else:
        OtherInfo['DType'][i] = OtherInfo['Data Type'][i]


DTypes = pd.DataFrame(OtherInfo[['DType','Data Columns']])
DTypes = DTypes.drop_duplicates()
DTypes = DTypes.reset_index(drop=True)

# Look for unknown table types
TableTypes = ['Foreign registrations','Name history', 'Reorganised from', \
              'Listed securities', 'Domicile history']
for i in DTypes['DType']:
    if i not in TableTypes:
        print(i)
        print("Unknown table type found!")

# Create new dataframes for storing OtherInfo
ForReg = pd.DataFrame(columns = conv2dt2(DTypes.loc[DTypes['DType']==\
                                                   "Foreign registrations"]\
                                        ['Data Columns'][0]))
ForReg.insert(0, "CompanyCode","")

NamHist = pd.DataFrame(columns = conv2dt2(DTypes.loc[DTypes['DType']==\
                                                    "Name history"]\
                                         ['Data Columns'][1]))
NamHist.insert(0, "CompanyCode","")

ReFrom = pd.DataFrame(columns = conv2dt2(DTypes.loc[DTypes['DType']==\
                                                   "Reorganised from"]\
                                        ['Data Columns'][2]))
ReFrom.insert(0, "CompanyCode","")

LisSec = pd.DataFrame(columns = conv2dt2(DTypes.loc[DTypes['DType']==\
                                                   "Listed securities"]\
                                        ['Data Columns'][3]))
LisSec.insert(0, 'Type',"")
LisSec.insert(0, "CompanyCode","")

DomHist = pd.DataFrame(columns = conv2dt2(DTypes.loc[DTypes['DType']==\
                                                    "Domicile history"]\
                                         ['Data Columns'][4]))
DomHist.insert(0, "CompanyCode","")


for i in range(len(OtherInfo)):
    if OtherInfo['DType'][i] == "Foreign registrations":
        col1 = OtherInfo.loc[i][0]
        data = conv2dt2(OtherInfo.loc[i][3])
        for i in range(0,int(len(data)/(len(ForReg.columns)-1))):
            col2 = data[4*i+0]
            col3 = data[4*i+1]
            col4 = data[4*i+2]
            col5 = data[4*i+3]
            ForReg = ForReg.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Place":[col2], \
                             "ID":[col3],"Registered":[col4],"Ceased":[col5]}))
    
    elif OtherInfo['DType'][i] == "Name history":
        col1 = OtherInfo.loc[i][0]
        data = conv2dt2(OtherInfo.loc[i][3])
        for i in range(0,int(len(data)/(len(NamHist.columns)-1))):
            col2 = data[3*i+0]
            col3 = data[3*i+1]
            col4 = data[3*i+2]
            NamHist = NamHist.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Old English name":[col2], \
                             "Old Chinese name":[col3],"Until":[col4]}))
                           
    elif OtherInfo['DType'][i] == "Reorganised from":
        col1 = OtherInfo.loc[i][0]
        data = conv2dt2(OtherInfo.loc[i][3])
        for i in range(0,int(len(data)/(len(ReFrom.columns)-1))):
            col2 = data[3*i+0]
            col3 = data[3*i+1]
            col4 = data[3*i+2]
            ReFrom = ReFrom.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Current English name":[col2], \
                             "Chinese name":[col3],"Effective":[col4]}))
    elif OtherInfo['DType'][i] == "Listed securities":
        col1 = OtherInfo.loc[i][0]
        col2 = OtherInfo.loc[i][1][19:-1]
        data = conv2dt2(OtherInfo.loc[i][3])
        for i in range(0,int(len(data)/(len(LisSec.columns)-2))):
            col3 = data[2*i+0]
            col4 = data[2*i+1]
            col5 = data[2*i+2]
            col6 = data[2*i+3]
            col7 = data[2*i+4]
            col8 = data[2*i+5]
            LisSec = LisSec.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Type":[col2], \
                             "Market":[col3],"Code":[col4],"List":[col5],\
                                 "Last trade":[col6],"Delist":[col7],"Notes":[col8]}))
        
    elif OtherInfo['DType'][i] == "Domicile history":
        col1 = OtherInfo.loc[i][0]
        data = conv2dt2(OtherInfo.loc[i][3])
        for i in range(0,int(len(data)/(len(DomHist.columns)-1))):
            col2 = data[3*i+0]
            col3 = data[3*i+1]
            DomHist = DomHist.append(pd.DataFrame\
                           ({"CompanyCode":[col1],"Old domicile":[col2], \
                             "Until":[col3]}))
    ForReg = ForReg.reset_index(drop=True)
    NamHist = NamHist.reset_index(drop=True)
    DomHist = DomHist.reset_index(drop=True)
    LisSec = LisSec.reset_index(drop=True)
    ReFrom = ReFrom.reset_index(drop=True)
    
ForReg.to_csv("Output Files/ForReg.csv")
NamHist.to_csv("Output Files/NamHist.csv")
DomHist.to_csv("Output Files/DomHist.csv")
LisSec.to_csv("Output Files/LisSec.csv")
ReFrom.to_csv("Output Files/ReFrom.csv")