from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleExcelClassesPath
from src.constants.schedule_structures_constants import excelMargin, excelFontSize, excelRangeStartCol, excelRangeStartRow
from pandas import ExcelWriter
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment as openpyxlAlignment
from openpyxl.styles import PatternFill as openpyxlPatternFill
from openpyxl.styles import Border as openpyxlBorder
from openpyxl.styles import Side as openpyxlSide
from openpyxl.styles import Font as openpyxlFont
from openpyxl.cell.cell import Cell as openpyxlCell
from openpyxl.cell.cell import MergedCell as openpyxlMergedCell
from openpyxl.utils import get_column_letter



def autoFormatScheduleExcel(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    autoFormatExcelCellSizes(workbook, excelFilePath)
    autoFormatScheduleExcelCellStyles(workbook, excelFilePath)



def autoFormatOverviewExcel(workbook=Workbook(), excelFilePath=''):
    autoFormatExcelCellSizes(workbook, excelFilePath)
    #autoFormatScheduleExcelCellStyles(workbook, excelFilePath)



def autoFormatScheduleExcelCellStyles(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath, shouldPrintSuccessMsg=False):
    from src.utils.excel_utils import getNrOfLastNonEmptyCellInCol
    msgText=''

    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(excelFilePath)

        if (workbook):
            for ws in workbook.worksheets:
                
                # column nr where the row indices end
                rowIndexesLastCol = excelMargin['col'] + 2

                # bold rows are for headers
                lastBoldRowAtBeggining = findLastBoldRowAtBeggining(ws, rowIndexesLastCol, excelRangeStartRow)

                # merge and format empty cells in the corner between the MultiIndexes
                mergeEmptyCellsAndFormat(ws, { 'startRow':  excelRangeStartRow,
                                                'startCol':  excelRangeStartCol,
                                                'endRow'  :  lastBoldRowAtBeggining,
                                                'endCol'  :  rowIndexesLastCol-1 } )
                
                # cells in the 1st two columns which row nr equals contentRowsStart
                # contains the names for the rows' MultiIndex
                contentFirstRow = lastBoldRowAtBeggining+1
                # col nr for the 1st cell for the 1st day
                daysFirstColList = rowIndexesLastCol+1

                totalColsRange = range(excelRangeStartCol, ws.max_column+1)
                # cells in the 2nd column contain part of rows indices & are less likely to be merged (for easier data analysis)
                totalRowsCount = lastBoldRowAtBeggining + getNrOfLastNonEmptyCellInCol(ws, minRow=contentFirstRow, col=rowIndexesLastCol)                    
                totalRowsRange = range(excelRangeStartRow, totalRowsCount+1)

                colorBgOfEmptyRow(ws, range(rowIndexesLastCol+1, ws.max_column+1), row=contentFirstRow, startColumn=daysFirstColList)


                # add MEDIUM RIGHT BORDERS
                # at the end of each important column and each day
                daysLastCol = sorted([mergedCellRange.max_col   for mergedCellRange in ws.merged_cells
                                                                   if mergedCellRange.min_row==mergedCellRange.max_row==excelRangeStartRow
                                                                      and   mergedCellRange.min_col > excelRangeStartCol+1])
                
                rowIndexesCols = list( range(excelRangeStartCol, rowIndexesLastCol+1) )
                colsWithRightMediumBorder = rowIndexesCols + daysLastCol

                if excelMargin['col']:
                    colsWithRightMediumBorder.insert(0, excelMargin['col'])
                
                standardDaySize = daysLastCol[0] - rowIndexesLastCol

                for col in colsWithRightMediumBorder:

                    for row1 in totalRowsRange:
                        cell = ws.cell(row=row1, column=col)
                        formatCellBorder(cell, right='medium')
                        
                        # add THIN SIDE BORDERS to the center column on days
                        # do not include the columns reserved for the rows indices
                        if rowIndexesLastCol < col:
                            rangeStartTemp = (col-standardDaySize)+1

                            for attrCol in range(rangeStartTemp, col):
                                cell = ws.cell(row=row1, column=attrCol)
                                formatCellBorder(cell, left='thin', right='thin')
                

                # add MEDIUM BOTTOM BORDERS
                # at the end of each index (for columns, for rows) and the entire schedule
                rowsWithBottomBorder = [lastBoldRowAtBeggining, contentFirstRow, totalRowsCount]

                if excelMargin['row']:
                    rowsWithBottomBorder.insert(0, excelMargin['row'])

                for row in rowsWithBottomBorder:
                    
                    # ignore long merged cell
                    totalColsRangeTemp = ( totalColsRange   if row!=contentFirstRow
                                                            else range(excelRangeStartCol, rowIndexesLastCol+1) )

                    for col in totalColsRangeTemp:
                        cell = ws.cell(row, column=col)
                        formatCellBorder(cell, bottom='medium')


                # add BACKGROUND
                # for the lessons with an odd numbers
                # and HAIR/THIN BORDERS

                for row in totalRowsRange:
                    
                    # fast checking if the row is in the specific merged range (for col A here)
                    merged = next(  ( r   for r in ws.merged_cells.ranges
                                             if r.min_col == excelRangeStartCol
                                                and   r.min_row <= row <= r.max_row ),
                                    None)

                    for col in totalColsRange:
                        cell = ws.cell(row, column=col)
                        # thinner ('HAIR') BORDER inside merged row
                        #if merged   and   merged.min_row != row:
                        #    topBorderStyle = 'hair'
                        # THIN BORDER for outer frame
                        #elif not cell.border.top.style:
                        topBorderStyle = 'thin'
                        formatCellBorder(cell, top=topBorderStyle)

                    # set LIGHT GREY BACKGROUND
                    # for the lessons with an odd number
                    rowNr = merged.min_row   if merged   else row
                    cellValue = ws.cell(row=rowNr, column=excelRangeStartCol).value

                    if isinstance(cellValue, int)   and   (cellValue & 1):
                        
                        for col in totalColsRange:
                            cell = ws.cell(row, column=col)
                            formatCellBackground(cell, fillType='solid', startColor='E5E5E5', endColor='E5E5E5')


        if shouldPrintSuccessMsg: msgText = '\nThe cell styles of the Excel file auto formatted.'

    except Exception as e:
        msgText = handleErrorMsg('\nError while formatting the cell styles in the Excel file.', getTraceback(e))
      
    if msgText: print(msgText)


    
def autoFormatExcelCellSizes(workbook=None, excelFilePath=scheduleExcelClassesPath, shouldPrintSuccessMsg=False):

    msgText = ''
    
    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(excelFilePath)

        if (workbook):
            for ws in workbook.worksheets:
                
                for col in range(excelRangeStartCol, ws.max_column+1):
                    max_length = 0
                    colLetter = get_column_letter(col)
                    
                    # loop through cells in column
                    for cell in ws[colLetter]:
                        if cell.row > excelMargin['row']:
                            
                            try:
                                cellValueLen = len(str(cell.value))

                                if cellValueLen > max_length:
                                    max_length = cellValueLen
                            except:
                                pass
                    
                    adjusted_width = (max_length + 2)
                    ws.column_dimensions[colLetter].width = adjusted_width

                for row in range(excelRangeStartRow, ws.max_row+1):
                    
                    for cell in ws[row]:
                        
                        cell.alignment = openpyxlAlignment(wrap_text=True, horizontal='center', vertical='center')
                        cell.font = openpyxlFont(size=excelFontSize, bold=cell.font.bold)
                    
                    ws.row_dimensions[row].height = excelFontSize * 1.3

            workbook.save(excelFilePath)

        if shouldPrintSuccessMsg: msgText = '\nThe cell sizes of the Excel file auto formatted.'

    except Exception as e:
        msgText = handleErrorMsg('\nError while formatting the cell sizes in the Excel file.', getTraceback(e))

    if msgText: print(msgText)



def formatCellBorder(cell=None, right='', left='', top='', bottom=''):
    msgText = ''

    if isinstance(cell, (openpyxlCell, openpyxlMergedCell)):
        try:
            currentBorder = cell.border
            defaultColor = '000000'
            borderStyle = { 'hair'  :  openpyxlSide(border_style='hair',    color=defaultColor),
                            'thin'  :  openpyxlSide(border_style='thin',    color=defaultColor),
                            'medium':  openpyxlSide(border_style='medium',  color=defaultColor),
                            'thick' :  openpyxlSide(border_style='thick',   color=defaultColor) }
            
            cell.border = openpyxlBorder( right = borderStyle[right]     if right    else currentBorder.right,
                                          left = borderStyle[left]       if left     else currentBorder.left,
                                          top = borderStyle[top]         if top      else currentBorder.top,
                                          bottom = borderStyle[bottom]   if bottom   else currentBorder.bottom )

        except Exception as e:
            msgText = handleErrorMsg('\nError while formatting the cell.', getTraceback(e))
            
    else:
        msgText = "\nError while formatting the cell: The value must be of type 'Cell'."
    
    if msgText: print(msgText)



def formatCellBackground(cell=None, fillType='', startColor='', endColor=''):
    msgText = ''

    if isinstance(cell, (openpyxlCell, openpyxlMergedCell)):
        try:
            if ( fillType=='solid'
                    and   isinstance(startColor, str)   and   startColor
                    and   isinstance(endColor, str)     and   endColor ):
                
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
                    
                    for col in range(excelRangeStartCol, ws.max_column+1):
                      
                        cell = ws.cell(row=grRow, column=col)
                        formatCellBackground(cell, 'solid', 'f3f3f3', 'f3f3f3')
    
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while adding background to the cells in the Excel sheet rows.', getTraceback(e))
    
    if msgText: print(msgText)


def mergeEmptyCellsAndFormat(ws=None, mergedCellObj={'startRow':int, 'startCol': int, 'endRow': int, 'endCol': int}):
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



def findLastBoldRowAtBeggining(ws, minCol=1, minRow=1):
    msgText=''

    try:
        lastBoldRowAtBeggining = -1
        rowTemp = minRow

        for col in ws.iter_cols(min_col=minCol, min_row=rowTemp):
          
            for cell in col:
                
                if cell.font   and   cell.font.bold:
                    lastBoldRowAtBeggining = cell.row
                    rowTemp = lastBoldRowAtBeggining
                else:
                    break
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while searching for the last bold row at the beggining.', getTraceback(e))

    if msgText: print(msgText)

    return lastBoldRowAtBeggining