from error_utils import handleErrorMsg, getTraceback
from src.constants.conversion_constants import excelEngineName, JSONIndentValue
from src.constants.excel_constants import excelMargin, excelDistance
from converters_utils import delInvalidChars, convertObjOfDfsToJSON, correctDfContent #, convertToDf, convertToObjOfDfs,
from excel_utils import countInnerCoords
from excel_styles_utils import autoFormatScheduleExcel, autoFormatOverviewExcel#, autoFormatExcelCellSizes, autoFormatScheduleExcelCellStyles, 
from files_utils import compareAndUpdateFile
from pandas import ExcelWriter#, DataFrame
import os
import json



def writeDfToExcelSheet(writer, excelFilePath, sheetName, df, innerCoords={'row':0, 'col':0}, doesWriteMsg=False, showIndex=True, showHeader=True, mergeCells=True):
    msgText = ''

    try:
        #if writer is None:
        #    writer = ExcelWriter
        #if df is None:
        #    df = DataFrame
        #if innerCoords is None:
        #    innerCoords = {'row':0, 'col':0}
        
        df.to_excel(writer, sheet_name=delInvalidChars(sheetName), merge_cells=mergeCells, index=showIndex, header=showHeader,
                    startrow=excelMargin['row']+innerCoords['row'], startcol=excelMargin['col']+innerCoords['col'] )

        if doesWriteMsg:
            msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}[{sheetName}].'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}[{sheetName}].', getTraceback(e))

    if msgText: print(msgText)



def writerForDfToExcelSheet(excelFilePath, df, sheetName, writerMode='w+', mergeCells=True, showIndex=True, showHeader=True):
    
    msgText=''

    try:
        #if df is None:
        #    df = DataFrame
        if os.path.exists(excelFilePath):
            with ExcelWriter(excelFilePath, mode=writerMode, engine=excelEngineName, if_sheet_exists='replace') as writer:       
                writeDfToExcelSheet(writer, excelFilePath, sheetName, df, showIndex=showIndex, showHeader=showHeader, mergeCells=mergeCells)
        
        else:
            with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:
                writeDfToExcelSheet(writer, excelFilePath, sheetName, df, showIndex=showIndex, showHeader=showHeader, mergeCells=mergeCells)

            #autoFormatScheduleExcel(writer.book, excelFilePath, doesNeedFormatStyle, doesNeedFormatSize)
        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writeObjOfDfsToExcel(writer, excelFilePath, dataToEnter, doesWriteMsg=True, showIndex=True, showHeader=True, mergeCells=True):
    msgText = ''

    try:
        #if writer is None:
        #    writer = ExcelWriter
        #if dataToEnter is None:
        #    dataToEnter = {}
        
        # group contains classes, teachers, subjects
        groupDfs = dataToEnter

        for groupName in groupDfs:
            writeDfToExcelSheet(writer, excelFilePath, groupName, groupDfs[groupName], showIndex=showIndex, showHeader=showHeader, mergeCells=mergeCells)

        if doesWriteMsg:
            msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForObjOfDfsToExcel(excelFilePath, objOfDfs, doesNeedFormatStyle=True, doesNeedFormatSize=True, writerMode='a'):
    msgText=''

    try:
        #if objOfDfs is None:
        #    objOfDfs = {}
        
        firstDf = next(iter(objOfDfs.values()))
        dfsRowIndexLen = firstDf.index.nlevels
        dfsdefColNamesLen = firstDf.columns.nlevels

        if os.path.exists(excelFilePath):
            with ExcelWriter(excelFilePath, mode=writerMode, engine=excelEngineName, if_sheet_exists='replace') as writer:       
                writeObjOfDfsToExcel(writer, excelFilePath, objOfDfs, False)

                autoFormatScheduleExcel(writer.book, doesNeedFormatStyle, dfsRowIndexLen, dfsdefColNamesLen, doesNeedFormatSize)
        
        else:
            with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
                writeObjOfDfsToExcel(writer, excelFilePath, objOfDfs, False)

                autoFormatScheduleExcel(writer.book, doesNeedFormatStyle, dfsRowIndexLen, dfsdefColNamesLen, doesNeedFormatSize)


        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForObjOfDfsToJSONAndExcel(dfsJSONFilePath, excelFilePath, schedulesObj):
    msgText=''
    try:
        #if schedulesObj is None:
        #    schedulesObj = {}
        
        if writeObjOfDfsToJSON(dfsJSONFilePath, schedulesObj):
            writerForObjOfDfsToExcel(excelFilePath, schedulesObj)
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(dfsJSONFilePath)} and {os.path.basename(excelFilePath)}.', getTraceback(e))

    if msgText: print(msgText)



def writeListOfObjsWithMultipleDfsToExcel(writer, excelFilePath, listOfObjsWithMultipleDfs, showIndex=True, showHeader=True,mergeCells=True):
    msgText = ''

    try:
        #if writer is None:
        #    writer = ExcelWriter
        #if listOfObjsWithMultipleDfs is None:
        #    listOfObjsWithMultipleDfs = {}
        
        for sheetName, sheetObj in listOfObjsWithMultipleDfs.items():            
            for excelDfObj in sheetObj:
                dfInnerCoords = { 'row': excelDfObj['startrow'],
                                  'col': excelDfObj['startcol'] }

                writeDfToExcelSheet(writer, excelFilePath, sheetName, excelDfObj['df'], dfInnerCoords, showIndex=showIndex, showHeader=showHeader, mergeCells=mergeCells)


        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writerForListOfObjsWithMultipleDfsToExcel(excelFilePath, listOfObjsWithMultipleDfs, doesNeedFormatStyle=True, writerMode='a'):
    msgText=''

    try:
        #if listOfObjsWithMultipleDfs is None:
        #    listOfObjsWithMultipleDfs = {}
        
        if os.path.exists(excelFilePath):
            with ExcelWriter(excelFilePath, mode=writerMode, engine=excelEngineName, if_sheet_exists='replace') as writer:       
                writeListOfObjsWithMultipleDfsToExcel(writer, excelFilePath, listOfObjsWithMultipleDfs)

                autoFormatOverviewExcel(writer.book, doesNeedFormatStyle)
        
        else:
            with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:       
                writeListOfObjsWithMultipleDfsToExcel(writer, excelFilePath, listOfObjsWithMultipleDfs)

                autoFormatOverviewExcel(writer.book, doesNeedFormatStyle)
            

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(excelFilePath)}.', getTraceback(e))
    
    if msgText: print(msgText)



def writeListOfObjsWithMultipleDfsToJSON(multiDfsJSONFilePath, listOfObjsWithMultipleDfs):
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
                                                                   'df'       : df.to_json(orient='split') } )

        listOfObjsWithMultipleDfsJSON = json.dumps(listOfObjsWithMultipleDfsJSON, indent=JSONIndentValue)
        isFileChanged = compareAndUpdateFile(multiDfsJSONFilePath, listOfObjsWithMultipleDfsJSON)


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(multiDfsJSONFilePath)}.', getTraceback(e))

    if msgText: print(msgText)


    return isFileChanged



def writerForListOfObjsWithMultipleDfsToJSONAndExcel(multiDfsJSONFilePath, excelFilePath, objsWithMultipleDfs, doesNeedFormatStyle=True, writingDirection='row', dfsInRowLimit=None):
    msgText = ''

    try:
        listOfObjsWithMultipleDfs = {}
        
        for sheetName, sheetDfs in objsWithMultipleDfs.items():
            listOfObjsWithMultipleDfs[sheetName] = []

            innerCoords = { 'row': 0,
                            'col': 0 }

            dfInLineCounter = 0
            isDirectionRow = writingDirection == 'row'
            writingDirectionConverted = writingDirection
            useDfsLimit = dfsInRowLimit is not None   and   isDirectionRow

            for df in sheetDfs:                

                # Move the DataFrame to the next line if needed.
                if len(listOfObjsWithMultipleDfs[sheetName]):
                    if useDfsLimit:
                        if dfInLineCounter % dfsInRowLimit == 0:
                          writingDirectionConverted = 'col'
                          innerCoords = { 'row': innerCoords['row'] + excelDistance['row'],
                                          'col': 0 }

                        elif writingDirectionConverted != 'row':
                            writingDirectionConverted = 'row'
                      
                    
                    innerCoords = countInnerCoords(df, writingDirectionConverted, innerCoords)
                

                listOfObjsWithMultipleDfs[sheetName].append( { 'startrow' : innerCoords['row'],
                                                               'startcol' : innerCoords['col'],
                                                               'df'       : correctDfContent(df, True) } )
                
                if useDfsLimit:
                    dfInLineCounter = dfInLineCounter+1
        

        if writeListOfObjsWithMultipleDfsToJSON(multiDfsJSONFilePath, listOfObjsWithMultipleDfs):
            writerForListOfObjsWithMultipleDfsToExcel(excelFilePath, listOfObjsWithMultipleDfs, doesNeedFormatStyle)
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the files {os.path.basename(multiDfsJSONFilePath)} and {os.path.basename(excelFilePath)}.', getTraceback(e))

    if msgText: print(msgText)



def writeObjOfDfsToJSON(filePath, objOfDfs):
    msgText = ''
    isFileChanged = False

    try:
        #if objOfDfs is None:
        #    objOfDfs = {}

        dataToEnter = convertObjOfDfsToJSON(objOfDfs)
        isFileChanged = compareAndUpdateFile(filePath, dataToEnter)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while loading data into the file {os.path.basename(filePath)}.', getTraceback(e))

    if msgText: print(msgText)

    return isFileChanged