from error_utils import handleErrorMsg, getTraceback
from src.constants.conversion_constants import excelEngineName
from pandas import ExcelWriter
import os
from converters_utils import convertToDf, convertToObjOfDfs, delInvalidChars, convertObjOfDfsToJSON
from excel_styles_utils import autoFormatScheduleExcel



def writeAsDfToExcelSheet(desire=None, sheetName='', dataToEnter=None):
    msgText = ''

    # desire should be Excel.Writer or filePath
    if not desire:
        from files_utils import createFileNameWithNr
        desire = createFileNameWithNr

    try:
        df = convertToDf(dataToEnter)
        df.to_excel(desire, sheet_name=sheetName, merge_cells=True)
        msgText = f'\nData for sheet {sheetName} loaded.'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError loading data into {sheetName}.', getTraceback(e))

    if msgText: print(msgText)



def writeObjOfDfsToExcel(writer=ExcelWriter, excelFilePath='', dataToEnter=None, isConverted=True):
    msgText = ''

    try:
        # group contains classes, teachers, subjects
        groupDfs = convertToObjOfDfs(dataToEnter)   if not isConverted   else dataToEnter

        for groupName in groupDfs:   
            groupDfs[groupName].to_excel(writer, sheet_name=delInvalidChars(groupName), merge_cells=True)

        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForWriteObjOfDfsToExcel(excelFilePath='', objOfDfs=None, doesNeedFormat=True):
    msgText=''

    try:
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
            writeObjOfDfsToExcel(writer, excelFilePath, objOfDfs)

            if doesNeedFormat:
                autoFormatScheduleExcel(writer.book, excelFilePath)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writeExcelWorksheetsWithMultipleDfs(writer=ExcelWriter, excelFilePath='', dataToEnter=None, isConverted=True, writingDirection='rows'):
    msgText = ''

    try:
        # group contains classes, teachers, subjects
        groupDfs = {el: convertToObjOfDfs(dataToEnter[el])   for el in dataToEnter}   if not isConverted   else dataToEnter
        
        for groupName in groupDfs:
            coords = { 'row': 0,
                       'col': 0 }

            for singleDf in groupDfs[groupName]:
                
                singleDf.to_excel( writer, sheet_name=delInvalidChars(groupName), merge_cells=True,
                                   startrow=coords['row'], startcol=coords['col'] )
                
                if writingDirection == 'rows':
                    coords['col'] = coords['col'] + singleDf.shape[1] + 3

                else:
                    coords['row'] = coords['row'] + singleDf.shape[0] + 4


        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForExcelWorksheetsWithMultipleDfs(excelFilePath='', objOfMultipleDfs=None, doesNeedFormat=True, writingDirection='rows'):
    msgText=''

    try:
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
            writeExcelWorksheetsWithMultipleDfs(writer, excelFilePath, objOfMultipleDfs, True, writingDirection)

            if doesNeedFormat:
                autoFormatScheduleExcel(writer.book, excelFilePath)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writeObjOfDfsToJSON(filePath='', objOfDfs=None):
    from files_utils import compareAndUpdateFile
    msgText = ''
    isFileChanged = False

    try:
        dataToEnter = convertObjOfDfsToJSON(objOfDfs)
        isFileChanged = compareAndUpdateFile(filePath, dataToEnter)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(filePath)}.', getTraceback(e))

    if msgText: print(msgText)

    return isFileChanged