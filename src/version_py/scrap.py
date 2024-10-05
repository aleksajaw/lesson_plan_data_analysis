import pandas as pd
from constants import *
from utils import *


baseUrl = getWithoutLastPart(planStartUrl)

listFrameLinks = findInFrame('a', {'target': 'plan'}, 'list', planStartUrl, True) or []

classesData = {}
classList = []

for link in listFrameLinks:
    
    currClassName = link.get_text(strip=True)
    classList.append(currClassName)

    print(currClassName,':', convertToFrameUrl(baseUrl, link.get('href')))
    
    table = findInFrame('table', {'class': 'tabela'}, 'plan', planStartUrl)

    classData = []
    for row in table.find_all('tr'):
        rowData = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if rowData:
            classData.append(rowData)

    classesData[currClassName.replace('/', ' ')] = classData


# Convert the list of lists into a DataFrame
#df = pd.DataFrame(classesData, columns=classesData[0])

# Export DataFrame to Excel
#excelFile = 'schedule2.xlsx'
#df.to_excel(excelFile, sheet_name='1A', index=False)