import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Firefox(executable_path = "..\..\..\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe")

discact = []
# Loop 1 to cycle through all company files
for filename in os.listdir("Output Files/Officers/Leftovers/"):
    print(filename)
    if filename =="Done":
        continue
    if filename == "Round 2":
        continue
    path = "Output Files/Officers/Leftovers/" + filename
    officers = pd.read_csv(path)
    officers.insert(1, 'DiscAct', "")
    
    # Loop 2 to cycle through each officer for a company
    for licensee in range(0,len(officers)):
        if isinstance(officers['SFC Link'][licensee], str):
            pass
        else:
            continue
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





###########################################3
# Double Check identified officers.
    
newdriver = webdriver.Firefox(executable_path = "..\..\..\Downloads\geckodriver-v0.26.0-win64\geckodriver.exe")

# Loop 1 to go through each file
for filename in os.listdir("Output Files/Officers/Done"):
    print(filename)
    if filename == "Checked":
        continue
    path = "Output Files/Officers/Done/" + filename
    officers = pd.read_csv(path)
    
    # Loop 2 to go through each licensee
    for licensee in range(0,len(officers)):
        if officers['DiscAct'][licensee] != "None":
            if isinstance(officers['SFC Link'][licensee], str):
                pass
            else:
                continue
            url = officers['SFC Link'][licensee][0:-13] + "disciplinaryAction"
            
            officers = officers.astype({'DiscAct':str})
            newdriver.get(url)
            time.sleep(1)
            soup = BeautifulSoup(newdriver.page_source, 'lxml')
        
            div = soup.find_all('div',id='gridview-1013')
            if div:
                if div[0].text == "None":
                    print('none')
                    officers.set_value(licensee, 'DiscAct', "None")
                    officers.set_value
                else:
                    print('FOUND 1!!!!!!!!!!!!!!!!!!!')               
    officers.to_csv(path, index = None)