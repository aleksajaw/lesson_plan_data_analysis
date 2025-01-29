from error_utils import handleErrorMsg, getTraceback
from src.constants.conversion_constants import excelEngineName
from src.constants.schedule_structures_constants import excelMargin, excelDistance
from pandas import ExcelWriter
import os
from converters_utils import convertToDf, convertToObjOfDfs, delInvalidChars, convertObjOfDfsToJSON
from excel_styles_utils import autoFormatScheduleExcel, autoFormatOverviewExcel



def writeAsDfToExcelSheet(writer=ExcelWriter, excelFilePath='', sheetName='', dataToEnter=None, coords={'row':0, 'col':0}, isConverted=True, doesWriteMsg=False):
    msgText = ''
    
    try:
        df = dataToEnter   if isConverted   else convertToDf(dataToEnter)
        
        df.to_excel(writer, sheet_name=delInvalidChars(sheetName), startrow=excelMargin['row']+coords['row'], startcol=excelMargin['col']+coords['col'], merge_cells=True)

        if doesWriteMsg:
            msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}[{sheetName}].'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}[{sheetName}].', getTraceback(e))

    if msgText: print(msgText)



def writeObjOfDfsToExcel(writer=ExcelWriter, excelFilePath='', dataToEnter=None, isConverted=True):
    msgText = ''

    try:
        # group contains classes, teachers, subjects
        groupDfs = convertToObjOfDfs(dataToEnter)   if not isConverted   else dataToEnter

        for groupName in groupDfs:   
            writeAsDfToExcelSheet(writer, excelFilePath, groupName, groupDfs[groupName])

        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.'


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
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



def writeExcelWorksheetsWithMultipleDfs(writer=ExcelWriter, excelFilePath='', dataToEnter=None, isConverted=True, writingDirection='row'):
    msgText = ''

    try:
        # group contains classes, teachers, subjects
        groupDfs = {el: convertToObjOfDfs(dataToEnter[el])   for el in dataToEnter}   if not isConverted   else dataToEnter
        
        for groupName in groupDfs:
            coords = {'row':0, 'col':0}

            for singleDf in groupDfs[groupName]:
                
                writeAsDfToExcelSheet( writer, excelFilePath, groupName, singleDf, coords )

                if writingDirection == 'row':
                    coords['col'] = coords['col'] + singleDf.shape[1] + singleDf.index.nlevels + excelDistance['col']

                elif writingDirection == 'col':
                    coords['row'] = coords['row'] + singleDf.shape[0] + singleDf.columns.nlevels + excelDistance['row']


        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForExcelWorksheetsWithMultipleDfs(excelFilePath='', objOfMultipleDfs=None, writingDirection='row', doesNeedFormat=True):
    msgText=''

    try:
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
            writeExcelWorksheetsWithMultipleDfs(writer, excelFilePath, objOfMultipleDfs, True, writingDirection)

            if doesNeedFormat:
                autoFormatOverviewExcel(writer.book, excelFilePath)

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