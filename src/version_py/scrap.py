import pandas as pd
from constants import *
from utils import *
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driverLocationStates = ['default', 'list', 'plan']

driver.get(planStartUrl)
currDriverLocation = driverLocationStates[0]

listFrame = driver.find_element(By.NAME, 'list')
planFrame = driver.find_element(By.NAME, 'plan')

driver.switch_to.frame(listFrame)
currDriverLocation = driverLocationStates[1]

classList = driver.find_elements(By.CSS_SELECTOR, 'a[target="plan"]')
classesData = {}

for link in classList:

    if(currDriverLocation!='list'):
      wait.until(EC.presence_of_element_located((By.NAME, 'list')))
      driver.switch_to.frame(listFrame)
    currDriverLocation = driverLocationStates[1]

    link.click()
    className2 = link.text

    driver.switch_to.default_content()
    currDriverLocation = driverLocationStates[0]

    wait.until(EC.presence_of_element_located((By.NAME, 'plan')))
    driver.switch_to.frame(planFrame)
    currDriverLocation = driverLocationStates[2]
    
    table = driver.find_element(By.CLASS_NAME, 'tabela')

    #print(table.get_attribute("outerHTML"))
    classData = []
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cols = row.find_elements(By.XPATH, './/td | .//th')
        rowData = []
        for col in cols:
           rowData.append(col.text)
        if rowData:
            classData.append(rowData)

    classesData[className2.replace('/', ' ')] = classData

    driver.switch_to.parent_frame()


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