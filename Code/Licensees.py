# This script goes through the League Table, opens the link for each company and get officer names along with the links to their pages on Webb Site

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Start with the League Table
leaguetable = pd.read_csv("Output Files/LeagueTable.csv")


# Loop 1 to go through all Company Links
for i in leaguetable['SFCLink']:
    
    # Setup temp df for storing data
    sampledf = pd.DataFrame()
    
    # Change the URL to show History
    url = "https://webb-site.com/dbpub/" + re.split('(h=)',i)[0] \
        + "h=N" + re.split('(h=)',i)[2][1:]
    page = requests.get(url)
    page.encoding = 'utf8'
    soup = BeautifulSoup(page.text, 'lxml')
    
    # Print Company name for tracking during scraping
    print(soup.find('h2').text)
    
    table = soup.find_all('table')[0]
    tr = table.find_all('tr')
    
    # Loop 2 for each row of the table
    for j in tr:
        values = []
        td = j.find_all('td')
        
        # <tr> with class 'total' are first rows for each officer. 
        # Consequent tr's are for expired licenses.
        # Expired License rows need extra data cell to compensate for URL
        if j.get('class'):
            pass
        else:
            values.append("")
        
        # Loop 3 for each data cell
        for k in td:
            values.append(k.get_text())
            # Include URL to Officer's page on Webb Site
            if k.find('a'):
                values.append(k.find('a').get('href'))
        
        sampledf = sampledf.append([values])

    sampledf.columns = ['SNo.', 'Name', 'URL', 'Age in 2020', 'Gender', 'Role', 'From', 'Until']
    sampledf = sampledf.reset_index(drop = True)
    
    # Copy info from total rows to expired license rows
    for l in range(1,len(sampledf)):
        if sampledf.loc[l][0] == "":
            sampledf.loc[l][0] = sampledf.loc[l-1][0]
            sampledf.loc[l][1] = sampledf.loc[l-1][1]
            sampledf.loc[l][2] = sampledf.loc[l-1][2]
            sampledf.loc[l][3] = sampledf.loc[l-1][3]
            sampledf.loc[l][4] = sampledf.loc[l-1][4]
        
    sampledf = sampledf.drop(columns = ['SNo.'])
    sampledf = sampledf.drop(sampledf.index[0])
    outputfile = "Output Files/Officers/" + soup.find('h2').text + ".csv"
    sampledf.to_csv(outputfile, index = None)

