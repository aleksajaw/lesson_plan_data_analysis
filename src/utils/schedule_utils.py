from error_utils import handleErrorMsg, getTraceback
from src.constants.schedule_structures_constants import weekdays, timeIndexNames, dayAndAttrNames, dfColWeekDayNamesTuples4el, dfColWeekDayNamesTuples5el, lessonTimePeriods
from excel_utils import dropnaInDfByAxis
import pandas as pd
from pandas import DataFrame
import numpy as np
import re



def concatAndFilterScheduleDataFrames(el1=None, el2=None, addNewCol=False, newColName='', newColVal=''):
    msgText = ''
    newDf = None

    try:
        # two lines below prevents FutureWarning:
        #   The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.
        #   In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes.
        #   To retain the old behavior, exclude the relevant entries before the concat operation.
        #el1 = dropnaInDfByAxis(el1, 1)
        if isinstance(el1, DataFrame)   and   isinstance(el2, DataFrame):
            el2 = dropnaInDfByAxis(el2, 1)
            newDf = pd.concat([el1, el2], sort=False).reset_index()
            newDf.set_index(keys=timeIndexNames, inplace=True)
            newDf = newDf.sort_index(level=0)
        else:
            newDf = el1 or el2
        newDf = filterAndConvertScheduleDataFrames(newDf, addNewCol, newColName, newColVal)


    except Exception as e:
        msgText = handleErrorMsg('\nError while concatenating and filter the schedule Data Frames.', getTraceback(e))

    if msgText: print(msgText)

    return newDf
        


def filterAndConvertScheduleDataFrames(df=None, addNewCol=False, newColName='', newColVal=''):
    newDfFiltered = []
    msgText = ''
    
    try:
        newDf = df.copy()
        #print('\nnewDf.index ', list(newDf.index))
        rowsFiltered = []

        prepareNewColVal = addNewCol   and   newColName   and   newColVal

        colDayNamesTuples = dfColWeekDayNamesTuples5el   if addNewCol   else dfColWeekDayNamesTuples4el
        timeKey1 = timeIndexNames[0]
        timeKey2 = timeIndexNames[1]

        # iterate through rows (time indices)
        for (lessonNr, time), row in newDf.groupby(timeIndexNames, sort=False):
            #print(lessonNr)
            #print(time)
            #print(row)
            rowFrame = row
            singleRowBase = {}
            singleRowBase[timeKey1] = int(lessonNr)
            singleRowBase[timeKey2] = time

            innerRows = []

            for col in newDf.columns:
                #print(rowFrame.keys())
                #print(col)
                booleanMask = rowFrame[col] != ''
                nonEmptyValues = [x for x in rowFrame[col][booleanMask] if pd.notna(x)]
                #print(nonEmptyValues)

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
                                #print([r[timeKey1]   for r in rowsFiltered])
                                #print((singleRowBase[timeKey1]))
                                #print(missingNrs)
                                desiredNr = missingNrs[0]
                                singleRowTemp = {}
                                
                                for lessonAttr in colDayNamesTuples:
                                    singleRowTemp[lessonAttr] = np.nan
                                
                                desiredPreviousTime = lessonTimePeriods[ desiredNr-1 ]
                                singleRowTemp[timeKey1] = desiredNr
                                singleRowTemp[timeKey2] = desiredPreviousTime
                                rowsFiltered.append(singleRowTemp.copy())
                                missingNrs = missingNrs[1:]   if missingNrs   else []
                                singleRowTemp = {}


                        innerRows[index][col] = value
                        #print('innerRows[index]:', innerRows[index])


                    if prepareNewColVal:
                        for index, r in enumerate(innerRows):
                            doesRowHaveDay = col[0] in [ rowKey[0]   for rowKey in r.keys() ]
                            doesDayHaveInnerCol = (col[0], newColName) in r

                            if doesRowHaveDay   and   not doesDayHaveInnerCol:
                                innerRows[index][(col[0], newColName)] = (newColVal   if not newColVal.isdigit()
                                                                                      else int(newColVal))

            for r in innerRows:
                rowsFiltered.append(r.copy())


        if addNewCol or ( len(newDf.columns.get_level_values(0).unique()) < len(weekdays) ):

            columnsVal = pd.MultiIndex.from_tuples(colDayNamesTuples, names=dayAndAttrNames)
        
        else:
            columnsVal = newDf.columns

        #print('rowsFiltered indexy ', [row[timeKey1]   for row in rowsFiltered])
        newDfFiltered = pd.DataFrame(rowsFiltered)
        #print('newDfFiltered.index ', newDfFiltered.index)
        newDfFiltered = newDfFiltered.reset_index()
        newDfFiltered.set_index(keys=timeIndexNames, inplace=True)
        #print('newDfFiltered.index ', newDfFiltered.index)
        newDfFiltered = newDfFiltered.reindex(columns=columnsVal, fill_value=np.nan)

    except Exception as e:
        msgText = handleErrorMsg('\nError while filter and convert schedule Data Frames for Excel worksheet.', getTraceback(e))
        
    if msgText: print(msgText)
    
    return newDfFiltered



# 'r' comes from 'rozszerzony/a' which means the subject is extendend like 'advanced English'
def createGroupsInListByPrefix(data=[], splitDelimiter = '-', replaceDelimiters = ['.r', 'r_']):
    msgText = ''

    try:
        groupList = []

        # only leave the part before the first '-' and cut '.r' and 'r_' out
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
        msgText = handleErrorMsg('\nError while creating groups in list by first letter.', getTraceback(e))
    
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
        msgText = handleErrorMsg('\nError while creating groups in list by numbers.', getTraceback(e))
    
    if msgText: print(msgText)



def createGroupsInListBy(listName='', data=[]):
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
                result = createGroupsInListByNumbers(data)
                groupingKey = 'numbers'


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while creating groups in the {listName}\' list by {groupingKey}.', getTraceback(e))
    
    if msgText: print(msgText)

    return result