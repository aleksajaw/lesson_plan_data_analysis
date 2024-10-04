import pandas as pd
from constants import *
from utils import *


baseUrl = getWithoutLastPart(planStartUrl)

listFrameLinks = findInFrame('a', {'target': 'plan'}, 'list', planStartUrl, True) or []

data = []

for link in listFrameLinks:
    
    table = findInFrame('table', {'class': 'tabela'}, 'plan', planStartUrl)

    for row in table.find_all('tr'):
        rowData = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if rowData:
            data.append(rowData)

# Convert the list of lists into a DataFrame
df = pd.DataFrame(data, columns=data[0])

# Export DataFrame to Excel
excelFile = 'schedule2.xlsx'
df.to_excel(excelFile, sheet_name='1A', index=False)