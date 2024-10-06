import pandas as pd
from constants import outputsPath
from files_utils import doesFileExist

engineName = 'openpyxl'
draftSheetName = 'draft_sheet'
scheduleExcelName = 'schedule.xlsx'
scheduleExcelPath = outputsPath + scheduleExcelName


def doesSheetExist(workbook=pd.ExcelWriter.book, sheetName=''):
    return bool((sheetName in workbook.sheetnames) & len(workbook.sheetnames))


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


def writingToExcel(writer=pd.ExcelWriter, sheetName='', dataToEnter=None):
    try:
        rows=dataToEnter[1:]
        cols=dataToEnter[0]
        df = pd.DataFrame(data=rows, columns=cols)
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