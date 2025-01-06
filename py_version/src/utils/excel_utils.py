from constants import scheduleExcelPath, excelEngineName, draftSheetName, dfColNamesTuples, timeIndexes
import json
import re
from pandas import ExcelWriter, DataFrame, read_excel, MultiIndex, RangeIndex
from openpyxl import Workbook, load_workbook
from openpyxl.cell import cell as openpyxl_cell



###   DRAFTS   ###
def createDraftSheet(excelFilePath=scheduleExcelPath):
    try:
        with ExcelWriter(excelFilePath, engine=excelEngineName, mode='w+') as writer:
            draftDf = DataFrame()  # Create an empty DataFrame
            draftDf.to_excel(writer, sheet_name=draftSheetName, merge_cells=True)

    except Exception as e:
        print(f'Error while creating draft sheet for Excel file: {e}')



def createDraftSheetIfNecessary(excelPath=scheduleExcelPath):
    from files_utils import doesFileExist
    if not doesFileExist(excelPath):
        createDraftSheet()



def delDraftIfNecessary(workbook=Workbook(), excelFilePath=scheduleExcelPath):
    from files_utils import doesFileExist

    if not bool(workbook) and doesFileExist(excelFilePath):

        try:
            workbook = load_workbook(excelFilePath)

            if (len(workbook.sheetnames)>1) & doesSheetExist(workbook, draftSheetName):
                deleteExcelSheet(workbook, draftSheetName)
                workbook.save(excelFilePath)
          
            else:
                workbook.close()


        except Exception as e:
            print(f"Unable to open the Excel file to check and delete the draft sheet: {e}")
            return

    


###   SHEET OPERATIONS   ###
def doesSheetExist(workbook=Workbook(), sheetName=''):
    return bool(sheetName in workbook.sheetnames and len(workbook.sheetnames)>0)



def deleteExcelSheet(workbook=Workbook(), sheetName=''):
    msgText = ''

    try:
        if isinstance(workbook, Workbook):
            worksheet = workbook[sheetName]
            workbook.remove(worksheet)
            msgText = f'The sheet {sheetName} deleted.'

        else:
          raise Exception(f'workbook variable should be Workbook() type, not {type(workbook)}')
        
    except Exception as e:
        msgText = f'Error deleting the sheet {sheetName}: {e}'

    print(msgText)



def writeAsDfToExcelSheet(desire=None, sheetName='', dataToEnter=None):
    msgText = ''

    # desire should be Excel.Writer or filePath
    if not desire:
        from files_utils import createFileName
        desire = createFileName

    try:
        df = convertToDf(dataToEnter)
        df.to_excel(desire, sheet_name=sheetName, merge_cells=True)
        msgText = f'Data for sheet {sheetName} loaded.'

    except Exception as e:
        msgText = f'Error loading data to {sheetName}: {e}'

    print(msgText)



def createGroupsInListByPrefix(data=[], splitDelimeter = '-', replaceDelimeter = '.r'):
    # only leave the part before the first '-' and cut '.r' out
    groupList = [ (str(item).split(splitDelimeter)[0]).replace(replaceDelimeter,'')
                        if isinstance(item, str)
                        else item
                      for item in data ]
    
    # group elements by names starting with the same prefix
    for i in range(2, len(groupList)):
        gList = groupList
        if ( all( isinstance(x, str)   for x in [gList[i-1], gList[i]] )
              and  gList[i].startswith(gList[i-1]) ):
            
            groupList[i] = gList[i-1]
    
    return groupList



def createGroupsInListByFirstLetter(data=[]):
    return [item[0]   for item in data]



def createGroupsInListByNumbers(data=[]):
    processed = []
    for item in data:
        itemStr = str(item)
        itemLen = len(itemStr)
        
        if any(c.isalpha()   for c in itemStr):
            item = ''.join([c   for c in itemStr if c.isalpha()])

        elif itemStr.isdigit():
            if itemLen > 1:
                item = itemStr[0] + (itemLen-1) * '0'
          
            elif 0 < int(item) < 10:
                item = 1
            
            item = int(item)
        
        else:
            # match e.g. '.9', '_09', '09' or '9'
            match = re.match(r'([^a-zA-Z0-9]*0*[^a-zA-Z0-9]*)\d+', itemStr)
            if match:# '.', '_0', '0'
                item = match.group(1)
        
        processed.append(item)
    
    return processed



def writeToExcelSheets(desire=None, dataToEnter=None):
    msgText = ''

    # desire should be Excel.Writer or filePath
    if not desire:
        from files_utils import createFileName
        desire = createFileName

    try:
        for key in dataToEnter.keys():
            try:
              # sort by numbers (which are keys here) inside list elements,
              # especially for classroom names like _08, s1, 1, 100
              # moreover, it prevents missorting like 1, 10, 100, 2, 20, 200 :)
              #dataToEnter[key].sort( key = lambda x: int( re.findall(r'\d+', x)[0] ) )

              # also add sorting strings between the values with numbers like: 1, s1, st1, 2, _02, s2
              # so we will have s1, s2, st1, 1, 2, _02
              dataToEnter[key].sort(  key=lambda x: (
                                        # True values are treated as smaller,
                                        # so they will appear earlier in the sorted list
                                        # so at first sort by letters
                                        not x[0].isalpha(),
                                        x.lower() if isinstance(x, str) and x[0].isalpha()
                                                  # sort by first digit in elements
                                                  else  int( re.findall( r'\d+', x )[0] )
                                                        if re.findall( r'\d+', x )
                                                        # if element does not have digit,
                                                        # use inf(inity) to move element
                                                        # at the end of the sorting here
                                                        else float('inf')
                                      )
                                    )
              # convert strings to integer, if it is possible
              dataToEnter[key] = [int(x)   if x.isdigit()   else x   for x in dataToEnter[key]]
            
            except:
                next
        
        with ExcelWriter(desire, mode='w+', engine=excelEngineName) as writer:
            objOfDfs = { sheetName: DataFrame({'names':dataToEnter[sheetName]})
                                    for sheetName in sorted(dataToEnter.keys()) }

            for listName in objOfDfs:
                df = objOfDfs[listName]
                # create index without '0' for better looking :)
                df.index = RangeIndex(start=1, stop=len(df)+1, step=1)
                df.to_excel(writer, sheet_name=listName)
        

        msgText = f'Data for {desire} loaded.'

    except Exception as e:
        msgText = f'Error loading data to {desire}: {e}'

    print(msgText)



def delInvalidChars(name='', target='sheetName'):
    if target=='sheetName':
        invalidScheetNameChars = ['/', '\\', ':', '*', '?', '[', ']']
        # replace invalid characters with character '_'
        return ''.join('_'  if c in invalidScheetNameChars   else c   for c in name)
    else:
        return name



def writeObjOfDfsToExcel(writer=ExcelWriter, dataToEnter=None, isConverted=True):
    msgText = ''

    try:
        # group contains classes, teachers, subjects
        groupDfs = convertToObjOfDfs(dataToEnter)   if not isConverted   else dataToEnter

        for groupName in groupDfs:   
            groupDfs[groupName].to_excel(writer, sheet_name=delInvalidChars(groupName), merge_cells=True)

        msgText = 'Data loaded to the main schedule Excel file.'

    except Exception as e:
        msgText = f'Error loading complete classes data: {e}'
    
    print(msgText)



###    CONVERTERS    ###


# DATA   =>   DATA FRAME
def convertToDf(dataToConvert=None):
    df = None

    if(dataToConvert):

        # multi-dimensional column names
        lessonColumns = MultiIndex.from_tuples(tuples = dfColNamesTuples)

        # old columns version
        #lessonColumns = dataToConvert[0]

        # schedule without column names
        lessonRows = dataToConvert[1:]

        df = DataFrame(data=lessonRows, columns=lessonColumns)

        # use empty string instead of null/NaN
        df = df.fillna('')
        
        # Restore 111 from '111.0'.
        # The problem is probably caused by the creation of the DataFrame.
        df = df.map(convertFloatToInt)

        # Useful if there are repeated index cells in the table,
        # e.g. when there are more than one lesson
        # at the same time for one class and its groups.

        # FOR NOW, LEAVE THIS AS A COMMENT
        # IF YOU WANT TO KEEP CREATING THE TEACHERS' TIMETABLE FUNCTIONAL.
        #for indexName in timeIndexes:
        #    df[indexName] = df[indexName].where(df[indexName] != df[indexName].shift(), '')
        
        # set actual columns as row indexes
        df.set_index(keys=timeIndexes, inplace=True)
        
    return df



# DATA   =>   OBJECT OF DATA FRAMES 
def convertToObjOfDfs(dataToConvert=None):
    if dataToConvert:
        return {sheetName: convertToDf(dataToConvert[sheetName])   for sheetName in dataToConvert}

    else:
        return {draftSheetName: DataFrame()}



# OBJECT OF DATA FRAMES   =>   JSON
def convertObjOfDfsToJSON(dataToConvert=None):
    objOfDfsJSON = {}

    try:
        for sheetName, df in dataToConvert.items():
            objOfDfsJSON[sheetName] = df.to_json(orient='split')

        objOfDfsJSON = json.dumps(objOfDfsJSON, indent=4)

    except Exception as e:
        print('Error while converting object of DataFrames to JSON: ',{e})

    return objOfDfsJSON



# EXCEL CONTENT   =>   OBJECT OF DATA FRAMES
#                    =>   JSON
def convertCurrExcelToDfsJSON():
    from files_utils import doesFileExist
    excelJSON = {}
    msgText = ''

    if not doesFileExist(scheduleExcelPath):
        return excelJSON

    try:
        excelData = read_excel(io=scheduleExcelPath, sheet_name=None, engine=excelEngineName,
                                keep_default_na=False)

        if(bool(excelData)):

            # old columns version
            #lessonColumns = dataToConvert[0]

            for sheetName, oldDf in excelData.items():
            
                if not oldDf.empty:
                    df = DataFrame(oldDf[2:])

                    # multi-dimensional column names
                    df.columns = MultiIndex.from_tuples(tuples = dfColNamesTuples)

                    # useful if there are repeated index cells in the table
                    # e.g. when there are more than one lesson
                    # at the same time for one class and its groups
                    for indexName in timeIndexes:
                        df[indexName] = df[indexName].where(df[indexName] != df[indexName].shift(), '')
                    
                    df.set_index(keys=timeIndexes, inplace=True)
                
                else:
                    df = oldDf
                excelData[sheetName] = df.to_json(orient='split')

        excelJSON = json.dumps(excelData, indent=4)


    except Exception as e:
        msgText = f'Error converting existing schedule Excel file to JSON: {e}'

    print(msgText)


    return excelJSON 



# 111.0   =>   111
def convertFloatToInt(value=None):
    isValueFloat = isinstance(value, float) and value.is_integer()
    if isValueFloat:
        return int(value)
    return value


# '1'   =>   1
def convertDigitInStrToInt(text=''):
    return int(text)  if str.isdigit(text)  else text


# <br>
# <br />   =>   \n
def convertBrInText(text=''):
    if isinstance(text, str):
        text = text.replace("<br>", "\n").replace("<br />", "\n")

    return text



# <p>
#   <span>hello</span> <span>world!&nbsp;</span>
# </p>
#   =>   helloworld!
def splitHTMLAndRemoveTags(HTMLText=''):
    HTMLTextStripped = re.sub(r'&nbsp;|\s+', '', HTMLText)
    tagParts = re.split(r'(<[^>]+>)', HTMLTextStripped)
    textParts = []

    for part in tagParts:
        if part and not part.startswith('<'):
            textParts.append( convertDigitInStrToInt(part) )

    return textParts



def get1stNotMergedCell(group=[]):
    foundNotMergedCell = False
    i = -1

    while not foundNotMergedCell:
        i+=1
        if not isinstance(group[i], openpyxl_cell.MergedCell):
            foundNotMergedCell = True

    return group[i] if i>=0 else None