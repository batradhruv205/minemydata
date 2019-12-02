ing# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 23:46:28 2019

@author: batra
"""

import pandas as pd

OtherInfo = pd.read_csv("OtherInfo.csv")

DTypes = OtherInfo['Data Type']
DTypes = pd.DataFrame(DTypes)
DTypes = DTypes.drop_duplicates()
DTypes = DTypes.reset_index(drop=True)
DTypes['Type'] = ""

for i in range(0,len(DTypes)):
    if DTypes['Data Type'][i].find("Listed securities") == 0 :
        DTypes['Type'][i] = "Listed securities"
    else:
        DTypes['Type'][i] = DTypes['Data Type'][i]

DTables = pd.DataFrame(DTypes['Type'])
DTables = DTables.drop_duplicates()
DTables = DTables.reset_index(drop=True)

OtherTables={}

for i in range(0, len(DTables)):
    OtherTables[DTables['Type'][i]]=pd.DataFrame()