import os
import pandas as pd

penalized = pd.DataFrame(columns = ['Company','Name', 'DiscAct', 'URL', 'SFC ID', 'SFC Link', 'Age in 2020', 'Gender','Role', 'From', 'Until'])
k = 0

for filename in os.listdir("Output Files/Officers/"):
    path = "Output Files/Officers/" + filename
    officers = pd.read_csv(path)
    
    for licensee in range(0,len(officers)):
        if officers['DiscAct'][licensee] == 'None':
            continue
        else:
            penalized = penalized.append(officers.loc[licensee], ignore_index=True)
            penalized['Company'][k] = filename[0:-4]
            k = k + 1