from src.constants import scheduleExcelClassesPath, weekdays, lessonAttrs3el, timeIndexes
from src.utils import autoFormatExcelCellSizes, formatCellBackground, formatCellBorder
import pandas as pd
import numpy as np
import re
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill as openpyxlPatternFill



def autoFormatScheduleExcel(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    autoFormatExcelCellSizes(workbook, excelFilePath)
    autoFormatScheduleExcelCellStyles(workbook, excelFilePath)



def autoFormatScheduleExcelCellStyles(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):

    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(excelFilePath)

        if (workbook):
            for ws in workbook.worksheets:
                
                permEmptyCellStyle = openpyxlPatternFill(fill_type='lightTrellis')
                
                # merge and format empty cells in the corner between the MultiIndexes
                ws.merge_cells('A1:B2')
                ws['A1'].fill = permEmptyCellStyle

                rowsStart = 3
                rowsCount = 0

                # count rows in the 1st and the 2nd column,
                # cells there are less likely to be merged (for easier data analysis)
                for row in ws.iter_rows(min_row=rowsStart, min_col=1, max_col=2):
                    if row[1].value is not None:
                        rowsCount += 1
                    else:
                        break
                

                totalRowsCount = rowsStart-1 + rowsCount
                rowIndexesColsEnd = 2
                colIndexesRowsEnd = 2
                colDaysStart = 3
                lenOfWeekdays = len(weekdays)
                lenOfLessonAttrs = len(lessonAttrs3el)
                totalColsCount = colDaysStart-1 + lenOfWeekdays * lenOfLessonAttrs
                

                # row with number rowsStart in the 1st two columns
                # contains the names for the rows' MultiIndex
                allEmpty = True 

                # check if the cells in the 1st row below column indexes are empty
                for col in range(colDaysStart, totalColsCount+1):
                    
                    if ws.cell(row=rowsStart, column=col).value is not None:
                        allEmpty = False
                        break


                # change the BACKGROUND of the cells in the row below column indexes
                # only if entire row is empty
                if allEmpty:
                    
                    # MERGE CELLS in the row 
                    ws.merge_cells( start_row=rowsStart, start_column=colDaysStart,
                                    end_row=rowsStart,   end_column=totalColsCount )
                    
                    cell = ws.cell(row=rowsStart, column=colDaysStart)
                    cell.fill = permEmptyCellStyle

                    #startCoordinate = f'{get_column_letter(colDaysStart)}{rowsStart}'
                    #endCoordinate = f'{get_column_letter(totalColsCount)}{rowsStart}'
                    
                    #for cell in ws[startCoordinate:endCoordinate][0]:
                    #    formatCellBorder(cell, bottom='thin')


                # add MEDIUM RIGHT BORDERS
                # at the end of each important column and each day
                dayColsEnd = [colIndexesRowsEnd + i * 3 for i in range(1, 6)]
                rowIndexesColsList = list(range(1, colIndexesRowsEnd+1))
                thickerColsList = rowIndexesColsList + dayColsEnd

                for thickerCol in thickerColsList:
                    for row in range(1, totalRowsCount+1):
                        cell = ws.cell(row=row, column=thickerCol)
                        formatCellBorder(cell, right='medium')
                        # add THIN SIDE BORDERS to the center column on days
                        if thickerCol > rowIndexesColsEnd:
                            cell = ws.cell(row=row, column=thickerCol-1)
                            formatCellBorder(cell, left='thin', right='thin')
                

                # add MEDIUM BOTTOM BORDERS
                # at the end of each index and the entire schedule
                colIndexesRowsList = list(range(1, colIndexesRowsEnd+1))[1:]
                thickerRowsList = colIndexesRowsList + [rowsStart, totalRowsCount]

                for thickerRow in thickerRowsList:
                    colsLimit = totalColsCount+1
                    # ignore long merged cell
                    if thickerRow==rowsStart:
                        colsLimit = rowIndexesColsEnd+1

                    for col in range(1, colsLimit):
                        cell = ws.cell(row=thickerRow, column=col)
                        formatCellBorder(cell, bottom='medium')


                # add BACKGROUND for the lessons with an odd numbers
                # and HAIR/THIN BORDERS
                #rowsToBeColoured = []
                for row in range(1, ws.max_row + 1):
                    # fast checking if the row is in the specific merged range (for col A here)
                    merged = next(  ( r   for r in ws.merged_cells.ranges
                                          if r.min_col == 1 and r.min_row <= row <= r.max_row ),
                                    None)
                

                    for col in range(1, totalColsCount+1):
                        cellForBorder = ws.cell(row=row, column=col)
                        # thinner ('HAIR') BORDER inside merged row
                        #if merged and merged.min_row != row:
                        #    topBorderStyle = 'hair'
                        # THIN BORDER for outer frame
                        #elif not cellForBorder.border.top.style:
                        topBorderStyle = 'thin'
                        formatCellBorder(cellForBorder, top=topBorderStyle)


                    # set LIGHT GREY BACKGROUND
                    rowNr = merged.min_row   if merged   else row
                    cellValue = ws.cell(row=rowNr, column=1).value
                    if isinstance(cellValue, int) and (cellValue % 2 != 0):
                        #rowsToBeColoured.append(row)
                        for col in range(1, totalColsCount+1):
                            cell = ws.cell(row=row, column=col)
                            formatCellBackground(cell, fillType='solid', startColor='E5E5E5', endColor='E5E5E5')


    except Exception as e:
        print('Error while formatting the cell styles in the Excel file:', e)



def concatAndFilterScheduleDataFrames(el1=None, el2=None):
    msgText = ''

    try:
        #el1 = el1.dropna(axis=1, how='all')
        el2 = el2.dropna(axis=1, how='all')
        newDf = pd.concat([el1, el2])#.sort_index()
        rowsFiltered = []

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
                        singleRow[col] = value

            rowsFiltered.append(singleRow)


        newDfFiltered = pd.DataFrame(rowsFiltered).set_index(keys=newDf.index.names)
        newDfFiltered = newDfFiltered.reindex(columns=newDf.columns, fill_value=np.nan)

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
        return [item[0]   for item in data]
    
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