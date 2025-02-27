import os
import sys
import subprocess
import json
from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import documentsPath
from src.constants.conversion_constants import JSONIndentValue, draftSheetName



def doesDirExist(dirPath, shouldPrintMsg=False):
    msgText = f'\nDirectory   {os.path.basename(dirPath)}   '
    doesDirExistBool = bool( os.path.isdir(dirPath) )

    msgText += ( 'exists.'   if doesDirExistBool
                             else 'does not exist.' )
    
    if shouldPrintMsg: print(msgText)

    return doesDirExistBool



def createDirIfNecessary(dirPath):
    if dirPath   and   not doesDirExist(dirPath):
        os.mkdir(dirPath)



def listSubdirectories(basePath):
    excludedDirs = ['.old']
    dirList = []

    try:
        for dirName in os.listdir(basePath):
            isDir = os.path.isdir( os.path.join(basePath, dirName) )
            
            if isDir   and   dirName not in excludedDirs:
                dirList.append(dirName)
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while getting the list of the subdirectories for {os.path.basename(basePath)}.', getTraceback(e))
        
        if msgText: print(msgText)
    
    return dirList



def doesFileExist(filePath, shouldPrintMsg=False):
    msgText = f'\nFile   {os.path.basename(filePath)}   '
    doesFileExistBool = bool( os.path.isfile(filePath) )

    msgText += ( 'exists.'   if doesFileExistBool
                             else 'does not exist.' )
    
    if shouldPrintMsg   or   not doesFileExistBool: print(msgText)

    return doesFileExistBool



def writeDataToFile(filePath, dataToEnter):
    msgText=''
    isSuccess=False

    try:
        with open(filePath, 'w') as file:
            file.write(dataToEnter)
            file.close()
        
        msgText = f'\nThe data has been loaded into the {(os.path.splitext(filePath)[1][1:]).upper()} file   {os.path.basename(filePath)}.'

        isSuccess = True

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while writing data to the file   {os.path.basename(filePath)}.', getTraceback(e))

    if msgText: print(msgText)

    return isSuccess



def compareAndUpdateFile(filePath, dataToCompare):
    msgText = ''
    isFileChanged = False
    #if bool(filePath) and bool(dataToCompare):

    try:
        with open(file=filePath, mode="r+") as file:
            #file.seek(0)
            fileContent = file.read()

            if str(fileContent) != str(dataToCompare):
                try:
                    fileContentAsDict = dict(json.loads(fileContent))
                    dataToCompareAsDict = dict(json.loads(dataToCompare))
                    
                    commonKeys = list(set(fileContentAsDict) & set(dataToCompareAsDict))
                    updatedFileContent = fileContentAsDict

                    if len(commonKeys):
                        for commonKey in commonKeys:
                            if fileContentAsDict[commonKey] != dataToCompareAsDict[commonKey]:
                                updatedFileContent[commonKey] = dataToCompareAsDict[commonKey]
                                if not isFileChanged:
                                    isFileChanged = True
                    
                    differentKeys = list(set(dataToCompareAsDict) - set(fileContentAsDict))

                    if len(differentKeys):
                        for key in differentKeys:
                            updatedFileContent[key] = dataToCompareAsDict[key]
                            if not isFileChanged:
                                isFileChanged = True
                    
                    if draftSheetName in updatedFileContent.keys()   and   draftSheetName not in commonKeys+differentKeys:
                        del updatedFileContent[draftSheetName]
                        if not isFileChanged:
                            isFileChanged = True
                    
                    if isFileChanged:
                        file.seek(0)
                        file.write(json.dumps(updatedFileContent, indent=JSONIndentValue))

                except Exception as e:
                    file.seek(0)
                    file.write(dataToCompare)
                    if not isFileChanged:
                        isFileChanged = True

                    # make sure to delete old redundant value
                    file.truncate()
                
            if isFileChanged:
                msgText = f'\nUpdated with new data the {(os.path.splitext(filePath)[1][1:]).upper()} file   {os.path.basename(filePath)}.'
                
            else:
                msgText = f'\nNothing to be updated in the {(os.path.splitext(filePath)[1][1:]).upper()} file   {os.path.basename(filePath)}.'

            file.close()

    except FileNotFoundError as e:
        isFileChanged = writeDataToFile(filePath, dataToCompare)
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while comparing and updating the file content.', getTraceback(e))

    if msgText: print(msgText)

    return isFileChanged



def findFileGroup(desiredBase, desiredExt, getSplitFileName=False, dirPath=documentsPath):
    from collections import defaultdict
    group = defaultdict(list)

    for fileName in os.listdir(dirPath):
        basename, ext = splitFileName(fileName)

        if desiredExt in ('', '*', ext)   and   desiredBase in ('', '*', basename):
            el = (basename, ext)   if getSplitFileName   else fileName

            group.append(el)

    return group



def splitFileName(fileName):
    basename, ext = ('', '')

    if fileName:
        basename, ext = os.path.splitext(fileName)

    return (basename, ext)



def findLastFileInGroup(desiredBase, desiredExt, getSplitFileName=False):
    filesList = findFileGroup(desiredBase, desiredExt, getSplitFileName)

    return filesList[-1]   if len(filesList)   else None



def getFileMarker(fileName, separator='-'):
    if separator in fileName:
        return removeEmptyStrFromArr(fileName.split(separator))[-1]

    else:
        return fileName



def createFileNameWithNr(basicFileName='schedule', fileExt = 'xlsx', separator = '-'):
    fileNameParts = findLastFileInGroup(basicFileName, fileExt, True)
    difference = ''

    # If there aren't any very similar files in the dir,
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
            
            if len(tempDifference) == 1   and   isinstance(tempDifference, int):
                difference = tempDifference+1
        
        else:
            difference = 1

        finalFileName += separator + difference


    return finalFileName + '.' + fileExt



def createFileNameWithDateTime(fileNameBase='log', fileExt='txt', mainSeparator='_', innerDateSeparator='-'):
    import datetime

    currTime = datetime.datetime.now()
    dateStr = '%Y' + innerDateSeparator + '%m' + innerDateSeparator + '%d' + mainSeparator + '%H'
    timeStr = '%M' + innerDateSeparator + '%S'
    currTimeFormatted = currTime.strftime( dateStr + innerDateSeparator + timeStr)

    fileName = currTimeFormatted + mainSeparator 
    fileName += fileNameBase or 'log'
    fileName += '.' + (fileExt or 'txt') 

    return fileName

        

def findFileNameDifference(fileName, fileNameToBeCompared):
    from src.utils.excel_utils import convertDigitInStrToInt

    difference = ''
    nameToRemove=''
    isReplacementRequired = False

    if fileNameToBeCompared in fileName:
        isReplacementRequired = True


    difference   = fileName               if not isReplacementRequired   else fileNameToBeCompared
    nameToRemove = fileNameToBeCompared   if not isReplacementRequired   else fileName

    difference.replace(nameToRemove, '')

    return convertDigitInStrToInt(difference)



def removeEmptyStrFromArr(arr=[]):
    return [el   for el in arr   if el]



def openFileWithDefApp(filePath):

    if filePath   and   not doesFileExist(filePath):
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
        print(f"Failed to open file for User: {getTraceback(e)}")



def extendFilePathWithCurrSchoolTitle(filePath):
    from src.handlers.scraper_saver import currSchoolWebInfo

    return extendFileNameInPath(filePath, '_' + currSchoolWebInfo['title'])   if currSchoolWebInfo['title']   else filePath



def extendFileNameInPath(filePath, strToAdd):
    baseName, ext = os.path.splitext(filePath)
    newBaseName = baseName + strToAdd
    newFileName = newBaseName + ext
    dirPath = os.path.dirname(filePath)

    return os.path.join(dirPath, newFileName)



def extendFileNameWithCurrSchoolTitle(fileName):
    from src.handlers.scraper_saver import currSchoolWebInfo

    return extendFileName(fileName, '_' + currSchoolWebInfo['title'])   if currSchoolWebInfo['title']   else fileName



def extendFileName(fileName, strToAdd):
    baseName, ext = os.path.splitext(fileName)
    newBaseName = baseName + strToAdd
    newFileName = newBaseName + ext

    return newFileName