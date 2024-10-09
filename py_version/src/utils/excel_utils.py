import pandas as pd
from constants import outputsPath
from files_utils import doesFileExist
import json

engineName = 'openpyxl'
draftSheetName = 'draft_sheet'
scheduleExcelName = 'schedule.xlsx'

# FILE PATHS
scheduleExcelPath = outputsPath + scheduleExcelName
scheduleJSONPath = outputsPath + 'schedule.json'
scheduleDfsJSONPath = outputsPath + 'schedule_dfs.json'
scheduleExcelJSONPath = outputsPath + 'schedule_dfs_excel.json'


def doesSheetExist(workbook=pd.ExcelWriter.book, sheetName=''):
    return bool(sheetName in workbook.sheetnames and len(workbook.sheetnames)>0)


def createDraftSheet(excelFilePath=scheduleExcelPath):
    writer = pd.ExcelWriter(excelFilePath, engine=engineName)
    draftDf = pd.DataFrame()
    draftDf.to_excel(writer, sheet_name=draftSheetName, index=False)
    writer.close()


def createDraftSheetIfNecessary():
    if not doesFileExist(scheduleExcelPath):
        createDraftSheet()


def delDraftIfNecessary(workbook=pd.ExcelWriter.book):
    if ((len(workbook.sheetnames)>1) & doesSheetExist(workbook, draftSheetName)):
        deleteExcelSheet(workbook, draftSheetName)


def compareAndUpdateFile(filePath='',dataToCompare=''):
    if bool(filePath) and bool(dataToCompare):
        try:
            with open(filePath, "r+") as file:
                if not (file.read()==dataToCompare):
                    file.seek(0)
                    file.write(dataToCompare)
                    file.close()
                    print(f'{filePath} updated with new data.')

        except FileNotFoundError:
            with open(filePath, 'w') as file:
              file.write(dataToCompare)
              file.close()
              print(f'{filePath} updated with new data.')


def writingObjOfDfsToExcel(writer=pd.ExcelWriter, dataToEnter=None, isConverted = True):
    try:
        classDfs = convertToObjOfDfs(dataToEnter) if not isConverted else dataToEnter

        for className in classDfs:
            classDfs[className].to_excel(writer, sheet_name=className, index=False)

        print('Data loaded to the schedule Excel file.')

    except Exception as e:
        print(f'Error loading complete classes data: {e}')


def writingToExcelSheet(writer=pd.ExcelWriter, sheetName='', dataToEnter=None):
    try:
        df = convertToDf(dataToEnter)
        df.to_excel(writer, sheet_name=sheetName, index=False)
        print(f'Data for sheet {sheetName} loaded.')

    except Exception as e:
        print(f'Error loading data to {sheetName}: {e}')


def deleteExcelSheet(workbook=pd.ExcelWriter.book, sheetName=''):
    try:
        del workbook[sheetName]
        msgText = f'The sheet {sheetName} deleted.'

    except Exception as e:
        msgText = f'Error deleting the sheet {sheetName}: {e}'

    print(msgText)


def convertCurrExcelToDfsJSON():
    excelJSON = {}

    try:
        excelDfs = pd.read_excel(scheduleExcelPath, sheet_name=None)
        excelJSON = convertObjOfDfsToJSON(excelDfs)

    except Exception as e:
        print(f'Error converting existing schedule Excel file to JSON: {e}')

    return excelJSON 


# CONVERTERS #
def convertObjOfDfsToJSON(dataToConvert=None):
    objOfDfsJSON = {}

    for sheet_name, df in dataToConvert.items():
        objOfDfsJSON[sheet_name] = df.to_json(orient='records')

    return json.dumps(objOfDfsJSON, indent=4)


def convertToDf(dataToConvert=None):
    df = None

    if(dataToConvert):
        rows=dataToConvert[1:]
        cols=dataToConvert[0]
        df = pd.DataFrame(data=rows, columns=cols)

    return df


def convertToObjOfDfs(dataToConvert=None):
    if dataToConvert:
        return {sheet_name: convertToDf(dataToConvert[sheet_name]) for sheet_name in dataToConvert}

    else:
        return pd.DataFrame()