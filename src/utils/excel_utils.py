from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleExcelClassesPath
from src.constants.conversion_constants import excelEngineName, draftSheetName
from pandas import ExcelWriter, DataFrame
from openpyxl import load_workbook, Workbook
from openpyxl.cell.cell import MergedCell as openpyxlMergedCell



###   DRAFTS   ###
def createDraftSheet(excelFilePath=scheduleExcelClassesPath):
    msgTxt=''
    try:
        with ExcelWriter(excelFilePath, engine=excelEngineName, mode='w+') as writer:
            draftDf = DataFrame()  # Create an empty DataFrame
            draftDf.to_excel(writer, sheet_name=draftSheetName, merge_cells=True)

    except Exception as e:
        msgTxt = handleErrorMsg('\nError while creating draft sheet for Excel file.', getTraceback(e))

    if msgTxt: print(msgTxt)



def createDraftSheetIfNecessary(excelFilePath=scheduleExcelClassesPath):
    from files_utils import doesFileExist
    if not doesFileExist(excelFilePath):
        createDraftSheet()



def delDraftIfNecessary(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    from files_utils import doesFileExist
    msgTxt=''

    if not bool(workbook) and doesFileExist(excelFilePath):

        try:
            workbook = load_workbook(excelFilePath)

            if (len(workbook.sheetnames)>1) & doesSheetExist(workbook, draftSheetName):
                deleteExcelSheet(workbook, draftSheetName)
                workbook.save(excelFilePath)
          
            else:
                workbook.close()


        except Exception as e:
            msgTxt = handleErrorMsg('\nUnable to open the Excel file to check and delete the draft sheet.', getTraceback(e))
            return
    
    if msgTxt: print(msgTxt)
    


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
        msgText = handleErrorMsg(f'\nError deleting the sheet {sheetName}.', getTraceback(e))

    if msgText: print(msgText)



def get1stNotMergedCell(group=[]):
    foundNotMergedCell = False
    i = -1

    while not foundNotMergedCell:
        i+=1
        if not isinstance(group[i], openpyxlMergedCell):
            foundNotMergedCell = True

    return group[i] if i>=0 else None



def getNrOfLastNonEmptyCellInCol(ws=None, minRow=int, col=int):
    msgText=''
    counter = -1

    try:
        for row in ws.iter_rows(min_row=minRow, min_col=col, max_col=col):

            if row[0].value is not None:           
                if counter < 0:
                    counter = 0
                
                counter += 1
            
            else:
                break
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while getting the last non-empty cell in column.', getTraceback(e))
                    
    if msgText: print(msgText)

    return counter

                    
def removeLastEmptyRowsInDataFrames(elToBeFiltered=None):
    msgText = ''

    try:
        if not isinstance(elToBeFiltered, list):
            elToBeFiltered = list(elToBeFiltered)

        # keep all the rows up to the last non-empty row
        for singleWorksheet in elToBeFiltered:
            if len(singleWorksheet.items()):
                for sheetName, sheetVal in singleWorksheet.items():
                    lastNonEmptyRow = int(sheetVal.dropna(how='all').index[-1][0])
                    #lastNonEmptyRow = (int(lastNonEmptyRow[0]), lastNonEmptyRow[1])
                    singleWorksheet[sheetName] = sheetVal.loc[:lastNonEmptyRow]
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while removing last empty rows in Excel worksheet.', getTraceback(e))
    
    if msgText: print(msgText)

    #return elToBeFiltered



def dropnaInDfByAxis(el=None, axis=-1, both=True):
    msgText=''

    try:
        if isinstance(el, DataFrame):
            axisList = [axis   if (axis>=0 and not both)   else 0,1]
            for axis in axisList:
                el = el.dropna(axis=axis, how='all')

    except Exception as e:
        msgText = handleErrorMsg('\nError while dropping the NA values in the both axis of Data Frame.', getTraceback(e))

    if msgText: print(msgText)
 
    return el