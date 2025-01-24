from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants import weekdays, scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelTeachersGroupedPath, scheduleExcelClassroomsGroupedPath, scheduleExcelSubjectsGroupedPath, scheduleListsExcelOwnersGroupedPath, excelEngineName, scheduleTeachersGroupedDfsJSONPath, scheduleClassroomsGroupedDfsJSONPath, scheduleSubjectsGroupedDfsJSONPath
from src.utils import writerForWriteObjOfDfsToExcel, writeObjOfDfsToJSON, autoFormatExcelCellSizes, removeLastEmptyRowsInDataFrames, createFileNameWithNr, addBgToExcelSheetRowsBasedOnObj, filterNumpyNdarray, concatAndFilterScheduleDataFrames, createGroupsInListBy, dropnaInDfByAxis, filterAndConvertScheduleDataFrames, getListOfKeys
import pandas as pd
from pandas import ExcelWriter, DataFrame, RangeIndex
import numpy as np
import re
import os


teacherSchedules, classroomSchedules, subjectSchedules, groupedOwnerLists = {}, {}, {}, {}



def createScheduleExcelFiles(classSchedulesDfs):
    
    createScheduleExcelFilesByOwnerTypes(classSchedulesDfs)
    #createScheduleExcelFileForOwnerLists()
    createScheduleExcelFilesByGroupedOwnerLists()



def createScheduleExcelFilesByOwnerTypes(classSchedulesDfs):
    global teacherSchedules, classroomSchedules, subjectSchedules
    msgText=''

    teacherSchedulesTemp, classroomSchedulesTemp, subjectSchedulesTemp = {}, {}, {}

    try:
        for className, classDf in classSchedulesDfs.items():
            
            buildOwnersTypeScheduleBasedOnCol(teacherSchedulesTemp, classDf, 'teacher', className)
            buildOwnersTypeScheduleBasedOnCol(classroomSchedulesTemp, classDf, 'classroom', className)
            buildOwnersTypeScheduleBasedOnCol(subjectSchedulesTemp, classDf, 'subject', className)

        removeLastEmptyRowsInDataFrames([teacherSchedulesTemp, classroomSchedulesTemp, subjectSchedulesTemp])

        teacherSchedules = teacherSchedulesTemp.copy()
        classroomSchedules = classroomSchedulesTemp.copy()
        subjectSchedules = subjectSchedulesTemp.copy()
    
        createScheduleExcelFileForOwnerLists()

        teacherSchedules = { key: teacherSchedules[key]   for key in getPureList(groupedOwnerLists['teachers']) }
        classroomSchedules = { str(key): classroomSchedules[str(key)]   for key in getPureList(groupedOwnerLists['classrooms']) }
        subjectSchedules = { key: subjectSchedules[key]   for key in getPureList(groupedOwnerLists['subjects']) }

        writerForWriteObjOfDfsToExcel(scheduleExcelTeachersPath, teacherSchedules, 'teachers')
        writerForWriteObjOfDfsToExcel(scheduleExcelClassroomsPath, classroomSchedules, 'classrooms')
        writerForWriteObjOfDfsToExcel(scheduleExcelSubjectsPath, subjectSchedules, 'subjects')
            
        
    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files (by owner types).', getTraceback(e))

    if msgText: print(msgText)



def createScheduleExcelFileForOwnerLists():
    global teacherSchedules, classroomSchedules, subjectSchedules, groupedOwnerLists
    msgText=''

    try:
        ownerLists = { 'teachers': getListOfKeys(teacherSchedules),
                       'classrooms': getListOfKeys(classroomSchedules),
                       'subjects': getListOfKeys(subjectSchedules) }
        
        groupedOwnerLists = writeGroupListsToExcelAndFormat(ownerLists)
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files for the owner lists.', getTraceback(e))
    
    if msgText: print(msgText)



def createScheduleExcelFilesByGroupedOwnerLists():
    global teacherSchedules, classroomSchedules, subjectSchedules, groupedOwnerLists
    msgText=''

    try:
        teacherSchedulesByGroups, classroomSchedulesByGroups, subjectSchedulesByGroups = {}, {}, {}

        concatAndFilterSingleGroupListDataFrames('teachers', teacherSchedules, groupedOwnerLists['teachers'], teacherSchedulesByGroups)
        writerForWriteObjOfDfsToExcel(scheduleExcelTeachersGroupedPath, teacherSchedulesByGroups)
        writeObjOfDfsToJSON(scheduleTeachersGroupedDfsJSONPath, teacherSchedulesByGroups)


        concatAndFilterSingleGroupListDataFrames('classrooms', classroomSchedules, groupedOwnerLists['classrooms'], classroomSchedulesByGroups)
        writerForWriteObjOfDfsToExcel(scheduleExcelClassroomsGroupedPath, classroomSchedulesByGroups)
        writeObjOfDfsToJSON(scheduleClassroomsGroupedDfsJSONPath, classroomSchedulesByGroups)
        
        
        concatAndFilterSingleGroupListDataFrames('subjects', subjectSchedules, groupedOwnerLists['subjects'], subjectSchedulesByGroups)
        writerForWriteObjOfDfsToExcel(scheduleExcelSubjectsGroupedPath, subjectSchedulesByGroups)
        writeObjOfDfsToJSON(scheduleSubjectsGroupedDfsJSONPath, subjectSchedulesByGroups)


    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files by grouped owner lists.', getTraceback(e))

    if msgText: print(msgText)



def buildOwnersTypeScheduleBasedOnCol(targetDict={}, baseDf=None, ownersType='', newColValue='', newMainColKey='class'):

    if (isinstance(baseDf,DataFrame)) and (ownersType!='') and (newColValue!=''):
        
        # main group in basic schedule is class
        ownerTypes = {'teacher': 'nauczyciel',
                      'classroom': 'sala',
                      'subject': 'przedmiot'}
        
        # column name in timetable to be changed
        colToBeChanged = ownerTypes[ownersType]

        # make life (program) easier to understand:)
        newScheduleOwner = colToBeChanged

        # main column in basic schedule is subject
        newMainCol = {'class': 'klasa',
                      'teacher': 'nauczyciel',
                      'classroom': 'sala'}
        newMainColName = newMainCol[newMainColKey]
               
        # get the list of teachers/classrooms/subjects inside the timetable
        group = baseDf.xs(newScheduleOwner, axis=1, level=1).stack(sort=False).unique()
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

                    elRows = elRows.groupby(level=[0,1], sort=False).first()
                    #indexLength = len(elRows.index)
                    #elRows.insert(loc=0, column=timeIndexNames[1], value=lessonTimePeriods[:indexLength])

                    if el not in targetDict:
                        targetDict[str(el)] = elRows

                    else:
                        x = targetDict[str(el)].copy()
                        #y = x.combine_first(elRows)
                        #y = x.join(elRows)

                        targetDict[str(el)] = concatAndFilterScheduleDataFrames(x, elRows)



def sortScheduleOwnersList(dataToSort=None):
    msgText = ''
    try:
        pattern = re.compile(r'\d+')
        for key in dataToSort.keys():

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
                                                else  int(pattern.search(x).group(0))
                                                      if pattern.search(x)
                                                      # if element does not have digit,
                                                      # use inf(inity) to move element
                                                      # at the end of the sorting here
                                                      else float('inf')
                                  )
                                )
            # convert strings to integer, if it is possible
            dataToSort[key] = [int(x)   if x.isdigit()   else x   for x in dataToSort[key]]
        
    except Exception as e:
        msgText = handleErrorMsg('\nError loading complete classes data.', getTraceback(e))

    if msgText: print(msgText)

    return dataToSort



def createScheduleGroupedOwnerObjOfDfs(dataToEnter={}):
    
    dataToEnter = sortScheduleOwnersList(dataToEnter)
    sheetsData = {sheetName: dataToEnter[sheetName]   for sheetName in dataToEnter.keys()}
    objOfDfs = {}

    # basic structure for the group list sheets
    for sheetName, sheetData in sheetsData.items():

        namesBaseList = createGroupsInListBy(sheetName, sheetData)
        dfBase = {  'names_base': namesBaseList,
                    'names': sheetData }
        
        objOfDfs[sheetName] = DataFrame(dfBase)
        objOfDfs[sheetName]['names_No.'] = RangeIndex(start=1, stop=len(objOfDfs[sheetName])+1, step=1)
    

    # develop the structure of the worksheet objects
    for listName in objOfDfs:
        df = objOfDfs[listName]

        # indices & their columns
        df['group_No.'] = (df.groupby('names_base', sort=False).ngroup() + 1).astype(str) + '.'
        df['names_in_group_No.'] = (df.groupby('names_base', sort=False).cumcount() + 1).astype(str) + '.'
        
        df.set_index(keys=['group_No.', 'names_base', 'names_in_group_No.'], inplace=True)
        objOfDfs[listName] = df


    return objOfDfs



def createObjForDfRowsColoring(dfWithRowsToColor=DataFrame(), keyToGroupBy='group_No.', strToDelete='.'):
    msgText = ''
    try:
        df = dfWithRowsToColor
        # Create the object for coloring the backgrounds of odd groups.
        # get_loc() starts counting rows from 1, not 0.
        # (Column headers are excluded here.)
        # keyToGroupBy is one of the indices.
        #groupedRows = df.groupby(keyToGroupBy).apply(lambda
        #                                              group: [  df.index.get_loc(x) + 1
        #                                                        for x in group.index ]
        #                                          ).to_dict()
        dfReset = df.copy().reset_index()
        dfReset['index_loc'] = dfReset.index + 1
        groupedRows = dfReset.groupby(keyToGroupBy, sort=False)['index_loc'].apply(list).to_dict()
        
        groupedRowsFiltered = {}
        
        for key, value in groupedRows.items():
            # convert '1.' => '1'
            convertedKey = key.replace(strToDelete,'')

            # int(x) & 1
            # Checks if the number x is odd by testing the least significant bit.
            if convertedKey.isdigit()   and   (int(convertedKey) & 1):
                groupedRowsFiltered[key] = value
        
        # Headers are in the 1st row of the worksheet,
        # so we add 1 to the item's value.
        return {  'rows': [ item+1   for groupList in groupedRowsFiltered.values()
                                        for item in groupList ],
                  'colsLength': len((df.reset_index()).columns) }
    

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating object for coloring Data Frame rows.', getTraceback(e))
    
    if msgText: print(msgText)



def writeGroupListsToExcel(excelPath=None, dataToEnter=None):
    msgText = ''
    dataToReturn = None

    if not excelPath:
        excelPath = createFileNameWithNr()

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

                # indices & their columns
                df['group_No.'] = (df.groupby('names_base', sort=False).ngroup() + 1).astype(str) + '.'
                df['names_in_group_No.'] = (df.groupby('names_base', sort=False).cumcount() + 1).astype(str) + '.'
                
                df.set_index(keys=['group_No.', 'names_base', 'names_in_group_No.'], inplace=True)
                
                sheetsGroups[listName] = createObjForDfRowsColoring(df)

                objOfDfs[listName] = df
                df.to_excel(writer, sheet_name=listName, merge_cells=True)

            dataToReturn = objOfDfs
            addBgToExcelSheetRowsBasedOnObj(writer, sheetsGroups)

        msgText = f'\nData loaded into the schedule Excel file   ' + os.path.basename(excelPath)


    except Exception as e:
        msgText = handleErrorMsg('\nError while writing group lists to excel sheets.', getTraceback(e))
    
    if msgText: print(msgText)

    return dataToReturn



def writeGroupListsToExcelAndFormat(groupLists={}):
    msgText = ''

    try:
        newObjOfDfs = writeGroupListsToExcel(scheduleListsExcelOwnersGroupedPath, groupLists)
        autoFormatExcelCellSizes(excelFilePath=scheduleListsExcelOwnersGroupedPath)
        
    except Exception as e:
        msgText = handleErrorMsg('\nError while writing and formatting the excel files for group lists.', getTraceback(e))

    if msgText: print(msgText)

    return newObjOfDfs



def getPureGroupList(df=DataFrame, colToGroupBy='names_base', colToCreateList='names'):
    # Group data in Data Frame by unique values in column (index) colToGroupBy.
    # Then, make list from colToCreateList.
    newDf = None
    if colToGroupBy in df.index.names   and colToCreateList in df.columns:
        newDf = df.groupby(colToGroupBy, sort=False)[colToCreateList].apply(list).to_dict()

    return newDf



def getPureList(df=DataFrame, colToCreateList='names'):
    # Make list from colToCreateList.
    newDf = None
    if colToCreateList in df.columns:
        newDf = list(df[colToCreateList])

    return newDf



def concatAndFilterSingleGroupListDataFrames(ownersType='', sheetsForOwnerTypes={}, ownersList=DataFrame, newDf={}):
    
    newColNames = { 'classes': 'klasa',
                    'classrooms': 'sala',
                    'subjects': 'przedmiot', 
                    'teachers': 'nauczyciel' }
    
    ownersPureGroupList = getPureGroupList(ownersList)

    # get group names like 'ang', '100' etc.
    for groupName, groupList in ownersPureGroupList.items():
        
        # get elements like 'ang.r', '101' etc.
        for el in groupList:
            x = newDf[str(groupName)]   if str(groupName) in newDf.keys()   else None
            y = sheetsForOwnerTypes[str(el)].copy()

            if isinstance(x, DataFrame):
                # ... and concatenate them :)
                # the line below prevents FutureWarning:
                #   The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.
                #   In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes.
                #   To retain the old behavior, exclude the relevant entries before the concat operation.
                x = dropnaInDfByAxis(x, 1)
                #y = dropnaInDfByAxis(y, 1)
                newDf[str(groupName)] = concatAndFilterScheduleDataFrames(x, y, True, newColNames[ownersType], str(el))

            else:
                newDf[str(groupName)] = filterAndConvertScheduleDataFrames(y, True, newColNames[ownersType], str(el))
    
    return newDf