from constants import scheduleExcelPath, excelEngineName, draftSheetName, dfColNamesTuples, timeIndexes
from files_utils import doesFileExist
import json
import re
from pandas import ExcelWriter, DataFrame, read_excel, MultiIndex
from openpyxl.cell import cell as openpyxl_cell


def doesSheetExist(workbook=ExcelWriter.book, sheetName=''):
    return bool(sheetName in workbook.sheetnames and len(workbook.sheetnames)>0)


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


def writeObjOfDfsToExcel(writer=ExcelWriter, dataToEnter=None, isConverted = True):
    try:
        classDfs = convertToObjOfDfs(dataToEnter) if not isConverted else dataToEnter

        for className in classDfs:
            classDfs[className].to_excel(writer, sheet_name=className)

        print('Data loaded to the schedule Excel file.')

    except Exception as e:
        print(f'Error loading complete classes data: {e}')


def writeToExcelSheet(writer=ExcelWriter, sheetName='', dataToEnter=None):
    try:
        df = convertToDf(dataToEnter)
        df.to_excel(writer, sheet_name=sheetName)
        print(f'Data for sheet {sheetName} loaded.')

    except Exception as e:
        print(f'Error loading data to {sheetName}: {e}')


def deleteExcelSheet(workbook=ExcelWriter.book, sheetName=''):
    try:
        del workbook[sheetName]
        msgText = f'The sheet {sheetName} deleted.'

    except Exception as e:
        msgText = f'Error deleting the sheet {sheetName}: {e}'

    print(msgText)


def convertCurrExcelToDfsJSON():
    excelJSON = {}

    try:
        excelDfs = read_excel(scheduleExcelPath, sheet_name=None)
        excelJSON = convertObjOfDfsToJSON(excelDfs)

    except Exception as e:
        print(f'Error converting existing schedule Excel file to JSON: {e}')

    return excelJSON 


# CONVERTERS #
def convertObjOfDfsToJSON(dataToConvert=None):
    objOfDfsJSON = {}

    for sheet_name, df in dataToConvert.items():
        objOfDfsJSON[sheet_name] = df.to_json(orient='split')

    return json.dumps(objOfDfsJSON, indent=4)


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


def convertToObjOfDfs(dataToConvert=None):
    if dataToConvert:
        return {sheet_name: convertToDf(dataToConvert[sheet_name]) for sheet_name in dataToConvert}

    else:
        return DataFrame()


def convertDigitInStrToInt(text=''):
    return int(text) if str.isdigit(text) else text


def convertBrInText(text=''):
    if isinstance(text, str):
        if '<br>' in text:
            text.replace("<br>", "\n")

        elif '<br />' in text:
            text.replace("<br />", "\n")

    return text


def splitHTMLAndRemoveTags(HTMLText=''):
    HTMLText = re.sub(r'&nbsp;|\s+', '', HTMLText)
    parts = re.split(r'(<[^>]+>)', HTMLText)
    textParts = []

    for part in parts:
        if part and not part.startswith('<'):
            textParts.append(convertDigitInStrToInt(part))

    return textParts


def get1stNotMergedCell(group=[]):
    foundNotMergedCell = False
    i = -1

    while not foundNotMergedCell:
        i+=1
        if not isinstance(group[i], openpyxl_cell.MergedCell):
            foundNotMergedCell = True

    return group[i] if i>=0 else None