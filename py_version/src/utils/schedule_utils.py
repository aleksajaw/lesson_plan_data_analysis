from src.constants import scheduleExcelClassesPath, weekdays, timeIndexes, dfColWeekDayNamesTuples3el, dfColWeekDayNamesTuples4el, lessonTimePeriods, dfColWeekDayEmptyRow
from src.utils import autoFormatExcelCellSizes, formatCellBackground, formatCellBorder, dropnaInDfByAxis
import pandas as pd
import numpy as np
import re
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill as openpyxlPatternFill



def autoFormatScheduleExcel(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    autoFormatExcelCellSizes(workbook, excelFilePath)
    autoFormatScheduleExcelCellStyles(workbook, excelFilePath)



def mergeEmptyCellsAndColorBg(ws=None, mergedCellObj={'startRow':int, 'startRow': int, 'startRow': int, 'endCol': int}):
    msgText=''

    try:
        permEmptyCellStyle = openpyxlPatternFill(fill_type='lightTrellis')

        ws.merge_cells( start_row=mergedCellObj['startRow'],
                        start_column=mergedCellObj['startRow'],
                        end_row=mergedCellObj['startRow'],
                        end_column=mergedCellObj['endCol'] )

        ws.cell(row=mergedCellObj['startRow'], column=mergedCellObj['startCol']).fill = permEmptyCellStyle


    except Exception as e:
        msgText = f'Error while merging the empty cells and coloring their background: {e}'


    if msgText: print(msgText)



def colorBgOfEmptyRow(ws=None, colRange=None, row=int, startColumn=int):
    msgText=''

    try:
        permEmptyCellStyle = openpyxlPatternFill(fill_type='lightTrellis')
        allEmpty = True 

        # check if the cells in the 1st row (below column indexes) are empty
        for col in colRange:
            
            if ws.cell(row=row, column=col).value is not None:
                allEmpty = False
                break


        # change the BACKGROUND of the cells in the row (below column indexes)
        # only if entire row is empty
        if allEmpty:
            
            # MERGE CELLS in the row 
            ws.merge_cells( start_row=row, start_column=startColumn,
                            end_row=row,   end_column=max(colRange) )
            
            cell = ws.cell(row=row, column=startColumn)
            cell.fill = permEmptyCellStyle
            

    except Exception as e:
        msgText = f'Error while coloring the background of empty rows: {e}'

    if msgText: print(msgText)



def findLastBoldRowAtBeggining(ws, minCol=1):
    msgText=''

    try:
        lastBoldRowAtBeggining = -1
        rowTemp = 1
        for col in ws.iter_cols(min_col=minCol, min_row=rowTemp):
            for cell in col:
                if cell.font and cell.font.bold:
                    lastBoldRowAtBeggining = cell.row
                    rowTemp = lastBoldRowAtBeggining
                else:
                    break
    
    except Exception as e:
        msgText = f'Error while searching for the last bold row at the beggining: {e}'

    if msgText: print(msgText)

    return lastBoldRowAtBeggining
                        


def autoFormatScheduleExcelCellStyles(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    from excel_utils import getNrOfLastNonEmptyCellInCol

    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(excelFilePath)

        if (workbook):
            for ws in workbook.worksheets:
                
                # column nr where the row indexes end
                rowIndexesLastCol = 2

                # bold rows are for headers
                lastBoldRowAtBeggining = findLastBoldRowAtBeggining(ws, rowIndexesLastCol)

                # merge and format empty cells in the corner between the MultiIndexes
                mergeEmptyCellsAndColorBg(ws, { 'startRow': 1,
                                                'startCol': 1,
                                                'endRow': lastBoldRowAtBeggining,
                                                'endCol': rowIndexesLastCol } )

                lastMergedCellColIn1stRow = max([cell.max_col   for cell in ws.merged_cells
                                                                if cell.min_row==1])
                
                # cells in the 1st two columns which row nr equals contentRowsStart
                # contains the names for the rows' MultiIndex
                contentFirstRow = lastBoldRowAtBeggining+1
                # col nr for the 1st cell for the 1st day
                daysFirstColList = rowIndexesLastCol+1

                totalColsCount = lastMergedCellColIn1stRow
                totalColsRange = range(1, totalColsCount+1)
                # cells in the 2nd column contain part of rows indexes & are less likely to be merged (for easier data analysis)
                totalRowsCount = lastBoldRowAtBeggining + getNrOfLastNonEmptyCellInCol(ws, minRow=contentFirstRow, col=2)                    
                totalRowsRange = range(1, totalRowsCount+1)

                colorBgOfEmptyRow(ws, range(rowIndexesLastCol+1, totalColsCount+1), row=contentFirstRow, startColumn=daysFirstColList)


                # add MEDIUM RIGHT BORDERS
                # at the end of each important column and each day
                daysLastCol = sorted([mergedCellRange.max_col  for mergedCellRange in ws.merged_cells
                                                              if mergedCellRange.min_row==mergedCellRange.max_row==1
                                                                and mergedCellRange.min_col > 2])
                rowIndexesCols = list(range(1, rowIndexesLastCol+1))
                colsWithRightMediumBorder = rowIndexesCols + daysLastCol
                standardDaySize = daysLastCol[0] - rowIndexesLastCol

                for col in colsWithRightMediumBorder:
                    for row1 in totalRowsRange:
                        cell = ws.cell(row=row1, column=col)
                        formatCellBorder(cell, right='medium')

                        # add THIN SIDE BORDERS to the center column on days
                        # do not include the columns reserved for the rows indexes
                        if rowIndexesLastCol < col:
                            for attrCol in range((col-standardDaySize)+1, col):
                                cell = ws.cell(row=row1, column=attrCol)
                                formatCellBorder(cell, left='thin', right='thin')
                

                # add MEDIUM BOTTOM BORDERS
                # at the end of each index (for columns, for rows) and the entire schedule
                rowsWithBottomBorder = [lastBoldRowAtBeggining, contentFirstRow, totalRowsCount]

                for row in rowsWithBottomBorder:
                    colsLimit = totalColsCount+1
                    # ignore long merged cell
                    if row==contentFirstRow:
                        colsLimit = rowIndexesLastCol+1

                    for col in range(1, colsLimit):
                        cell = ws.cell(row, column=col)
                        formatCellBorder(cell, bottom='medium')


                # add BACKGROUND for the lessons with an odd numbers
                # and HAIR/THIN BORDERS
                #rowsToBeColoured = []
                for row in totalRowsRange:
                    colsLimit = totalColsCount+1

                    # fast checking if the row is in the specific merged range (for col A here)
                    merged = next(  ( r   for r in ws.merged_cells.ranges
                                          if r.min_col == 1 and r.min_row <= row <= r.max_row ),
                                    None)

                    for col in range(1, colsLimit):
                        cell = ws.cell(row, column=col)
                        # thinner ('HAIR') BORDER inside merged row
                        #if merged and merged.min_row != row:
                        #    topBorderStyle = 'hair'
                        # THIN BORDER for outer frame
                        #elif not cell.border.top.style:
                        topBorderStyle = 'thin'
                        formatCellBorder(cell, top=topBorderStyle)


                    # set LIGHT GREY BACKGROUND
                    rowNr = merged.min_row   if merged   else row
                    cellValue = ws.cell(row=rowNr, column=1).value

                    if isinstance(cellValue, int) and (cellValue % 2 != 0):
                        #rowsToBeColoured.append(row)
                        for col in totalColsRange:
                            cell = ws.cell(row, column=col)
                            formatCellBackground(cell, fillType='solid', startColor='E5E5E5', endColor='E5E5E5')


    except Exception as e:
        print('Error while formatting the cell styles in the Excel file:', e)



def concatAndFilterScheduleDataFrames(el1=None, el2=None, addNewCol=False, newColName='', newColVal=''):
    msgText = ''

    try:
        # two lines below prevents FutureWarning:
        #   The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.
        #   In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes.
        #   To retain the old behavior, exclude the relevant entries before the concat operation.
        el1 = dropnaInDfByAxis(el1, 1)
        el2 = dropnaInDfByAxis(el2, 1)
        newDf = pd.concat([el1, el2])#.sort_index()
        rowsFiltered = []

        prepareNewColVal = addNewCol and newColName and newColVal

        colDayNamesTuples = dfColWeekDayNamesTuples4el   if addNewCol   else dfColWeekDayNamesTuples3el

        # iterate through rows (time indexes)
        for (day, time), singleLessonAttr in newDf.groupby(timeIndexes):
            singleRow = {}
            singleRow[timeIndexes[0]] = day
            singleRow[timeIndexes[1]] = time

            for col in newDf.columns:
                booleanMask = singleLessonAttr[col] != ''
                nonEmptyValues = singleLessonAttr[col][booleanMask].dropna().tolist()

                if nonEmptyValues:
                    for value in nonEmptyValues:
                        
                        # add empty rows to avoid tables that do not start from row nr 1
                        if len(rowsFiltered) < singleRow[timeIndexes[0]]-1:
                            
                            lastFilteredRowNr = ( int( rowsFiltered[-1][timeIndexes[0]] )  if len(rowsFiltered)
                                                                                           else 0 )
                            currRowNr = int( singleRow[timeIndexes[0]] )
                            missingNrs = list( range( lastFilteredRowNr+1, currRowNr ) )
                            desiredNr = missingNrs[0]

                            singleRowTemp = dfColWeekDayEmptyRow
                            
                            while desiredNr and lastFilteredRowNr != missingNrs[-1]:
                                
                                desiredPreviousTime = lessonTimePeriods[ desiredNr-1 ]
                                singleRowTemp[timeIndexes[0]] = desiredNr
                                singleRowTemp[timeIndexes[1]] = desiredPreviousTime
                                
                                rowsFiltered.append(singleRowTemp.copy())

                                lastFilteredRowNr = int(rowsFiltered[-1][timeIndexes[0]])
                                missingNrs = missingNrs[1:]   if len(missingNrs)   else []
                                desiredNr  = missingNrs[0]    if len(missingNrs)   else 0


                        singleRow[col] = value


                    if prepareNewColVal:
                        if not (col[0], newColName) in singleRow:
                            singleRow[(col[0], newColName)] = (newColVal   if not newColVal.isdigit()
                                                                           else int(newColVal))


            rowsFiltered.append(singleRow)


        if addNewCol or ( len(newDf.columns.get_level_values(0)) < len(weekdays) ):
            
            columnsVal = pd.MultiIndex.from_tuples(colDayNamesTuples)
        
        else:
            columnsVal = newDf.columns
        
        newDfFiltered = pd.DataFrame(rowsFiltered).set_index(keys=timeIndexes)
        #print(newDfFiltered)
        newDfFiltered = newDfFiltered.reindex(columns=columnsVal, fill_value=np.nan)

        #print(newDfFiltered)

        return newDfFiltered
    
    except Exception as e:
        msgText = f'Error while concatenating Data Frames for Excel worksheet: {e}'
        
    if msgText: print(msgText)



def createGroupsInListByPrefix(data=[], splitDelimeter = '-', replaceDelimeter = '.r'):
    msgText = ''

    try:
        # only leave the part before the first '-' and cut '.r' out
        groupList = [ (str(item).split(splitDelimeter)[0]).replace(replaceDelimeter,'')
                            if isinstance(item, str)
                            else item
                          for item in data ]
        
        # group elements by names starting with the same prefix
        for i in range(2, len(groupList)):
            gList = groupList
            if ( all( isinstance(x, str)   for x in [gList[i-1], gList[i]] )
                  and  gList[i].startswith(gList[i-1]) ):
                
                groupList[i] = gList[i-1]
    
    except Exception as e:
        msgText = f'Error while creating groups in list by prefix: {e}'
    
    if msgText: print(msgText)
    
    return groupList



def createGroupsInListByFirstLetter(data=[]):
    msgText = ''

    try:
        newData = []
        for item in data:
            #if any(c.isdigit()   for c in item):
            match = re.match(r'[^\d\w]+[a-zA-Z]*', item)

            if match:
              if item!=match[0]:
                # e.g. '#re4'   =>   '#re'
                newData.append(match[0])

              else:
                # e.g. '#re'   =>   '#r'
                newData.append(match[1])
            
            else:
                newData.append(item[0])

        return newData
        #return [item[0]   for item in data]
    
    except Exception as e:
        msgText = f'Error while creating groups in list by first letter: {e}'
    
    if msgText: print(msgText)



def createGroupsInListByNumbers(data=[], optionalPartInNrPrefix='0'):
    msgText=''

    try:
        groupsInList = []
        for item in data:
            itemStr = str(item)
            itemLen = len(itemStr)
            
            if any(c.isalpha()   for c in itemStr):
                item = ''.join([c   for c in itemStr if c.isalpha()])

            elif itemStr.isdigit():
                if itemLen > 1:
                    item = itemStr[0] + (itemLen-1) * '0'
              
                elif 0 < int(item) < 10:
                    item = 1
                
                item = int(item)
            
            else:
                # match e.g. '.9', '_09', '09' or '9'
                pattern = r'([^a-zA-Z0-9]*' + re.escape(optionalPartInNrPrefix) + r'*[^a-zA-Z0-9]*)\d+'
                match = re.match(pattern, itemStr)
                
                if match:
                    # '.', '_0', '0'   only if   optionalPartInNrPrefix = 0
                    item = match.group(1)
            
            groupsInList.append(item)
        
        return groupsInList
    
    except Exception as e:
        msgText = f'Error while creating groups in list by numbers: {e}'
    
    if msgText: print(msgText)



def createGroupsInListBy(groupName='', data=[]):
    result = []
    msgText = ''
    
    try:
        match groupName:
            case 'subjects':
                result = createGroupsInListByPrefix(data)
        
            case 'teachers':
                result = createGroupsInListByFirstLetter(data)

            case 'classrooms':
                result = createGroupsInListByNumbers(data)


    except Exception as e:
        msgText = f'Error while creating groups in list by...: {e}'
    
    if msgText: print(msgText)

    return result