# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 00:07:38 2020

@author: batra
"""

import pandas as pd
import re

holdings = pd.read_csv("Output Files/Holds.csv")
holdings.insert(2,"URL","")


for i in range(0,len(holdings)):
    url = "https://webb-site.com/dbpub/"+ re.findall("\(orgdata\.asp\?.*\)",holdings['Issuer'][i])[0][1:-1]
    holdings['URL'][i] = url
    holdings['Issuer'][i] = holdings['Issuer'][i][:(re.search("\(orgdata.*\)",holdings['Issuer'][i]).start(0)-1)]
    