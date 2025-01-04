import os
import sys
import subprocess
from constants import scheduleExcelPath, outputsPath
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment as openpyxlAlignment
from openpyxl.utils import column_index_from_string



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



def autoFormatExcelFileCellSizes(workbook=Workbook()):
    from excel_utils import get1stNotMergedCell

    try:
        if not isinstance(workbook, Workbook):
            workbook = load_workbook(scheduleExcelPath)

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


                    ws.column_dimensions[colLetter].width = colsLength[colIndex] + 1


            workbook.save(scheduleExcelPath)


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