import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Firefox(executable_path = "..\..\..\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe")

discact = []
# Loop 1 to cycle through all company files
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/Console 3A/"):
    print(filename)
    path = "D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/Console 3A/" + filename
    officers = pd.read_csv(path)
    officers.insert(1, 'DiscAct', "")
    
    # Loop 2 to cycle through each officer for a company
    for licensee in range(0,len(officers)):
        url = officers['SFC Link'][licensee][0:-13] + "disciplinaryAction"

        driver.get(url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        div = soup.find_all('div',id='gridview-1013')
        if div:
            if div[0].text == "None":
                print('none')
                officers.set_value(licensee, 'DiscAct', "None")
            else:
                discact.append(filename)
                print('FOUND 1!!!!!!!!!!!!!!!!!!!')
                
    officers.to_csv(path, index = None)



