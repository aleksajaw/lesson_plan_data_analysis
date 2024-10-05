import pandas as pd
from constants import *
from utils import *
import os.path

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


excelFileName = 'schedule.xlsx'
engineName = 'openpyxl'

if not ( os.path.isfile(excelFileName) ):
  writer = pd.ExcelWriter(excelFileName, engine=engineName)
  empty_dataframe=pd.DataFrame()
  empty_dataframe.to_excel(writer, sheet_name='empty')
  writer.close()

else:

  try:  
    with pd.ExcelWriter(excelFileName, engine=engineName) as writer:
      df=pd.DataFrame([1,2,3,4])
      df.to_excel(writer, sheet_name='empty', index=False, header=False)

    '''for key in classesData:
      classData = classesData[key]
      print(key)
      print(classData)
      df = pd.DataFrame(classData)
      df.to_excel(writer, sheet_name=key[0], index=False)'''

  except Exception as e:
    print(f"Error reading the Excel file: {e}")