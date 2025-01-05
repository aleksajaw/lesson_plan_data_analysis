import os
import sys
import subprocess
from constants import scheduleExcelPath, outputsPath
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment as openpyxlAlignment
from openpyxl.styles import PatternFill as openpyxlPatternFill
from openpyxl.styles import Border as openpyxlBorder
from openpyxl.styles import Side as openpyxlSide
from openpyxl.cell.cell import Cell as openpyxlCell
from openpyxl.cell.cell import MergedCell as openpyxlMergedCell
from openpyxl.utils import column_index_from_string, get_column_letter



def doesFileExist(filePath='', shouldPrintMsg=False):
    msgText = f'File   {os.path.basename(filePath)}   '
    doesFileExistBool = bool (os.path.isfile(filePath))

    if doesFileExistBool:
        msgText += 'exists.'
    else:
        msgText += 'does not exist.'

    if shouldPrintMsg:
        print(msgText)

    return doesFileExistBool



def compareAndUpdateFile(filePath='', dataToCompare=''):
    
    isFileChanged = False
    if bool(filePath) and bool(dataToCompare):
        msgText = ''

        try:
            with open(file=filePath, mode="r+") as file:
                #file.seek(0)
                fileContent = file.read()
                if str(fileContent) != str(dataToCompare):
                    file.seek(0)
                    file.write(dataToCompare)
                    # make sure to delete old redundant value
                    file.truncate()
                    msgText = f'\nFile   {os.path.basename(filePath)}   updated with new data.'
                    isFileChanged = True
                    
                else:
                    msgText = f'\nNothing to be updated in file   {os.path.basename(filePath)}.'

                file.close()
                print(msgText)

        except FileNotFoundError as e:
            
            with open(filePath, 'w') as file:
              file.write(dataToCompare)
              file.close()

              print(f'File   {os.path.basename(filePath)}   not found. Created a new file and complete it with data.')
        
        except Exception as e:
            print('Error while comparing and updating file content: ', e)


        return isFileChanged



def autoFormatExcelFile(workbook=Workbook(), excelFilePath=scheduleExcelPath):
    autoFormatExcelFileCellSizes(workbook, excelFilePath)
    autoFormatExcelFileCellsStyle(workbook, excelFilePath)



def autoFormatExcelFileCellSizes(workbook=Workbook(), excelFilePath=scheduleExcelPath):
    from excel_utils import get1stNotMergedCell

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
                for rowNr in range(1,len(rowsLines)+1):
                    ws.row_dimensions[rowNr].height = rowsLines[rowNr] * defaultFontSize * 1.25

            workbook.save(excelFilePath)

    except Exception as e:
        print('Error while formatting the Excel file:', e)



def formatCellBorder(cell=None, right='', left='', top='', bottom=''):
    if isinstance(cell, (openpyxlCell, openpyxlMergedCell)):
        try:
            currentBorder = cell.border
            borderStyle = { 'solid': openpyxlSide(border_style="thin", color="000000")}
            cell.border = openpyxlBorder( right = borderStyle[right]   if right   else currentBorder.right,
                                          left = borderStyle[left]   if left   else currentBorder.left,
                                          top = borderStyle[top]   if top   else currentBorder.top,
                                          bottom = borderStyle[bottom]   if bottom   else currentBorder.bottom )

        except Exception as e:
            print('Error while formatting the cell:', e)
            
    else:
        print("Error while formatting the cell: The value must be of type 'Cell'.")



def autoFormatExcelFileCellsStyle(workbook=Workbook(), excelFilePath=scheduleExcelPath):
    from constants import weekdays, lessonAttrs

    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(excelFilePath)

        if (workbook):
            for ws in workbook.worksheets:
                
                permEmptyCellStyle = openpyxlPatternFill(fill_type='lightTrellis')
                
                # merge and format empty cells in the corner between the MultiIndexes
                ws.merge_cells('A1:B2')
                ws['A1'].fill = permEmptyCellStyle

                rowNrStart = 3
                rowsCount = 0

                # count rows in the 1st and the 2nd column,
                # cells there are less likely to be merged (for easier data analysis)
                for row in ws.iter_rows(min_row=rowNrStart, min_col=1, max_col=2):
                    if row[1].value is not None:
                        rowsCount += 1
                    else:
                        break
                

                totalRowsCount = rowNrStart-1 + rowsCount
                colNrIndexesEnd = 2
                colNrDaysStart = 3
                lenOfWeekdays = len(weekdays)
                lenOfLessonAttrs = len(lessonAttrs)
                colNrEnd = colNrDaysStart-1 + lenOfWeekdays * lenOfLessonAttrs
                

                # row with number rowNrStart in the 1st two columns
                # contains the names for the rows' MultiIndex
                allEmpty = True 

                # check if the cells in the 1st row below column indexes are empty
                for col in range(colNrDaysStart, colNrEnd+1):
                    if ws.cell(row=rowNrStart, column=col).value is not None:
                        allEmpty = False
                        break


                # change the BACKGROUND of the cells in the row
                # if entire row below column indexes is empty
                if allEmpty:
                    
                    # MERGE CELLS in the row 
                    ws.merge_cells( start_row=rowNrStart, start_column=colNrDaysStart,
                                    end_row=rowNrStart, end_column=colNrEnd )
                    cell = ws.cell(row=rowNrStart, column=colNrDaysStart)
                    cell.fill = permEmptyCellStyle

                    startCoordinate = f'{get_column_letter(colNrDaysStart)}{rowNrStart}'
                    endCoordinate = f'{get_column_letter(colNrEnd)}{rowNrStart}'
                    
                    for cell in ws[startCoordinate:endCoordinate][0]:
                        formatCellBorder(cell, bottom='solid')


                # add a RIGHT BORDER at the end of each day
                for daysCounter in range(1, 1+lenOfWeekdays):
                    colNr = colNrIndexesEnd + (daysCounter * lenOfLessonAttrs)

                    newRowStart = rowNrStart   if daysCounter == lenOfWeekdays   else rowNrStart + 1

                    for rowNr in range(newRowStart, totalRowsCount+1):
                        cell = ws.cell(row=rowNr, column=colNr)
                        formatCellBorder(cell, right = 'solid')
                

                # add the BOTTOM BORDER for the schedule
                for col in range(colNrDaysStart, colNrEnd+1):
                    cell = ws.cell(row=totalRowsCount, column=col)
                    formatCellBorder(cell, bottom='solid')

    except Exception as e:
        print('Error while formatting the Excel file:', e)



def findFileGroup(desiredBase='', desiredExt='', getSplitFileName=False):
    from collections import defaultdict
    group = defaultdict(list)

    for fileName in os.listdir(outputsPath):
        basename, ext = splitFileName(fileName)

        if desiredExt in ('', '*', ext) and desiredBase in ('', '*', basename):
            el = (basename, ext)   if getSplitFileName   else fileName

            group.append(el)

    return group



def splitFileName(fileName=''):
    basename, ext = ('', '')

    if fileName:
        basename, ext = os.path.splitext(fileName)

    return (basename, ext)



def findLastFileInGroup(desiredBase='', desiredExt='', getSplitFileName=False):
    filesList = findFileGroup(desiredBase, desiredExt, getSplitFileName)

    return filesList[-1]   if len(filesList)   else None



def getFileMarker(fileName='', separator='-'):
    if separator in fileName:
        return removeEmptyStrFromArr(fileName.split(separator))[-1]

    else:
        return fileName



def createFileName(basicFileName = 'schedule', fileExt = 'xlsx', separator = '-'):
    fileNameParts = findLastFileInGroup(basicFileName, fileExt, True)
    difference = ''

    # If there aren't any very similar files in the folder,
    # use the basic file name.
    finalFileName = basicFileName

    # Otherwise, expand the basic file name.
    if len(fileNameParts):
        difference = findFileNameDifference(fileNameParts[0])

        # But still - only if it is very similar file name.
        # For example basicFileName + separator + 1.fileExt
        hasSeparator = separator in difference
        if hasSeparator:
            tempDifference = getFileMarker(difference, separator)
            
            if len(tempDifference) == 1 and type(tempDifference) == int:
                difference = tempDifference+1
        
        else:
            difference = 1

        finalFileName+= separator + difference


    return finalFileName + '.' + fileExt

        

def findFileNameDifference(fileName='', fileNameToBeCompared=''):
    from excel_utils import convertDigitInStrToInt

    difference = ''
    nameToRemove=''
    isReplacementRequired = False

    if fileNameToBeCompared in fileName:
        isReplacementRequired = True


    difference = fileName   if not isReplacementRequired   else fileNameToBeCompared
    nameToRemove = fileNameToBeCompared   if not isReplacementRequired   else fileName

    difference.replace(nameToRemove, '')

    return convertDigitInStrToInt(difference)



def removeEmptyStrFromArr(arr=[]):
    return [el   for el in arr   if el!='']



def openFileWithDefApp(filePath=''):

    if filePath!='' and not doesFileExist(filePath, True):
        return

    try:
        # Windows
        if sys.platform == "win32":
            subprocess.run(['start', '', filePath], shell=True)

        # macOS
        elif sys.platform == "darwin":
            subprocess.run(['open', filePath])

        # Linux / Unix-like
        else:
            subprocess.run(['xdg-open', file_path])

    except Exception as e:
        print(f"Failed to open file for User: {e}")