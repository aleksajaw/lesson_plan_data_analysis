from error_utils import handleErrorMsg, getTraceback
from src.constants.conversion_constants import excelEngineName, JSONIndentValue
from src.constants.schedule_structures_constants import excelMargin, excelDistance
from converters_utils import convertToDf, convertToObjOfDfs, delInvalidChars, convertObjOfDfsToJSON, correctDfContent
from excel_utils import countInnerCoords
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



def writerForObjOfDfsToJSONAndExcel(dfsJSONFilePath='', excelFilePath='', schedulesObj={}):
    msgText=''
    try:
        if writeObjOfDfsToJSON(dfsJSONFilePath, schedulesObj):
            writerForObjOfDfsToExcel(excelFilePath, schedulesObj)
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(dfsJSONFilePath)} and {os.path.basename(excelFilePath)}.', getTraceback(e))

    if msgText: print(msgText)



def writeListOfObjsWithMultipleDfsToExcel(writer=ExcelWriter, excelFilePath='', listOfObjsWithMultipleDfs={}):
    msgText = ''

    try:
        for sheetName, sheetObj in listOfObjsWithMultipleDfs.items():            
            for excelDfObj in sheetObj:
                dfInnerCoords = { 'row': excelDfObj['startrow'],
                                  'col': excelDfObj['startcol'] }

                writeDfToExcelSheet( writer, excelFilePath, sheetName, excelDfObj['df'], dfInnerCoords )


        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForListOfObjsWithMultipleDfsToExcel(excelFilePath='', listOfObjsWithMultipleDfs={}, doesNeedFormat=True):
    msgText=''

    try:
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
            writeListOfObjsWithMultipleDfsToExcel(writer, excelFilePath, listOfObjsWithMultipleDfs)

            if doesNeedFormat:
                autoFormatOverviewExcel(writer.book, excelFilePath)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writeListOfObjsWithMultipleDfsToJSON(multiDfsJSONFilePath='', listOfObjsWithMultipleDfs=[]):
    msgText = ''
    isFileChanged = False

    try:
        listOfObjsWithMultipleDfsJSON = {}

        for sheetName, sheetObj in listOfObjsWithMultipleDfs.items():
            listOfObjsWithMultipleDfsJSON[sheetName] = []

            for excelDfObj in sheetObj:
                [startRow, startCol, df] = excelDfObj.values()
                
                listOfObjsWithMultipleDfsJSON[sheetName].append( { 'startrow' : startRow,
                                                                   'startcol' : startCol,
                                                                   'df'       : correctDfContent(df, True).to_json(orient='split') } )

        listOfObjsWithMultipleDfsJSON = json.dumps(listOfObjsWithMultipleDfsJSON, indent=JSONIndentValue)
        isFileChanged = compareAndUpdateFile(multiDfsJSONFilePath, listOfObjsWithMultipleDfsJSON)


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(multiDfsJSONFilePath)}.', getTraceback(e))

    if msgText: print(msgText)


    return isFileChanged



def writerForListOfObjsWithMultipleDfsToJSONAndExcel(multiDfsJSONFilePath='', excelFilePath='', objsWithMultipleDfs=[], writingDirection='row', doesNeedFormat=True):
    msgText = ''

    try:
        listOfObjsWithMultipleDfs = {}
        
        for sheetName, sheetDfs in objsWithMultipleDfs.items():
            listOfObjsWithMultipleDfs[sheetName] = []

            innerCoords = { 'row': 0,
                            'col': 0 }

            for df in sheetDfs:
                listOfObjsWithMultipleDfs[sheetName].append( { 'startrow' : innerCoords['row'],
                                                               'startcol' : innerCoords['col'],
                                                               'df'       : correctDfContent(df, True) } )
                
                innerCoords = countInnerCoords(writingDirection, innerCoords, df)
        

        if writeListOfObjsWithMultipleDfsToJSON(multiDfsJSONFilePath, listOfObjsWithMultipleDfs):
            writerForListOfObjsWithMultipleDfsToExcel(excelFilePath, listOfObjsWithMultipleDfs)
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the files {os.path.basename(multiDfsJSONFilePath)} and {os.path.basename(excelFilePath)}.', getTraceback(e))

    if msgText: print(msgText)



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