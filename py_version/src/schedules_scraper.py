from constants import planURL, driverLocationStates
from utils import splitHTMLAndRemoveTags
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = None
wait = None
currDriverLocation = ''
listFrame = None
planFrame = None

classesData = {}
classList = []


def initSchedulePageDriver():
    
    global driver, wait, currDriverLocation, listFrame, planFrame
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    driver.get(planURL)
    currDriverLocation = driverLocationStates[0]

    listFrame = driver.find_element(By.NAME, 'list')
    planFrame = driver.find_element(By.NAME, 'plan')

    driver.switch_to.frame(listFrame)
    currDriverLocation = driverLocationStates[1]


def scrapeAndSetClassList():

    global driver, classList
    classList = driver.find_elements(By.CSS_SELECTOR, 'a[target="plan"]')


def scrapeClassTables():
    
    global classList, wait, driver, currDriverLocation, driverLocationStates, classesData

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

        classData = []

        rows = table.find_elements(By.TAG_NAME, 'tr')

        finalRows = []


        # loop through rows
        rowsCounter = 0
        
        for row in rows:
            cols = row.find_elements(By.XPATH, './/td | .//th')

            # loop through cells (columns) in rows
            colsCounter = 0
            maxRowCounter = 0
            maxColCounter = 0

            for cell in cols:
                cellContent = cell.get_attribute('innerHTML')

                # convert all to []
                if '<br>' in cellContent:
                    #cellContent = [cellContent.split('<br>')[0]]
                    cellContent = cellContent.split('<br>')

                else:
                    cellContent = [cellContent]

                while rowsCounter >= len(finalRows):
                    finalRows.append([])

                # loop through lines inside a single cell
                currColNr = colsCounter
                currRowNr = rowsCounter
                linesInRowCounter = 0

                for cellLine in cellContent:
                    partsOfLine = splitHTMLAndRemoveTags(cellLine)
                    colsInCellCounter = 0
                    rowNrWithExtraLines = currRowNr + linesInRowCounter

                    while rowNrWithExtraLines >= len(finalRows):
                        finalRows.append([])
                    
                    parentRow = finalRows[rowNrWithExtraLines]

                    if len(partsOfLine) > 0:

                        for part in partsOfLine:
                            x = currColNr + colsInCellCounter

                            while x >= len(parentRow):
                                finalRows[rowNrWithExtraLines].append('')                      

                            finalRows[rowNrWithExtraLines][x] = part
                            colsInCellCounter+=1

                    else:
                        finalRows[rowNrWithExtraLines].extend(['','',''])
                        colsInCellCounter+=3
                    
                    maxColCounter = max(maxColCounter,colsInCellCounter)
                    linesInRowCounter += 1


                if linesInRowCounter >1:

                    for i in range(linesInRowCounter):
                        checkingRowNr = currRowNr + i

                        for j in range(2):
                            if(finalRows[checkingRowNr][j]==''):
                                finalRows[checkingRowNr][j] = finalRows[checkingRowNr-1][j]

                maxRowCounter = max(maxRowCounter, linesInRowCounter)
                colsCounter = currColNr + maxColCounter


            rowsCounter+=maxRowCounter

        classData = finalRows
        #print(classData)
        classesData[className2.replace('/', ' ')] = classData

        driver.switch_to.parent_frame()



def scrapeSchoolWebPage():

    initSchedulePageDriver()
    scrapeAndSetClassList()
    scrapeClassTables()


def getClassesDataFromSchoolWebPage():
    
    global classesData

    scrapeSchoolWebPage()

    return classesData