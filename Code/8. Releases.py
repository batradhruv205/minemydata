import pandas as pd
import requests
import PyPDF2

discact = pd.read_csv("Output Files/DiscAct.csv")

discact.insert(7, 'EngText', "")
discact = discact.reset_index(drop=True)

for i in range(0, len(discact)):
    print(discact['Name'][i])
    url = discact['Eng Release'][i]
    page = requests.get(url)
    with open("my_pdf.pdf", 'wb') as my_data:
        my_data.write(page.content)
    open_pdf_file = open("my_pdf.pdf", 'rb')
    read_pdf = PyPDF2.PdfFileReader(open_pdf_file)
    discact.at[i, 'EngText'] = read_pdf.getPage(0).extractText().strip()
    
discact.to_csv("Output Files/Actions.csv", index = None)

