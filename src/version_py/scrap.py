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
    classLink = link.get('href')
    classList.append(currClassName)

    print(currClassName,':', convertToFrameUrl(baseUrl, classLink))
    
    table = findInFrame('table', {'class': 'tabela'}, 'plan', planStartUrl)

    classData = []
    for row in table.find_all('tr'):
        rowData = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if rowData:
            classData.append(rowData)

    classesData[currClassName.replace('/', ' ')] = classData


excelFileName = 'schedule.xlsx'
engineName = 'openpyxl'
draftSheetName = 'draft_sheet'


if not ( os.path.isfile(excelFileName) ):
  writer = pd.ExcelWriter(excelFileName, engine=engineName)
  draftDf=pd.DataFrame()
  draftDf.to_excel(writer, sheet_name=draftSheetName, index=False)
  writer.close()


try:  
  with pd.ExcelWriter(excelFileName, mode='a', if_sheet_exists='replace', engine=engineName) as writer:

    workbook = writer.book
    
    for key in classesData:

      classData = classesData[key]
      msgStr = key+': '

      try:
        cols = classData[0]
        df = pd.DataFrame(classData[1:], columns=classData[0])
        df.to_excel(writer, sheet_name=key, index=False)
        print(f'{key}: data loaded.')

      except Exception as e:
        print(f'{key}: error occurred while loading data.')

    if (draftSheetName in workbook.sheetnames) & (len(workbook.sheetnames)):
      del workbook[draftSheetName]
      print('Draft sheet deleted.')


except Exception as e:
  print(f"Error reading the Excel file: {e}")