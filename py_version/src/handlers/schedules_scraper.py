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
        # To quickly check the scraping loop:
        # comment out the above code
        # and uncomment one of the two options below.
        #for link in classList[:4]:
        #for link in [classList[0]]:

            ###   SCRAPER   START   ###
            # Go to the list frame.
            if(currDriverLocation!=driverLocationStates[1]):
                wait.until(EC.presence_of_element_located(scraperPresenceLocators[driverLocationStates[1]]))
                driver.switch_to.frame(listFrame)
                currDriverLocation = driverLocationStates[1]

            link.click()
            schoolClassName = link.text

            driver.switch_to.default_content()
            currDriverLocation = driverLocationStates[0]

            # Go to the plan frame.
            wait.until( EC.presence_of_element_located(scraperPresenceLocators[driverLocationStates[2]]) )
            driver.switch_to.frame(planFrame)
            currDriverLocation = driverLocationStates[2]
            
            # Get main data.
            table = driver.find_element(*scraperFindKeys['table'])
            rows = table.find_elements(*scraperFindKeys['rows'])
            ###   SCRAPER   END   ###


            classRows = []


            # Counters for the loop below.
            currRowNr = 0

            # Loop through the rows in the table.
            for row in rows:
                
                cols = row.find_elements(*scraperFindKeys['cols'])


                # Counters for the loop below.
                currColNr = 0
                # Explanation for the counter below is on the line 190.
                maxColInRowCounter = 0
                # Explanation for the counter below is on the line 219.
                maxLinesInRowCounter = 0

                # Loop through cells (columns) in rows.
                for cell in cols:

                    # Get the cell content and split it into lines if necessary.
                    cellContent = [ cell.get_attribute('innerHTML')
                                    or   '' ]
                    
                    if '<br>' in cellContent[0]:
                        cellContent = cellContent[0].split('<br>')


                    # Counter for the loop below.
                    linesInRowCounter = 0

                    # Loop through lines inside a single cell.
                    for cellLine in cellContent:
                        
                        # For e.g., get '<span>subject name</span> <span>teacher name</span> <span>classroom number</span>'
                        # as ['subject name', 'teacher name', 'classroom number']
                        partsOfLine = splitHTMLAndRemoveTags(cellLine)
                        partsOfLineLength = len(partsOfLine)
                        
                        colsInCellLineCounter = 0
                        currRowWithLinesTotalNr = currRowNr + linesInRowCounter

                        # Initialize new rows in the classRows if necessary.
                        while currRowWithLinesTotalNr > (len(classRows)-1):
                            classRows.append([])
                        
                        currRow = classRows[currRowWithLinesTotalNr]


                        # If:
                        # 1)  the line has more than 1 element.
                        #       - This property is reserved for the time indcises.
                        #       - This condition also could mean that the line is not empty
                        #         ([''] has length = 1);
                        # or
                        # 2)  the line has exactly 1 element,
                        #       but it is one of the time index columns;
                        isItTimeIndexCol = partsOfLineLength==1   and   currColNr < colsNrReservedForRowMultiIndex

                        if partsOfLineLength > 1   or   isItTimeIndexCol:

                            currColWithLineColsTotalNr = currColNr + partsOfLineLength

                            # initialize missing columns in the current row if necessary;
                            while currColWithLineColsTotalNr > len(currRow):
                                classRows[currRowWithLinesTotalNr].append('')

                            # write the parts of the line;
                            for partNr, part in enumerate(partsOfLine):
                                currColWithLinePartColNr = currColNr + partNr

                                # then update the value of that column   &   inner column counter.
                                classRows[currRowWithLinesTotalNr][currColWithLinePartColNr] = part

                            colsInCellLineCounter += partsOfLineLength


                        else:
                            # Add an empty cell.
                            classRows[currRowWithLinesTotalNr].extend(emptyCellDefaultCols)
                            colsInCellLineCounter += len(emptyCellDefaultCols)
                        

                        # This variable is used to find the maximum number of inner columns in the row's cells,
                        # update the currentColNr with that value,
                        # and avoid overwriting values in cells with multiple inner columns.
                        maxColInRowCounter = max(maxColInRowCounter, colsInCellLineCounter)
                        linesInRowCounter += 1


                    # Add missing columns for time indices
                    # to rows with more than 1 line. This means that
                    # the lessons in those rows occur at the same time.
                    if linesInRowCounter > 1:
                        for lineNr in range( linesInRowCounter ):
                            
                            rowNrUnderCheck = currRowNr + lineNr
                            currRow = classRows[rowNrUnderCheck]
                            earlierRow = classRows[rowNrUnderCheck-1]
                            
                            # The time index columns are at the beginning of each row,
                            # so we iterate using the length of timeIndexNames.
                            for timeIndexColNr in range( len(timeIndexNames) ):
                                earlierTimeIndex = earlierRow[timeIndexColNr]

                                # The time index column should be equal to '' or proper value.
                                if not currRow[timeIndexColNr]:
                                    classRows[rowNrUnderCheck][timeIndexColNr] = earlierTimeIndex

                    
                    # Update the current column number with the number of the columns from the previous cell in the row.
                    currColNr = currColNr + maxColInRowCounter

                    # This variable is used to find the maximum number of lines in the row's cells,
                    # update the currentRowNr with that value,
                    # and avoid overwriting values in rows with multiple lines.
                    maxLinesInRowCounter = max(maxLinesInRowCounter, linesInRowCounter)
                
                # Update the current row number with the number of the lines from the previous row.
                currRowNr += maxLinesInRowCounter


            #print(classRows)
            classesData[delInvalidChars(schoolClassName)] = classRows

            driver.switch_to.parent_frame()
    

        # IMPORTANT: This line prevents memory leaks.
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