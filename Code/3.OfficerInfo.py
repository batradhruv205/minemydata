# This script will go through each company's officers file, open the URL for each officer and get their SFC ID along with the URL for their SFC Page

import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Loop 1 to cycle through all company files
for filename in os.listdir("Output Files/Officers/"):
    print(filename)
    path = "Output Files/Officers/" + filename
    officers = pd.read_csv(path)
    
    officers.insert(2, "SFC ID","")
    officers.insert(3, "SFC Link","")
    
    # Loop 2 to cycle through each officer in the file
    for i in range(0,len(officers)):
        url = "https://webb-site.com/dbpub/natperson.asp?p=" + re.split('p=',officers.loc[i][1])[1]
        page = requests.get(url)
        page.encoding = 'utf8'
        soup = BeautifulSoup(page.text, 'lxml')
        tables = soup.find_all('table')
        
        # Loop 3 to cycle through all tables and identify the appropriate table
        for tb in tables:
            # The required table has the class "opltable"
            if tb.get('class') == ["opltable"]:
                td = tb.find_all('td')
                # Loop 4 goes through each data cell to find the required cell
                for j in range(0,len(td)):
                    if td[j].get_text() == "SFC ID:":
                        SFCID = td[j+1].get_text()
                        SFCLnk = td[j+1].find('a').get('href')
                        officers.set_value(i,'SFC ID',SFCID)
                        officers.set_value(i,'SFC Link',SFCLnk) 
                        break
                break
    officers.to_csv(path, index=None)

#########################################
# Double check for missed out officers
    
import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Loop 1 to cycle through all company files
for filename in os.listdir("Output Files/Officers/"):
    print(filename)
    path = "Output Files/Officers/" + filename
    officers = pd.read_csv(path)
    
    for licensee in range(0, len(officers)):
        if isinstance(officers['SFC ID'][licensee], str):
            pass
        else:
            url = "https://webb-site.com/dbpub/natperson.asp?p=" + re.split('p=',officers.loc[licensee][2])[1]
            page = requests.get(url)
            page.encoding = 'utf8'
            soup = BeautifulSoup(page.text, 'lxml')
            tables = soup.find_all('table')
        
            # Loop 3 to cycle through all tables and identify the appropriate table
            for tb in tables:
                # The required table has the class "opltable"
                if tb.get('class') == ["opltable"]:
                    td = tb.find_all('td')
                    # Loop 4 goes through each data cell to find the required cell
                    for j in range(0,len(td)):
                        if td[j].get_text() == "SFC ID:":
                            SFCID = td[j+1].get_text()
                            SFCLnk = td[j+1].find('a').get('href')
                            officers.set_value(licensee,'SFC ID',SFCID)
                            officers.set_value(licensee,'SFC Link',SFCLnk) 
                            break
                    break
    officers.to_csv(path, index=None)