#from src.constants.scraper_constants import planURL, driverLocationStates, scraperFindKeys, scraperPresenceLocators
from src.constants.scraper_constants import driverLocationStates, scraperFindKeys
from src.constants.schedule_structures_constants import timeIndexNames, noGroupMarker
from src.utils.converters_utils import splitHTMLAndRemoveTags, delInvalidChars, convertObjKeysToDesiredOrder
from src.utils.error_utils import handleErrorMsg, getTraceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = None
wait = None
currDriverLocation = ''
listFrame = None
planFrame = None

classesData = {}
classList = []


def initSchedulePageDriver(schoolWebInfo):
    
    global driver, wait, currDriverLocation, listFrame, planFrame
    msgText=''
    noErrors = True
    
    try:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        driver.set_window_size(1920, 1080)

        driver.get(schoolWebInfo['planURL']['full'])
        
        if schoolWebInfo['useDOMFrames']:
            currDriverLocation = driverLocationStates[0]

            listFrame = driver.find_element(*schoolWebInfo['scheduleLinksInfo']['selectorParent'])
            planFrame = driver.find_element(*schoolWebInfo['planInfo']['selector'])

            driver.switch_to.frame(listFrame)
            currDriverLocation = driverLocationStates[1]
    
    except Exception as e:
        noErrors = False
        msgText = handleErrorMsg(f'\nError while initializing Web Driver and its elements for {schoolWebInfo['schoolURL']}.', getTraceback(e))

    if msgText: print(msgText)  

    return noErrors



def scrapeAndSetClassList(schoolWebInfo):

    global driver, classList
    msgText=''
    noErrors = True
    
    try:
        classList = driver.find_elements(*schoolWebInfo['scheduleLinksInfo']['selector'])

    except Exception as e:
        noErrors = False
        msgText = handleErrorMsg(f'\nError while scraping and setting the class list for the schedules for {schoolWebInfo['schoolURL']}.', getTraceback(e))

    if msgText: print(msgText)
    
    return noErrors



def scrapeClassTables(schoolWebInfo):
    
    global classList, wait, driver, currDriverLocation, classesData
    msgText=''
    noErrors = True

    try:
        colsNrReservedForRowMultiIndex = len(timeIndexNames)
        emptyCellDefaultCols = []

        for linkNr in range(len(classList)):
            
            if not schoolWebInfo['useDOMFrames']:
                # Wait for the body to be ready.
                wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            ###   SCRAPER   START   ###
            link = classList[linkNr]

            # Go to the list frame.
            if( schoolWebInfo['useDOMFrames']   and   currDriverLocation!=driverLocationStates[1] ):
                wait.until( EC.visibility_of_element_located(schoolWebInfo['scheduleLinksInfo']['selectorParent']))
                driver.switch_to.frame(listFrame)
                currDriverLocation = driverLocationStates[1]
            
            elif not schoolWebInfo['useDOMFrames']:
                href = link.get_attribute('href')

                # Use only links that lead to the concrete schedules, not the main page for the schedules - skip them.
                if len(href) <= len(schoolWebInfo['planURL']['full']):
                    continue
            
                #wait.until( EC.visibility_of_element_located( (By.XPATH, '//a[@href="' + href + '""]') ) )

            try:
                link.click()

            except:
                if not schoolWebInfo['useDOMFrames']:
                    # Scroll the page to the footer to see the desired link to click.
                    footerEl = driver.find_element(By.XPATH, "//footer")
                    driver.execute_script("arguments[0].scrollIntoView(true);", footerEl)
                    
                    time.sleep(1.5)
                link.click()
            

            if not schoolWebInfo['useDOMFrames']:
                # Update the list of links to click after the page reloads.
                classList = driver.find_elements(*schoolWebInfo['scheduleLinksInfo']['selector'])
                link = classList[linkNr]

            schoolClassName = link.text

            if schoolWebInfo['useDOMFrames']:
                driver.switch_to.default_content()
                currDriverLocation = driverLocationStates[0]

                # Go to the plan frame.
                wait.until( EC.visibility_of_element_located(schoolWebInfo['planInfo']['selector']) )

                driver.switch_to.frame(planFrame)
                currDriverLocation = driverLocationStates[2]
            
            # Get main data.
            table = driver.find_element(*scraperFindKeys['table'])
            rows = table.find_elements(*scraperFindKeys['rows'])
            ###   SCRAPER   END   ###


            classRows = []


            # Counters for the loop below.
            currRowNr = 0

            # Find the default column number   and   assign correct value to the empty cell variable.
            if not len(emptyCellDefaultCols):
                exampleLessonCell = table.find_elements(By.XPATH, ".//td[.//span]")[colsNrReservedForRowMultiIndex + 1]
                exampleLessonElList = exampleLessonCell.find_elements(By.XPATH, ".//span[not(descendant::span)]")
                lessonElListLen = len(exampleLessonElList)
                emptyCellDefaultCols = [''] * ( 4   if lessonElListLen % 3 == 0   else
                                                3   if lessonElListLen % 2 == 0   else 0 )


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
                        
                        if partsOfLineLength > 1:
                            # get separate column for lesson group
                            elWithGroup = list(part   for part in partsOfLine[0].rpartition('-')   if part)
                            if len(elWithGroup)>1:
                                partsOfLine[0] = elWithGroup[0]
                                groupPart = elWithGroup[2]
                            else:
                                # subject without division into the groups
                                groupPart = noGroupMarker
                            partsOfLine.insert(1, groupPart)
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

                                if isinstance(part, str)   and   currColNr <= colsNrReservedForRowMultiIndex:
                                    part = part.replace(' ', '')

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

                    # Keep the correct column number, even if there are no values in the cells.
                    if not len(cellContent):
                        # Add an empty cell.
                        classRows[currRowWithLinesTotalNr].extend(emptyCellDefaultCols)
                        colsInCellLineCounter += len(emptyCellDefaultCols)
                        

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

            if schoolWebInfo['useDOMFrames']:
                driver.switch_to.parent_frame()
    
        classesData = convertObjKeysToDesiredOrder(classesData, sorted(classesData.keys()))

        # IMPORTANT: This line prevents memory leaks.
        driver.quit()

    except Exception as e:
        driver.quit()
        noErrors = False
        msgText = handleErrorMsg(f'\nError while scrapping the schedules from {schoolWebInfo['schoolURL']}.', getTraceback(e))

    if msgText: print(msgText)     

    return noErrors



def scrapeSchoolWebPage(schoolWebInfo):

    noErrors = initSchedulePageDriver(schoolWebInfo)
    
    if noErrors:
        noErrors = scrapeAndSetClassList(schoolWebInfo)

    if noErrors:
        noErrors = scrapeClassTables(schoolWebInfo)



def getClassesDataFromSchoolWebPage(schoolWebInfo):
    
    global classesData

    scrapeSchoolWebPage(schoolWebInfo)

    return classesData