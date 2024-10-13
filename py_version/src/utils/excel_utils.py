from constants import scheduleExcelPath, excelEngineName, draftSheetName, dfColNamesTuples, timeIndexes
from files_utils import doesFileExist
import json
import re
from pandas import ExcelWriter, DataFrame, read_excel, MultiIndex
from openpyxl.cell import cell as openpyxl_cell



###   DRAFTS   ###
def createDraftSheet(excelFilePath=scheduleExcelPath):
    writer = ExcelWriter(excelFilePath, engine=excelEngineName)
    draftDf = DataFrame()
    draftDf.to_excel(writer, sheet_name=draftSheetName)
    writer.close()



def createDraftSheetIfNecessary():
    if not doesFileExist(scheduleExcelPath):
        createDraftSheet()



def delDraftIfNecessary(workbook=ExcelWriter.book):
    if ((len(workbook.sheetnames)>1) & doesSheetExist(workbook, draftSheetName)):
        deleteExcelSheet(workbook, draftSheetName)



###   SHEET OPERATIONS   ###
def doesSheetExist(workbook=ExcelWriter.book, sheetName=''):
    return bool(sheetName in workbook.sheetnames and len(workbook.sheetnames)>0)



def deleteExcelSheet(workbook=ExcelWriter.book, sheetName=''):
    msgText = ''

    try:
        del workbook[sheetName]
        msgText = f'The sheet {sheetName} deleted.'

    except Exception as e:
        msgText = f'Error deleting the sheet {sheetName}: {e}'

    print(msgText)



def writeToExcelSheet(writer=ExcelWriter, sheetName='', dataToEnter=None):
    msgText = ''

    try:
        df = convertToDf(dataToEnter)
        df.to_excel(writer, sheet_name=sheetName)
        msgText = f'Data for sheet {sheetName} loaded.'

    except Exception as e:
        msgText = f'Error loading data to {sheetName}: {e}'

    print(msgText)



def writeObjOfDfsToExcel(writer=ExcelWriter, dataToEnter=None, isConverted = True):
    msgText = ''

    try:
        classDfs = convertToObjOfDfs(dataToEnter) if not isConverted else dataToEnter

        for className in classDfs:
            classDfs[className].to_excel(writer, sheet_name=className)

        msgText = 'Data loaded to the schedule Excel file.'

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

        # set actual columns as row indexes
        df.set_index(keys=timeIndexes, inplace=True)

    return df



# DATA   =>   OBJECT OF DATA FRAMES 
def convertToObjOfDfs(dataToConvert=None):
    if dataToConvert:
        return {sheet_name: convertToDf(dataToConvert[sheet_name]) for sheet_name in dataToConvert}

    else:
        return {draftSheetName: DataFrame()}



# OBJECT OF DATA FRAMES   =>   JSON
def convertObjOfDfsToJSON(dataToConvert=None):
    objOfDfsJSON = {}

    for sheet_name, df in dataToConvert.items():
        objOfDfsJSON[sheet_name] = df.to_json(orient='split')

    return json.dumps(objOfDfsJSON, indent=4)



# EXCEL CONTENT   =>   OBJECT OF DATA FRAMES
#                    =>   JSON
def convertCurrExcelToDfsJSON():
    excelJSON = {}
    msgText = ''

    try:
        excelDfs = read_excel(scheduleExcelPath, sheet_name=None)
        excelJSON = convertObjOfDfsToJSON(excelDfs)

    except Exception as e:
        msgText = f'Error converting existing schedule Excel file to JSON: {e}'

    print(msgText)

    return excelJSON 



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