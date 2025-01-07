import os
import sys
import subprocess
from src.constants import outputsPath



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