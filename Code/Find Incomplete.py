import os
import pandas as pd
import shutil

# Check the done folder for unprocessed files
incomplete = []
for filename in os.listdir("Output Files/Officers/"):
    path = "Output Files/Officers/" + filename
    if filename == "Leftovers":
        continue
    officers = pd`.read_csv(path)
    if officers.columns[1] == "DiscAct":
        pass
    else:
        print(filename)
        incomplete.append(filename)
        #shutil.move(path,"Output Files/Officers/Round 2")
          


# check Done folder for incomplete files         
incomplete = []
for filename in os.listdir("Output Files/Officers/Done/"):
    path = "Output Files/Officers/Done/" + filename
    officers = pd.read_csv(path)
    if len(officers['DiscAct']) == 0:
        print(filename)
        incomplete.append(filename)
        

# Check for files without OfficerInfo
incomplete = []
for filename in os.listdir("Output Files/Officers/"):
    path = "Output Files/Officers/" + filename
    if filename == "Done":
        continue
    officers = pd.read_csv(path)
    if officers.columns[2] == "SFC ID":
        pass
    else:
        print(filename)  
        incomplete.append(filename)


# To check for files without SFC ID in done folder
incomplete2 = []
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/"):
    path = "D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/" + filename
    if filename == "Console 3A":
        continue
    if filename == "Console 4A":
        continue
    officers = pd.read_csv(path)
    if officers.columns[2] == "SFC ID":
        pass
    else:
        print(filename)
        incomplete2.append(filename)
        

# To check for files with empty columns for SFC ID and SFC Link
incomplete2 = []
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/"):
    if filename == "Console 3A":
        continue
    if filename == "Console 4A":
        continue
    path = "D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/" + filename
    officers = pd.read_csv(path)
    if isinstance(officers['SFC ID'][0],str): 
        pass
    else:
        print(filename)
        officers = officers.drop(columns = ['SFC ID', 'SFC Link'])
        officers.to_csv(path, index = None)
        incomplete2.append(filename)
        

# Remove index from previous datacheck
        
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/Cleanup/"):
    print(filename)
    path = "D:/Dhruv/Drive/minemydata/Output Files/Officers/Cleanup/" + filename
    officers = pd.read_csv(path)
    if officers.columns[0] == "Unnamed: 0":
        print('fixed')
        officers = officers.drop(columns=['Unnamed: 0'])
        officers.to_csv(path, index = None)


# Cross check for double files
drive = []
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/"):
    drive.append(filename)
    
drivedone = []
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/Done"):
    drivedone.append(filename)

drivedone3a = []
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/Console 3A"):
    drivedone3a.append(filename)

drivedone4a = []
for filename in os.listdir("D:/Dhruv/Drive/minemydata/Output Files/Officers/Done/Console 4A"):
    drivedone4a.append(filename)

gith = []
for filename in os.listdir("Output Files/Officers/"):
    gith.append(filename)

githdone = []
for filename in os.listdir("Output Files/Officers/Done/"):
    githdone.append(filename)

githround2 = []
for filename in os.listdir("Output Files/Officers/Round 2/"):
    githround2.append(filename)
    
dupli = []
for filename in gith:
    if filename in githdone:
        dupli.append(filename)
    elif filename in drive:
        dupli.append(filename)
    elif filename in drivedone:
        dupli.append(filename)
    elif filename in drivedone3a:
        dupli.append(filename)
    elif filename in driv:
        pass
        

fulllist = gith + githdone
dupli = []
for filename in githround2:
    if filename in fulllist:
        dupli.append(filename)
        
for filename in dupli:
    print (filename)
    if filename in gith:
        print ("gith")
    if filename in githdone:
        print('githdone')
    if filename in githround2:
        print('githround2')
    if filename in drivedone4a:
        print('drivedone4a')
    if filename in drivedone3a:
        print('drivedone3a')
    if filename in drivedone:
        print('drivedone')
    if filename in drive:
        print('drive')


#############################
# To look for missing files
    
leaguetable = pd.read_csv("Output Files/LeagueTable.csv")


for filename in leaguetable['Name']:
    if any(filename in s for s in os.listdir("Output Files/Officers")):
        pass
    else:
        print(filename)
        print("missing!")