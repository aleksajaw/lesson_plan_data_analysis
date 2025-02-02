from error_utils import handleErrorMsg, getTraceback
from src.constants.conversion_constants import excelEngineName, JSONIndentValue
from src.constants.schedule_structures_constants import excelMargin, excelDistance
from converters_utils import convertToDf, convertToObjOfDfs, delInvalidChars, convertObjOfDfsToJSON, correctValsInColsWithNumbers
from excel_styles_utils import autoFormatScheduleExcel, autoFormatExcelCellSizes, autoFormatScheduleExcelCellStyles, autoFormatOverviewExcel
from files_utils import compareAndUpdateFile
from pandas import ExcelWriter, DataFrame
import os
import json



def writeDfToExcelSheet(writer=ExcelWriter, excelFilePath='', sheetName='', dataToEnter=None, innerCoords={'row':0, 'col':0}, isConverted=True, doesWriteMsg=False):
    msgText = ''
    
    try:
        df = dataToEnter   if isConverted   else convertToDf(dataToEnter)
        
        df.to_excel(writer, sheet_name=delInvalidChars(sheetName), startrow=excelMargin['row']+innerCoords['row'], startcol=excelMargin['col']+innerCoords['col'], merge_cells=True)

        if doesWriteMsg:
            msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}[{sheetName}].'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}[{sheetName}].', getTraceback(e))

    if msgText: print(msgText)



def writerForDfToExcelSheet(excelFilePath='', df=DataFrame, groupName=''):
    
    msgText=''

    try:
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
            writeDfToExcelSheet(writer, excelFilePath, groupName, df)

            #autoFormatScheduleExcel(writer.book, excelFilePath, doesNeedFormatStyle, doesNeedFormatSize)
        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writeObjOfDfsToExcel(writer=ExcelWriter, excelFilePath='', dataToEnter=None, isConverted=True, doesWriteMsg=True):
    msgText = ''

    try:
        # group contains classes, teachers, subjects
        groupDfs = convertToObjOfDfs(dataToEnter)   if not isConverted   else dataToEnter

        for groupName in groupDfs:
            writeDfToExcelSheet(writer, excelFilePath, groupName, groupDfs[groupName])

        if doesWriteMsg:
            msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForObjOfDfsToExcel(excelFilePath='', objOfDfs=None, doesNeedFormatStyle=True, doesNeedFormatSize=True):
    msgText=''

    try:
        firstDf = next(iter(objOfDfs.values()))
        dfsRowIndexLen = firstDf.index.nlevels
        dfsdefColNamesLen = firstDf.columns.nlevels

        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
            writeObjOfDfsToExcel(writer, excelFilePath, objOfDfs, True, False)

            autoFormatScheduleExcel(writer.book, excelFilePath, doesNeedFormatStyle, dfsRowIndexLen, dfsdefColNamesLen, doesNeedFormatSize)

        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForObjOfDfsToJSONAndExcel(schedulesObj={}, dfsJSONFilePath='', excelFilePath=''):
    msgText=''
    try:
        if writeObjOfDfsToJSON(dfsJSONFilePath, schedulesObj):
            writerForObjOfDfsToExcel(excelFilePath, schedulesObj)
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(dfsJSONFilePath)} and {os.path.basename(excelFilePath)}.', getTraceback(e))

    if msgText: print(msgText)



def writeListOfObjsWithMultipleDfsToExcel(writer=ExcelWriter, excelFilePath='', dataToEnter=None, isConverted=True, writingDirection='row'):
    msgText = ''

    try:
        # group contains classes, teachers, subjects
        groupDfs = {el: convertToObjOfDfs(dataToEnter[el])   for el in dataToEnter}   if not isConverted   else dataToEnter
        
        for groupName in groupDfs:
            innerCoords = {'row':0, 'col':0}

            for singleDf in groupDfs[groupName]:
                
                writeDfToExcelSheet( writer, excelFilePath, groupName, singleDf, innerCoords )

                if writingDirection == 'row':
                    innerCoords['col'] = innerCoords['col'] + singleDf.shape[1] + singleDf.index.nlevels + excelDistance['col']

                elif writingDirection == 'col':
                    innerCoords['row'] = innerCoords['row'] + singleDf.shape[0] + singleDf.columns.nlevels + excelDistance['row']


        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForListOfObjsWithMultipleDfsToExcel(excelFilePath='', objOfMultipleDfs=None, writingDirection='row', doesNeedFormat=True):
    msgText=''

    try:
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
            writeListOfObjsWithMultipleDfsToExcel(writer, excelFilePath, objOfMultipleDfs, True, writingDirection)

            if doesNeedFormat:
                autoFormatOverviewExcel(writer.book, excelFilePath)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForObjWithMultipleDfsToJSONAndExcel(objOfMultipleDfs=None, dfsJSONFilePath='', excelFilePath='', writingDirection='row', doesNeedFormat=True):
    msgText = ''
    isFileChanged = False

    try:
        groupDfs = {}
        groupDfsJSON = {}
        
        for groupName in objOfMultipleDfs:
            innerCoords = { 'row': 0,
                            'col': 0 }
            
            groupDfs[groupName] = []
            groupDfsJSON[groupName] = []

            for singleDf in objOfMultipleDfs[groupName]:
                
                groupDfs[groupName].append(         { 'startrow' : innerCoords['row'],
                                                      'startcol' : innerCoords['col'],
                                                      'df'       : singleDf           } )
                
                # Restore 111 from values like '111.0'.
                singleDf = correctValsInColsWithNumbers(singleDf, True)
                
                groupDfsJSON[groupName].append(     { 'startrow' : innerCoords['row'],
                                                      'startcol' : innerCoords['col'],
                                                      'df'       : singleDf.to_json(orient='split') } )

                if   writingDirection == 'row':
                    innerCoords['col'] = innerCoords['col'] + singleDf.shape[1] + singleDf.index.nlevels + excelDistance['col']

                elif writingDirection == 'col':
                    innerCoords['row'] = innerCoords['row'] + singleDf.shape[0] + singleDf.columns.nlevels + excelDistance['row']
        

        isFileChanged = compareAndUpdateFile(dfsJSONFilePath, json.dumps(groupDfsJSON, indent=JSONIndentValue))
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file.', getTraceback(e))

    if msgText: print(msgText)

    return isFileChanged



def writeObjOfDfsToJSON(filePath='', objOfDfs=None):
    msgText = ''
    isFileChanged = False

    try:
        dataToEnter = convertObjOfDfsToJSON(objOfDfs)
        isFileChanged = compareAndUpdateFile(filePath, dataToEnter)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(filePath)}.', getTraceback(e))

    if msgText: print(msgText)

    return isFileChanged