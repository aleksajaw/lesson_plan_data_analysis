from constants import planURL, scheduleExcelPath, excelEngineName, scheduleExcelJSONPath, scheduleDfsJSONPath, scheduleJSONPath
from utils import convertToObjOfDfs, convertObjOfDfsToJSON, createDraftSheetIfNecessary, convertCurrExcelToDfsJSON, writingObjOfDfsToExcel, delDraftIfNecessary, compareAndUpdateFile
import json
from pandas import ExcelWriter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


classesData = {}


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driverLocationStates = ['default', 'list', 'plan']

driver.get(planURL)
currDriverLocation = driverLocationStates[0]

listFrame = driver.find_element(By.NAME, 'list')
planFrame = driver.find_element(By.NAME, 'plan')

driver.switch_to.frame(listFrame)
currDriverLocation = driverLocationStates[1]

classList = driver.find_elements(By.CSS_SELECTOR, 'a[target="plan"]')


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
            colContent = int(col.text) if str.isdigit(col.text) else col.text
            rowData.append(colContent)
        if rowData:
            classData.append(rowData)

    classesData[className2.replace('/', ' ')] = classData

    driver.switch_to.parent_frame()


classesDataJSON = json.dumps(classesData, indent=4)
classesDataDfs = convertToObjOfDfs(classesData)
classesDataDfsJSON = convertObjOfDfsToJSON(classesDataDfs)


createDraftSheetIfNecessary()


try:

    with ExcelWriter(scheduleExcelPath, mode='a', if_sheet_exists='replace', engine=excelEngineName) as writer:

        workbook = writer.book
        currExcelAsJSON = convertCurrExcelToDfsJSON()

        try:
            if not (currExcelAsJSON == classesDataDfsJSON):
                writingObjOfDfsToExcel(writer, classesDataDfs)
                
            else:
                print('Nothing to be updated in Excel file.')

            delDraftIfNecessary(workbook)

            compareAndUpdateFile(scheduleExcelJSONPath, currExcelAsJSON)
            compareAndUpdateFile(scheduleDfsJSONPath, classesDataDfsJSON)
            compareAndUpdateFile(scheduleJSONPath, classesDataJSON)

        except Exception as e: 
            print(f"Error writing data to the Excel file: {e}")

except Exception as e:
    print(f"Error reading the Excel file: {e}")