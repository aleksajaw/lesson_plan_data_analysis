from src.constants import planURL, driverLocationStates, timeIndexNames, scraperFindKeys, scraperPresenceLocators
from src.utils import splitHTMLAndRemoveTags, delInvalidChars
from src.utils.error_utils import getTraceback
from selenium import webdriver
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
    msgText=''
    noErrors = True
    
    try:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)

        driver.get(planURL)
        currDriverLocation = driverLocationStates[0]

        listFrame = driver.find_element(*scraperPresenceLocators['list'])
        planFrame = driver.find_element(*scraperPresenceLocators['plan'])

        driver.switch_to.frame(listFrame)
        currDriverLocation = driverLocationStates[1]
    
    except Exception as e:
        msgText = f'\nError while initializing webdriver and its elements for {planURL}: {getTraceback(e)}'
        noErrors = False

    if msgText: print(msgText)  

    return noErrors



def scrapeAndSetClassList():

    global driver, classList
    msgText=''
    noErrors = True
    
    try:
        classList = driver.find_elements(*scraperFindKeys['classList'])

    except Exception as e:
        msgText = f'\nError while scraping and setting the class list for the schedules for {planURL}: {getTraceback(e)}'
        noErrors = False

    if msgText: print(msgText)  
    
    return noErrors



def scrapeClassTables():
    
    global classList, wait, driver, currDriverLocation, driverLocationStates, classesData
    msgText=''
    noErrors = True

    try:
        colsNrReservedForRowMultiIndex = len(timeIndexNames)
        emptyCellDefaultCols = ['','','']

        for link in classList:
        # comment out above code and
        # uncomment one of the two option below to quicker check the scraper
        #for link in classList[:4]:
        #if(True):
        #    link=classList[1]

            if(currDriverLocation!=driverLocationStates[1]):
                wait.until(EC.presence_of_element_located(scraperPresenceLocators[driverLocationStates[1]]))
                driver.switch_to.frame(listFrame)
                currDriverLocation = driverLocationStates[1]

            link.click()
            schoolClassName = link.text

            driver.switch_to.default_content()
            currDriverLocation = driverLocationStates[0]

            wait.until( EC.presence_of_element_located(scraperPresenceLocators[driverLocationStates[2]]) )
            driver.switch_to.frame(planFrame)
            currDriverLocation = driverLocationStates[2]
            
            table = driver.find_element(*scraperFindKeys['table'])
            rows = table.find_elements(*scraperFindKeys['rows'])


            classRows = []


            # loop through rows
            currRowNr = 0

            for row in rows:
                
                cols = row.find_elements(*scraperFindKeys['cols'])


                currColNr = 0
                maxColInRowCounter = 0
                maxLinesInRowCounter = 0

                for cell in cols:

                    cellContent = [ cell.get_attribute('innerHTML')
                                    or   '' ]
                    
                    if '<br>' in cellContent[0]:
                        cellContent = cellContent[0].split('<br>')


                    linesInRowCounter = 0

                    for cellLine in cellContent:
                        
                        partsOfLine = splitHTMLAndRemoveTags(cellLine)

                        
                        colsInCellLineCounter = 0
                        currRowWithLinesTotalNr = currRowNr + linesInRowCounter

                        while currRowWithLinesTotalNr > (len(classRows)-1):
                            classRows.append([])
                        
                        currRow = classRows[currRowWithLinesTotalNr]


                        isItTimeIndexCol = len(partsOfLine)==1   and   currColNr <= colsNrReservedForRowMultiIndex

                        if len(partsOfLine) > 1   or   isItTimeIndexCol:

                            for partNr, part in enumerate(partsOfLine):
                                currColWithLinePartTotalNr = currColNr + partNr

                                while currColWithLinePartTotalNr > (len(currRow)-1):
                                    classRows[currRowWithLinesTotalNr].append('')                      

                                classRows[currRowWithLinesTotalNr][currColWithLinePartTotalNr] = part

                            colsInCellLineCounter += len(partsOfLine)


                        else:
                            classRows[currRowWithLinesTotalNr].extend(emptyCellDefaultCols)
                            colsInCellLineCounter += len(emptyCellDefaultCols)
                        

                        maxColInRowCounter = max(maxColInRowCounter, colsInCellLineCounter)
                        linesInRowCounter += 1


                    if linesInRowCounter > 1:
                        for lineNr in range( linesInRowCounter ):
                            
                            rowNrUnderCheck = currRowNr + lineNr
                            currRow = classRows[rowNrUnderCheck]
                            earlierRow = classRows[rowNrUnderCheck-1]
                            
                            for timeIndexColNr in range( len(timeIndexNames) ):
                                earlierTimeIndex = earlierRow[timeIndexColNr]

                                if not currRow[timeIndexColNr]:
                                    classRows[rowNrUnderCheck][timeIndexColNr] = earlierTimeIndex

                    
                    currColNr = currColNr + maxColInRowCounter

                    maxLinesInRowCounter = max(maxLinesInRowCounter, linesInRowCounter)
                
                currRowNr += maxLinesInRowCounter


            #print(classRows)
            classesData[delInvalidChars(schoolClassName)] = classRows

            driver.switch_to.parent_frame()
    

        driver.quit()

    except Exception as e:
        msgText = f'\nError while scrapping the schedules from {planURL}: {getTraceback(e)}'
        noErrors = False

    if msgText: print(msgText)     

    return noErrors



def scrapeSchoolWebPage():

    noErrors = True
    noErrors = initSchedulePageDriver()
    
    if noErrors:
        noErrors = scrapeAndSetClassList()

    if noErrors:
        noErrors = scrapeClassTables()



def getClassesDataFromSchoolWebPage():
    
    global classesData

    scrapeSchoolWebPage()

    return classesData