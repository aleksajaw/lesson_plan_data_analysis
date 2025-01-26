from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleExcelClassesPath
from excel_utils import get1stNotMergedCell
from pandas import ExcelWriter
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment as openpyxlAlignment
from openpyxl.styles import PatternFill as openpyxlPatternFill
from openpyxl.styles import Border as openpyxlBorder
from openpyxl.styles import Side as openpyxlSide
from openpyxl.cell.cell import Cell as openpyxlCell
from openpyxl.cell.cell import MergedCell as openpyxlMergedCell
from openpyxl.utils import column_index_from_string



def autoFormatScheduleExcel(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    autoFormatExcelCellSizes(workbook, excelFilePath)
    autoFormatScheduleExcelCellStyles(workbook, excelFilePath)
                        


def autoFormatScheduleExcelCellStyles(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    from src.utils.excel_utils import getNrOfLastNonEmptyCellInCol
    msgText=''

    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(excelFilePath)

        if (workbook):
            for ws in workbook.worksheets:
                
                # column nr where the row indices end
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
                # cells in the 2nd column contain part of rows indices & are less likely to be merged (for easier data analysis)
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
                        # do not include the columns reserved for the rows indices
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

                    if isinstance(cellValue, int) and (cellValue & 1):
                        #rowsToBeColoured.append(row)
                        for col in totalColsRange:
                            cell = ws.cell(row, column=col)
                            formatCellBackground(cell, fillType='solid', startColor='E5E5E5', endColor='E5E5E5')


    except Exception as e:
        msgText = handleErrorMsg('\nError while formatting the cell styles in the Excel file.', getTraceback(e))
      
    if msgText: print(msgText)


    
def autoFormatExcelCellSizes(workbook=None, excelFilePath=scheduleExcelClassesPath):

    msgText = ''
    
    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(excelFilePath)

        if (workbook):
            rowsCounter = 0

            for ws in workbook.worksheets:
                rowsCounter+=1
                rowsLines = {}
                colsLength = {}


                for col in ws.columns:

                    colLetter = get1stNotMergedCell(col).column_letter
                    colIndex = column_index_from_string(colLetter)
                    
                    # init content length for specific column in worksheet
                    colsLength[colIndex] = 1


                    for cell in col:

                        if cell.row not in rowsLines:
                            rowsLines[cell.row] = 1

                        maxRowLines = rowsLines[cell.row]
                        maxColLength = colsLength[cell.column]
                        
                        if isinstance(cell.value, str) and '\n' in cell.value:

                            linesCount = cell.value.count('\n') + 1
                            rowsLines[cell.row] = max(maxRowLines, linesCount)
                            temp = cell.value.split('\n')

                            for t in temp:
                                colsLength[cell.column] = max(maxColLength, len(str(t)))

                        else:
                            colsLength[cell.column] = max(maxColLength, len(str(cell.value)))

                        cell.alignment = openpyxlAlignment(wrap_text=True, horizontal='center', vertical='center')


                    ws.column_dimensions[colLetter].width = colsLength[colIndex] + 2

                defaultFontSize = 11
                for row in range(1,len(rowsLines)+1):
                    ws.row_dimensions[row].height = rowsLines[row] * defaultFontSize * 1.3

            workbook.save(excelFilePath)

    except Exception as e:
        msgText = handleErrorMsg('\nError while formatting the cell sizes in the Excel file.', getTraceback(e))

    if msgText: print(msgText)



def formatCellBorder(cell=None, right='', left='', top='', bottom=''):
    msgText = ''

    if isinstance(cell, (openpyxlCell, openpyxlMergedCell)):
        try:
            currentBorder = cell.border
            defaultColor = '000000'
            borderStyle = { 'hair':   openpyxlSide(border_style='hair',   color=defaultColor),
                            'thin':  openpyxlSide(border_style='thin',  color=defaultColor),
                            'medium': openpyxlSide(border_style='medium', color=defaultColor),
                            'thick':   openpyxlSide(border_style='thick',   color=defaultColor) }
            
            cell.border = openpyxlBorder( right = borderStyle[right]    if right    else currentBorder.right,
                                          left = borderStyle[left]      if left     else currentBorder.left,
                                          top = borderStyle[top]        if top      else currentBorder.top,
                                          bottom = borderStyle[bottom]  if bottom   else currentBorder.bottom )

        except Exception as e:
            msgText = handleErrorMsg('\nError while formatting the cell.', getTraceback(e))
            
    else:
        msgText = "\nError while formatting the cell: The value must be of type 'Cell'."
    
    if msgText: print(msgText)



def formatCellBackground(cell=None, fillType='', startColor='', endColor=''):
    msgText = ''

    if isinstance(cell, (openpyxlCell, openpyxlMergedCell)):
        try:
            if (  fillType=='solid'
                  and isinstance(startColor, str) and startColor != ''
                  and isinstance(startColor, str) and endColor != '' ):
                
                cell.fill = openpyxlPatternFill(start_color=startColor, end_color=endColor, fill_type=fillType)
            
            elif fillType:
                cell.fill = openpyxlPatternFill(fill_type=fillType)

        except Exception as e:
            msgText = handleErrorMsg('\nError while formatting the cell.', getTraceback(e))
            
    else:
        msgText = '\nError while formatting the cell: The value must be of type \'Cell\'.'

    if msgText: print(msgText)



def addBgToExcelSheetRowsBasedOnObj(writer=ExcelWriter, sheetRowsToColor={'rows':[], 'colsLength':0}):
    # add BACKGROUND to the (odd here) groups of the cells in worksheet 
    msgText = ''

    try:
        workbook = writer.book
        if workbook:
                            
            for sheetname in workbook.sheetnames:
                ws = workbook[sheetname]
                sheetBgRanges = sheetRowsToColor[sheetname]

                for grRow in sheetBgRanges['rows']:
                    for col in range(1, sheetBgRanges['colsLength']+1):
                        cell = ws.cell(row=grRow, column=col)
                        formatCellBackground(cell, 'solid', 'f3f3f3', 'f3f3f3')
    
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while adding background to the cells in the Excel sheet rows.', getTraceback(e))
    
    if msgText: print(msgText)


def mergeEmptyCellsAndColorBg(ws=None, mergedCellObj={'startRow':int, 'startCol': int, 'endRow': int, 'endCol': int}):
    msgText=''

    try:
        permEmptyCellStyle = openpyxlPatternFill(fill_type='lightTrellis')

        ws.merge_cells( start_row=mergedCellObj['startRow'],
                        start_column=mergedCellObj['startCol'],
                        end_row=mergedCellObj['endRow'],
                        end_column=mergedCellObj['endCol'] )

        ws.cell(row=mergedCellObj['startRow'], column=mergedCellObj['startCol']).fill = permEmptyCellStyle


    except Exception as e:
        msgText = handleErrorMsg('\nError while merging the empty cells and coloring their background.', getTraceback(e))


    if msgText: print(msgText)



def colorBgOfEmptyRow(ws=None, colRange=None, row=int, startColumn=int):
    msgText=''

    try:
        permEmptyCellStyle = openpyxlPatternFill(fill_type='lightTrellis')
        allEmpty = True 

        # check if the cells in the 1st row (below column indices) are empty
        for col in colRange:
            
            if ws.cell(row=row, column=col).value is not None:
                allEmpty = False
                break


        # change the BACKGROUND of the cells in the row (below column indices)
        # only if entire row is empty
        if allEmpty:
            
            # MERGE CELLS in the row 
            ws.merge_cells( start_row=row, start_column=startColumn,
                            end_row=row,   end_column=max(colRange) )
            
            cell = ws.cell(row=row, column=startColumn)
            cell.fill = permEmptyCellStyle
            

    except Exception as e:
        msgText = handleErrorMsg('\nError while coloring the background of empty rows.', getTraceback(e))

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
        msgText = handleErrorMsg('\nError while searching for the last bold row at the beggining.', getTraceback(e))

    if msgText: print(msgText)

    return lastBoldRowAtBeggining