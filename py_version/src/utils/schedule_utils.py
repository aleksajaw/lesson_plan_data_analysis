from src.constants import scheduleExcelClassesPath, weekdays, lessonAttrs
from src.utils import autoFormatExcelCellSizes, formatCellBackground, formatCellBorder
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill as openpyxlPatternFill



def autoFormatScheduleExcel(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):
    autoFormatExcelCellSizes(workbook, excelFilePath)
    autoFormatScheduleExcelCellsStyle(workbook, excelFilePath)



def autoFormatScheduleExcelCellsStyle(workbook=Workbook(), excelFilePath=scheduleExcelClassesPath):

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
                lenOfLessonAttrs = len(lessonAttrs)
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
        print('Error while formatting the Excel file:', e)