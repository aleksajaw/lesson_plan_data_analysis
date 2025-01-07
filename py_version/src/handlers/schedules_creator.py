from src.constants import weekdays, scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleListsExcelOwnersGrouped, excelEngineName, timeIndexes, dfRowNrAndTimeTuples, lessonAttrs
from src.utils import writeSortedObjOfDfsToExcel, autoFormatExcelCellSizes, removeLastEmptyRowsInDataFrames, createFileName, formatCellBackground
import pandas as pd
from pandas import ExcelWriter, DataFrame, RangeIndex
import numpy as np
import re



def createOtherScheduleExcelFiles(classSchedulesDfs):

    teacherSchedules = {}
    classroomSchedules = {}
    subjectSchedules = {}

    for className, classDf in classSchedulesDfs.items():
        #weekdays = classDf.columns.get_level_values(0).unique()

        buildNewOwnerScheduleBasedOnCol(teacherSchedules, classDf, 'teacher', className)
        buildNewOwnerScheduleBasedOnCol(classroomSchedules, classDf, 'classroom', className)
        buildNewOwnerScheduleBasedOnCol(subjectSchedules, classDf, 'subject', className)
    
    ownersLists = { 'teachers': list(teacherSchedules.keys()),
                    'classrooms': list(classroomSchedules.keys()),
                    'subjects': list(subjectSchedules.keys()) }

    groupedOwnersLists = writeGroupListsToExcelAndFormat(ownersLists)

    removeLastEmptyRowsInDataFrames([teacherSchedules,classroomSchedules, subjectSchedules])
    
    writeSortedObjOfDfsToExcel(teacherSchedules, 'teacher', scheduleExcelTeachersPath)
    writeSortedObjOfDfsToExcel(classroomSchedules, 'classroom', scheduleExcelClassroomsPath)
    writeSortedObjOfDfsToExcel(subjectSchedules, 'subject', scheduleExcelSubjectsPath)



def buildNewOwnerScheduleBasedOnCol(targetDict={}, baseDf=None, groupType='', newColValue='', newMainColKey='class'):

    if (isinstance(baseDf,DataFrame)) and (groupType!='') and (newColValue!=''):
        
        # main group in basic schedule is class
        groupTypes = {'teacher': 'nauczyciel',
                      'classroom': 'sala',
                      'subject': 'przedmiot'}
        
        # column name in timetable to be changed
        colToBeChanged = groupTypes[groupType]

        # make life (program) easier to understand:)
        newScheduleOwner = colToBeChanged

        # main column in basic schedule is subject
        newMainCol = {'class': 'klasa',
                      'teacher': 'nauczyciel',
                      'classroom': 'sala'}
        newMainColName = newMainCol[newMainColKey]
               
        # get the list of teachers/classrooms/subjects inside the timetable
        group = baseDf.xs(newScheduleOwner, axis=1, level=1).stack().unique()
        group = filterNumpyNdarray(group)

        if len(group):

            # loop for each teacher/classroom/subject
            for el in group:

                # copy for modification
                baseDfCopy = baseDf.copy().astype('object')
                # axis  =1 => columns
                #       =0 => index
                #
                # level of MultiIndex in column
                # level =1 => weekdays
                #       =2 => subject, teacher, classroom
                newScheduleOwnerTempData = baseDfCopy.xs(newScheduleOwner, axis=1, level=1)
                
                # get cells with value of specific el in group (teacher, classroom or subject)
                # e.g. KJ, 110, mat
                # not whole teacher, classroom, subject
                #
                # use data type (integer or other)
                try:
                    maskToFindDesiredPartOfLessons = newScheduleOwnerTempData == int(el)
                except:
                    maskToFindDesiredPartOfLessons = newScheduleOwnerTempData == el

                emptyValue = np.nan

                # use mask to get whole desired lessons
                # replace not matching whole rows with emptyValue
                # leave rows with any matches untouched
                elRows = baseDfCopy.where(maskToFindDesiredPartOfLessons.any(axis=1), emptyValue)

                # divide rows into weekdays
                # replace value with NaN for not matching days
                for day in weekdays:
                    # divide earlier mask to days 
                    elDayMask = maskToFindDesiredPartOfLessons[day]

                    # go through each day,
                    # ignore other days to make things easier
                    # replace not matching day cells with emptyValue
                    elRows[day] = elRows[day].where(elDayMask, emptyValue)


                # restrict loop actions to rows which match mask
                if not elRows.empty:

                    # change the column name and its value
                    elRows = elRows.rename(columns={colToBeChanged: newMainColName})

                    # asign
                    #   to the column "klasa" (old "nauczyciel", "przedmiot", "sala")
                    #   mapped values of the column "klasa" to className
                    # only if current value is not NaN in numeric arrays,
                    #   None or NaN in object arrays,
                    #   NaT in datetimelike
                    elRows.loc[:,(weekdays, newMainColName)] = elRows.loc[:, (weekdays, newMainColName)].map(lambda x: newColValue   if pd.notna(x)   else x)

                    elRows = elRows.groupby(level=[0,1]).first()
                    #indexLength = len(elRows.index)
                    #elRows.insert(loc=0, column=timeIndexes[1], value=lessonTimePeriods[:indexLength])

                    if el not in targetDict:
                        targetDict[str(el)] = elRows

                    else:
                        x = targetDict[str(el)].copy()
                        #y = x.combine_first(elRows)
                        #y = x.join(elRows)

                        targetDict[str(el)] = concatAndFilterScheduleDataFrames(x, elRows)



def filterNumpyNdarray(arr=np.ndarray, shouldConvertBack=False, elToDel=''):
    # convert values to string
    arrAsStr = arr.astype(str)
    # remove specific value
    sortedArr = np.sort( arrAsStr[ arrAsStr != elToDel] )

    return np.array([val for val in sortedArr])



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
        
    if len(msgText):
        print(msgText)



def createGroupsInListByPrefix(data=[], splitDelimeter = '-', replaceDelimeter = '.r'):
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
    
    return groupList



def createGroupsInListByFirstLetter(data=[]):
    return [item[0]   for item in data]



def createGroupsInListByNumbers(data=[]):
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
            match = re.match(r'([^a-zA-Z0-9]*0*[^a-zA-Z0-9]*)\d+', itemStr)
            if match:# '.', '_0', '0'
                item = match.group(1)
        
        groupsInList.append(item)
    
    return groupsInList



def createGroupsInListBy(groupName='', data=[]):
    result = []

    match groupName:
        case 'subjects':
            result = createGroupsInListByPrefix(data)
    
        case 'teachers':
            result = createGroupsInListByFirstLetter(data)

        case 'classrooms':
            result = createGroupsInListByNumbers(data)

    return result



def sortScheduleOwnersList(dataToSort=None):
    msgText = ''
    try:
        for key in dataToSort.keys():
            try:
                # sort by numbers (which are keys here) inside list elements,
                # especially for classroom names like _08, s1, 1, 100
                # moreover, it prevents missorting like 1, 10, 100, 2, 20, 200 :)
                #dataToEnter[key].sort( key = lambda x: int( re.findall(r'\d+', x)[0] ) )

                # also add sorting strings between the values with numbers like: 1, s1, st1, 2, _02, s2
                # so we will have s1, s2, st1, _02, 1, 2
                dataToSort[key].sort( key=lambda x: (
                                          # False values are treated as smaller,
                                          # so they will appear earlier in the sorted list
                                          # so at first sort by letters
                                          not x[0].isalpha(),
                                          # put values like _07 before digits
                                          # for easier grouping
                                          x.isdigit(),
                                          x.lower() if isinstance(x, str) and x[0].isalpha()
                                                    # sort by first digit in elements
                                                    else  int( re.findall( r'\d+', x )[0] )
                                                          if re.findall( r'\d+', x )
                                                          # if element does not have digit,
                                                          # use inf(inity) to move element
                                                          # at the end of the sorting here
                                                          else float('inf')
                                      )
                                    )
                # convert strings to integer, if it is possible
                dataToSort[key] = [int(x)   if x.isdigit()   else x   for x in dataToSort[key]]
            
            except:
                next
      
    except Exception as e:
        msgText = f'Error loading complete classes data: {e}'

    if msgText: print(msgText)
    return dataToSort



def createObjForDfRowsColoring(dfWithRowsToColor=DataFrame(), keyToGroupBy='group_No.', strToDelete='.'):
    msgText = ''
    try:
        df = dfWithRowsToColor
        # create the object for coloring the backgrounds of odd groups
        groupedRows = df.groupby(keyToGroupBy).apply(lambda
                                                      group: [  df.index.get_loc(x) + 1
                                                                for x in group.index ]
                                                  ).to_dict()
        groupedRowsFiltered = {}
        
        for key, value in groupedRows.items():
            convertedKey = key.replace(strToDelete,'')
            if convertedKey.isdigit() and int(convertedKey)%2!=0:
                groupedRowsFiltered[key] = value
        
        return {  'rowsToColor': [ item+1   for groupList in groupedRowsFiltered.values()
                                            for item in groupList ],
                  'columnsLength': len((df.reset_index()).columns) }
    

    except Exception as e:
        msgText = f'Error while writing group lists to excel sheets: {e}'
    
    if msgText: print(msgText)



def addBgToExcelSheetRowsBasedOnObj(writer=ExcelWriter, sheetsGroups={}):
    # add BACKGROUND to the (odd here) groups of the cells in worksheet 
    msgText = ''

    try:
        workbook = writer.book
        if workbook:
                            
            for sheetname in workbook.sheetnames:
                ws = workbook[sheetname]
                sheetBgRanges = sheetsGroups[sheetname]

                for grRow in sheetBgRanges['rowsToColor']:
                    for col in range(1, sheetBgRanges['columnsLength']+1):
                        cell = ws.cell(row=grRow, column=col)
                        formatCellBackground(cell, 'solid', 'f3f3f3', 'f3f3f3')
    
    
    except Exception as e:
        msgText = f'Error while adding background to the cells in the Excel sheet rows: {e}'
    
    print(msgText)



def writeGroupListsToExcel(excelPath=None, dataToEnter=None):
    msgText = ''
    dataToReturn = None

    if not excelPath:
        excelPath = createFileName

    try:
        dataToEnter = sortScheduleOwnersList(dataToEnter)
        objOfDfs = {}
        
        with ExcelWriter(excelPath, mode='w+', engine=excelEngineName) as writer:
            dataToEnter = {sheetName: dataToEnter[sheetName]   for sheetName in sorted(dataToEnter.keys())}

            sheetsGroups = {}

            # basic structure for the group list sheets
            for sheetName, sheetData in dataToEnter.items():
                
                namesBaseList = createGroupsInListBy(sheetName, sheetData)
                
                dfBase = {  'names_base': namesBaseList,
                            'names': sheetData }
                
                objOfDfs[sheetName] = DataFrame(dfBase)
                objOfDfs[sheetName]['names_No.'] = RangeIndex(start=1, stop=len(objOfDfs[sheetName])+1, step=1)
            
            
            # develop the structure of the worksheet objects
            for listName in objOfDfs:
                df = objOfDfs[listName]

                # indexes & their columns
                df['group_No.'] = (df.groupby('names_base', sort=False).ngroup() + 1).astype(str) + '.'
                df['names_in_group_No.'] = (df.groupby('names_base').cumcount() + 1).astype(str) + '.'
                
                df.set_index(keys=['group_No.', 'names_base', 'names_in_group_No.'], inplace=True)
                
                sheetsGroups[listName] = createObjForDfRowsColoring(df)
                
                objOfDfs[listName] = df
                df.to_excel(writer, sheet_name=listName, merge_cells=True)

            dataToReturn = objOfDfs
            addBgToExcelSheetRowsBasedOnObj(writer, sheetsGroups)

        msgText = f'Data loaded into the schedule Excel file: ' + excelPath.split('/')[-1]


    except Exception as e:
        msgText = f'Error while writing group lists to excel sheets: {e}'
    
    if msgText: print(msgText)

    return dataToReturn



def writeGroupListsToExcelAndFormat(groupLists={}):
    dataToReturn = None
    msgText = ''
    try:
        dataToReturn = writeGroupListsToExcel(scheduleListsExcelOwnersGrouped, groupLists)
        autoFormatExcelCellSizes(excelFilePath=scheduleListsExcelOwnersGrouped)

    except Exception as e:
        msgText = f'Error while writing and formatting the excel files for group lists: {e}'

    if msgText!='': print(msgText)

    return dataToReturn