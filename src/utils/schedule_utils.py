from error_utils import handleErrorMsg, getTraceback
from src.constants.schedule_structures_constants import weekdays, timeIndexNames, dayAndAttrNames, dfColWeekDayNameTuples4el, dfColWeekDayNameTuples5el, dfColWeekDayNameArrays4el, dfColWeekDayNameArrays5el, lessonTimePeriods
from converters_utils import correctDfContent
from excel_utils import dropnaInDfByAxis
import pandas as pd
from pandas import DataFrame
import numpy as np
import re



def concatAndFilterScheduleDataFrames(df1, df2, addNewCol=False, newColName=None, newColVal=None):
    msgText = ''
    newDf = None

    try:
        #if df1 is None:
        #    df1 = DataFrame
        #if df2 is None:
        #    df2 = DataFrame
        
        # two lines below prevents FutureWarning:
        #   The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.
        #   In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes.
        #   To retain the old behavior, exclude the relevant entries before the concat operation.
        #df1 = dropnaInDfByAxis(df1, 1)
        df2 = dropnaInDfByAxis(df2, 1)
        newDf = pd.concat([df1, df2], sort=False).sort_index(level=0)
        
        newDf = filterAndConvertScheduleDataFrames(newDf, addNewCol, newColName, newColVal)


    except Exception as e:
        msgText = handleErrorMsg('\nError while concatenating and filter the schedule Data Frames.', getTraceback(e))

    if msgText: print(msgText)

    return newDf
        


def filterAndConvertScheduleDataFrames(df, addNewCol=False, newColName=None, newColVal=None):
    newDf = []
    msgText = ''
    
    try:
        #if df is None:
        #    df = DataFrame
        
        rowsFiltered = []

        prepareNewColVal = addNewCol   and   newColName   and   newColVal

        colDayNameTuples = dfColWeekDayNameTuples5el   if addNewCol   else df.columns


        if len(colDayNameTuples) != len(df.columns):
            # Reduce some columns in colDayNameTuples
            # if they are not going to be added   and   do not exist in the current DataFrame's columns.
            # For example, some schedules may not have 'teacher' column.
            colsDiff = [ item   for item in colDayNameTuples
                                if item[1] not in df.columns.get_level_values(1).unique()
                                   and   item[1] != newColName ]
            
            colDayNameTuples = [colTuple   for colTuple in colDayNameTuples
                                           if colTuple not in colsDiff]


        #colDayNameArrays = dfColWeekDayNameArrays5el   if addNewCol   else dfColWeekDayNameArrays4el
        timeKey1 = timeIndexNames[0]
        timeKey2 = timeIndexNames[1]

        # iterate through rows (time indices)
        for (lessonNr, time), rowFrame in df.groupby(timeIndexNames, sort=False):
            singleRowBase = {}
            singleRowBase[timeKey1] = int(lessonNr)
            singleRowBase[timeKey2] = time

            innerRows = []

            for col in df.columns:
                booleanMask = rowFrame[col] != ''
                nonEmptyValues = [x   for x in rowFrame[col][booleanMask]   if pd.notna(x)]

                if nonEmptyValues:
                    for index, value in enumerate(nonEmptyValues):
                        
                        if len(innerRows) < len(nonEmptyValues):
                            innerRows.append(singleRowBase.copy())

                            currRowNr = int( singleRowBase[timeKey1] )


                        # add empty rows to avoid tables that do not start from row nr 1
                        if ( (       rowsFiltered   and   (int(rowsFiltered[-1][timeKey1]) < currRowNr-1) )
                            or ( not rowsFiltered   and   1 < currRowNr) ):

                            lastFilteredRowNr = ( int( rowsFiltered[-1][timeKey1] )   if len(rowsFiltered)
                                                                                      else 0 )

                            missingNrs = list( range( lastFilteredRowNr+1, currRowNr ) )
                            
                            while len(missingNrs):
                                desiredNr = missingNrs[0]
                                singleRowTemp = {}
                                
                                for lessonAttr in colDayNameTuples:
                                    singleRowTemp[lessonAttr] = np.nan
                                
                                desiredPreviousTime = lessonTimePeriods[ desiredNr-1 ]
                                singleRowTemp[timeKey1] = desiredNr
                                singleRowTemp[timeKey2] = desiredPreviousTime
                                rowsFiltered.append( singleRowTemp.copy() )
                                missingNrs = missingNrs[1:]   if missingNrs   else []
                                singleRowTemp = {}


                        innerRows[index][col] = value


                    if prepareNewColVal:
                        for index, r in enumerate(innerRows):
                            doesRowHaveDay = col[0] in [ rowKey[0]   for rowKey in r.keys() ]
                            doesDayHaveInnerCol = (col[0], newColName) in r

                            if doesRowHaveDay   and   not doesDayHaveInnerCol:
                                innerRows[index][(col[0], newColName)] = newColVal

            for r in innerRows:
                rowsFiltered.append(r.copy())

        if addNewCol   or   ( len(df.columns.get_level_values(0).unique()) < len(weekdays) ):

            columnsVal = pd.MultiIndex.from_tuples(colDayNameTuples, names=dayAndAttrNames)
            #columnsVal = pd.MultiIndex.from_arrays(arrays=colDayNameArrays, names=dayAndAttrNames)
        
        else:
            columnsVal = df.columns

        newDf = correctDfContent( DataFrame(rowsFiltered).set_index(timeIndexNames)
                                                         .reindex(columns=columnsVal) )

    except Exception as e:
        msgText = handleErrorMsg('\nError while filtering and converting schedule Data Frames for Excel worksheet.', getTraceback(e))
        
    if msgText: print(msgText)
    
    return newDf



# 'r' comes from 'rozszerzony/a' which means the subject is extendend like 'advanced English'
def createGroupsInListByPrefix(data, splitDelimiter = '-', replaceDelimiters = ['.r', 'r_']):
    msgText = ''

    try:
        groupList = []

        # retain only the part before the first '-' and remove '.r' and 'r_'
        for item in data:
            itemAdded = False

            if isinstance(item, str):
                item1stEl = str(item).split(splitDelimiter)[0]

                for repDeli in replaceDelimiters:
                    itemAdded = False

                    if repDeli in item1stEl:
                        
                        # e.g., delimiter to replace + subject name   =>   'r_matematyka'
                        if item1stEl.startswith(repDeli):
                            groupList.append( item1stEl.replace(repDeli, '', 1) )
                            itemAdded = True
                            break
                        
                        # e.g., delimiter to replace + subject name   =>   'matematyka.r'
                        elif item1stEl.endswith(repDeli):
                            deliIndex = item1stEl.rfind(repDeli)

                            if deliIndex != -1:
                                groupList.append( item1stEl[:deliIndex] )
                                itemAdded = True
                                break
                
                
                if not itemAdded:
                    groupList.append(item1stEl)
            
            else:
                groupList.append(item)
        
        # group elements by names starting with the same prefix
        for i in range(2, len(groupList)):
            
            el = groupList[i]
            previousEl = groupList[i-1]
            doesElStartSameAsPrevious = el.startswith( previousEl )

            if doesElStartSameAsPrevious:
                groupList[i] = previousEl
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while creating groups in list by prefix.', getTraceback(e))
    
    if msgText: print(msgText)
    
    return groupList



def createGroupsInListByFirstLetter(data):
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
        msgText = handleErrorMsg('\nError while creating groups in list by first letter.', getTraceback(e))
    
    if msgText: print(msgText)



def createGroupsInListByStringAndNumbers(data, optionalPartInNrPrefix='0'):
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
                # matches e.g. '.9', '_09', '09' or '9'
                pattern = r'([^a-zA-Z0-9]*' + re.escape(optionalPartInNrPrefix) + r'*[^a-zA-Z0-9]*)\d+'
                match = re.match(pattern, itemStr)
                
                if match:
                    # '.', '_0', '0'   only if   optionalPartInNrPrefix = 0
                    item = match.group(1)
            
            groupsInList.append(item)
        
        return groupsInList
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while creating groups in list by string and numbers.', getTraceback(e))
    
    if msgText: print(msgText)



def createGroupsInListByNumbers(data):
    msgText=''

    try:
        groupsInList = []
        for item in data:
            itemStr = str(item)
            
            # matches numbers
            pattern = r'\d+'
            match = re.match(pattern, itemStr)
                
            if match:
                item = int(match.group(0))
          
            groupsInList.append(item)
        
        return groupsInList
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while creating groups in list by numbers.', getTraceback(e))
    
    if msgText: print(msgText)



def createGroupsInListBy(listName, data):
    result = []
    msgText = ''
    groupingKey = ''

    try:
        match listName:
            case 'subjects':
                result = createGroupsInListByPrefix(data)
                groupingKey = 'prefix'
        
            case 'teachers':
                result = createGroupsInListByFirstLetter(data)
                groupingKey = 'first letter'

            case 'classrooms':
                result = createGroupsInListByStringAndNumbers(data)
                groupingKey = 'string and numbers'

            case 'classes':
                result = createGroupsInListByNumbers(data)
                groupingKey = 'numbers'


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while creating groups in the {listName}\' list by {groupingKey}.', getTraceback(e))
    
    if msgText: print(msgText)

    return result