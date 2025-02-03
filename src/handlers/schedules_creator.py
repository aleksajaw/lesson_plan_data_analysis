from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.schedule_structures_constants import dayAndAttrNames, weekdays, excelMargin, timeIndexNames, dfRowIndexNamesTuples, dfRowNrAndTimeTuples
from src.constants.paths_constants import allOwnerTypeNames, testExcelPath, testJSONPath, scheduleClassesVerticallyExcelPath, schedulesWideAndVerticallyExcelPath, scheduleTeachersExcelPath, scheduleClassroomsExcelPath, scheduleSubjectsExcelPath, scheduleClassesGroupedExcelPath, scheduleTeachersGroupedExcelPath, scheduleClassroomsGroupedExcelPath, scheduleSubjectsGroupedExcelPath, scheduleListsOwnersGroupedExcelPath, schedulesWideAndVerticallyDfsJSONPath, scheduleClassesGroupedDfsJSONPath, scheduleTeachersGroupedDfsJSONPath, scheduleClassroomsGroupedDfsJSONPath, scheduleSubjectsGroupedDfsJSONPath, scheduleTeachersDfsJSONPath, scheduleClassroomsDfsJSONPath, scheduleSubjectsDfsJSONPath, scheduleListsOwnersGroupedJSONPath, allScheduleExcelPaths
from src.constants.conversion_constants import excelEngineName
from src.utils.converters_utils import getListOfKeys, filterNumpyNdarray, getPureGroupedList, getPureList, convertObjKeysToDesiredOrder, sortObjKeys
from src.utils.excel_utils import removeLastEmptyRowsInDataFrames, dropnaInDfByAxis
from src.utils.files_utils import createFileNameWithNr
from src.utils.schedule_utils import concatAndFilterScheduleDataFrames, createGroupsInListBy, filterAndConvertScheduleDataFrames
from src.utils.writers_df_utils import writeObjOfDfsToJSON, writerForObjOfDfsToJSONAndExcel, writerForObjOfDfsToExcel, writerForDfToExcelSheet
from src.utils.readers_df_utils import readExcelFileAsObjOfDfs
from src.utils.transl_utils import getTranslation, getTranslByPlural
import pandas as pd
from pandas import ExcelWriter, DataFrame, RangeIndex, CategoricalDtype, MultiIndex
import numpy as np
import re
import os


classSchedules, teacherSchedules, classroomSchedules, subjectSchedules, groupedOwnerLists = {}, {}, {}, {}, {}


def createScheduleExcelFiles(classSchedulesDfs={}):
    global classSchedules
    classSchedules = classSchedulesDfs.copy()

    createScheduleExcelFilesByOwnerTypes()
    createScheduleExcelFileVertical()
    #createScheduleExcelFileForOwnerLists()
    createScheduleExcelFilesByGroupedOwnerLists()



def createScheduleExcelFileVertical():
    msgText=''

    try:
        newObjOfDfs = {}
        sheetNames = [ getTranslByPlural(ownerTypeName, True)   for ownerTypeName in allOwnerTypeNames ]
        i = 0

        for excelFilePath in allScheduleExcelPaths:
            
            objOfDfs = readExcelFileAsObjOfDfs(excelFilePath)
            newDf = DataFrame()
            currSheetName = sheetNames[i]

            # Get the 1st DataFrame in the list
            for dfKey, df in objOfDfs.items():
                
                # Transform DataFrame into a vertical order where column names become the 1st level of the MultiIndex for the rows. 
                dfVertical = df.stack( level=0, dropna=False)
                
                # Correct the order of the levels in the hierarchy.
                dfVertical.index = dfVertical.index.reorder_levels( [2, 0, 1] )
                
                # Making the 1st lvl a CategoricalDType to simplify the sorting proccess.
                weekdaysCatDtype = CategoricalDtype(categories=weekdays, ordered=True)
                dfVertical.index = dfVertical.index.set_levels(
                                              dfVertical.index.levels[0].astype(weekdaysCatDtype), level=0
                                          )
                
                # Sort the values in the row index levels, except the last row (it is not needed). 
                dfVertical = dfVertical.sort_values(dfVertical.index.names[:-1])

                # Add the parent name for the class columns.
                dfVertical.columns = MultiIndex.from_product([[dfKey], dfVertical.columns], names=[currSheetName.capitalize()]+dfVertical.columns.names)
                
                # Remove empty rows.
                dfVertical = dfVertical[~(dfVertical == '').all(axis=1)]

                if not newDf.empty:
                # THE IMPORTANT WAY TO COMBINE TWO DATAFRAMES WHICH DIFFER IN INDICES.

                    # Create a new column named 'idx_temp' containing the numeric index.
                    newDf['idx_temp']      = newDf.groupby(newDf.index).cumcount()
                    dfVertical['idx_temp'] = dfVertical.groupby(dfVertical.index).cumcount()

                    # Set the column 'idx_temp' as an extra lvl of the current DataFrame index.
                    newDf      = newDf.set_index(['idx_temp'], append=True)
                    dfVertical = dfVertical.set_index(['idx_temp'], append=True)
                    # Combine two DataFrames along the columns axis
                    # and then remove the 'idx_temp' level from the MultiIndex, completely removing it from the columns.
                    merged = pd.concat([newDf, dfVertical], axis=1).reset_index(level=['idx_temp'], drop=True)
                    newDf = merged.sort_index()
                    
                else:
                    newDf = dfVertical

            newObjOfDfs[currSheetName] = newDf
            i=i+1

        writerForObjOfDfsToJSONAndExcel(schedulesWideAndVerticallyDfsJSONPath, schedulesWideAndVerticallyExcelPath, newObjOfDfs)

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the Excel file with all the schedules written wide and vertically.', getTraceback(e))

    if msgText: print(msgText)



def createScheduleExcelFilesByOwnerTypes():
    global classSchedules, teacherSchedules, classroomSchedules, subjectSchedules, groupedOwnerLists
    msgText=''

    teacherSchedulesTemp, classroomSchedulesTemp, subjectSchedulesTemp = {}, {}, {}

    try:
        for className, classDf in classSchedules.items():
            
            buildOwnersTypeScheduleBasedOnCol(teacherSchedulesTemp, classDf, 'teachers', className)
            buildOwnersTypeScheduleBasedOnCol(classroomSchedulesTemp, classDf, 'classrooms', className)
            buildOwnersTypeScheduleBasedOnCol(subjectSchedulesTemp, classDf, 'subjects', className)

        removeLastEmptyRowsInDataFrames([teacherSchedulesTemp, classroomSchedulesTemp, subjectSchedulesTemp])

        teacherSchedules   = teacherSchedulesTemp.copy()
        classroomSchedules = classroomSchedulesTemp.copy()
        subjectSchedules   = subjectSchedulesTemp.copy()
    
        createScheduleExcelFileForOwnerLists()

        teacherSchedules = convertObjKeysToDesiredOrder(teacherSchedulesTemp, getPureList(groupedOwnerLists['teachers']))
        writerForObjOfDfsToJSONAndExcel(scheduleTeachersDfsJSONPath, scheduleTeachersExcelPath, teacherSchedules)

        classroomSchedules = convertObjKeysToDesiredOrder(classroomSchedulesTemp, getPureList(groupedOwnerLists['classrooms']), True)
        writerForObjOfDfsToJSONAndExcel(scheduleClassroomsDfsJSONPath, scheduleClassroomsExcelPath, classroomSchedules)

        subjectSchedules = convertObjKeysToDesiredOrder(subjectSchedulesTemp, getPureList(groupedOwnerLists['subjects']))
        writerForObjOfDfsToJSONAndExcel(scheduleSubjectsDfsJSONPath, scheduleSubjectsExcelPath, subjectSchedules)
        
        
    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files (by owner types).', getTraceback(e))

    if msgText: print(msgText)



def createScheduleExcelFileForOwnerLists():
    global classSchedules, teacherSchedules, classroomSchedules, subjectSchedules, groupedOwnerLists
    msgText=''

    try:
        ownerLists = { 'classes'   :  getListOfKeys(classSchedules),
                       'teachers'  :  getListOfKeys(teacherSchedules),
                       'classrooms':  getListOfKeys(classroomSchedules),
                       'subjects'  :  getListOfKeys(subjectSchedules) }
        
        groupedOwnerLists = createScheduleGroupedOwnerObjOfDfs(ownerLists)
        
        if writeObjOfDfsToJSON(scheduleListsOwnersGroupedJSONPath, groupedOwnerLists):
            writeGroupListsToExcelAndFormat(groupedOwnerLists)
    

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files for the owner lists.', getTraceback(e))
    
    if msgText: print(msgText)



def createScheduleExcelFilesByGroupedOwnerLists():
    global classSchedules, teacherSchedules, classroomSchedules, subjectSchedules, groupedOwnerLists
    msgText=''

    try:
        fullConstructAndWriteScheduleByGroup('classes', classSchedules, scheduleClassesGroupedDfsJSONPath, scheduleClassesGroupedExcelPath)
        fullConstructAndWriteScheduleByGroup('teachers', teacherSchedules, scheduleTeachersGroupedDfsJSONPath, scheduleTeachersGroupedExcelPath)
        fullConstructAndWriteScheduleByGroup('classrooms', classroomSchedules, scheduleClassroomsGroupedDfsJSONPath, scheduleClassroomsGroupedExcelPath)
        fullConstructAndWriteScheduleByGroup('subjects', subjectSchedules, scheduleSubjectsGroupedDfsJSONPath, scheduleSubjectsGroupedExcelPath)

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files by grouped owner lists.', getTraceback(e))

    if msgText: print(msgText)



def fullConstructAndWriteScheduleByGroup(ownersType='', schedulesObj={}, dfsJSONFilePath='', excelFilePath=''):
    global groupedOwnerLists

    msgText=''
    try:
        schedulesByGroups = {}
        concatAndFilterSingleGroupListDataFrames(ownersType, schedulesObj, groupedOwnerLists[ownersType], schedulesByGroups)

        writerForObjOfDfsToJSONAndExcel(dfsJSONFilePath, excelFilePath, schedulesByGroups)


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while constructing the {ownersType} schedules by grouped owner list and writing them to the Excel file.', getTraceback(e))
    
    if msgText: print(msgText)



def buildOwnersTypeScheduleBasedOnCol(targetDict={}, baseDf=None, ownersType='', newColValue='', newMainColKey='class'):

    if isinstance(baseDf, DataFrame)   and   ownersType   and   newColValue:
     
        # column name in timetable to be changed
        colToBeChanged = getTranslByPlural(ownersType)

        # make life (program) easier to understand:)
        newScheduleOwner = colToBeChanged

        # main column in basic schedule is subject
        newMainColName = getTranslation(newMainColKey)
               
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
                    elRows = elRows.rename( columns={ colToBeChanged: newMainColName } )

                    # asign
                    #   to the column "klasa" (old "nauczyciel", "przedmiot", "sala")
                    #   mapped values of the column "klasa" to className
                    # only if current value is not NaN in numeric arrays,
                    #   None or NaN in object arrays,
                    #   NaT in datetimelike
                    elRows.loc[:,(weekdays, newMainColName)] = elRows.loc[:, (weekdays, newMainColName)].map( lambda x: newColValue   if pd.notna(x)
                                                                                                                                      else x )

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



def createScheduleGroupedOwnerObjOfDfs(dataToEnter={}):
    
    dataToEnter = sortObjKeys(dataToEnter)
    sheetsData = { sheetName: dataToEnter[sheetName]   for sheetName in dataToEnter.keys() }
    objOfDfs = {}

    # basic structure for the group list sheets
    for sheetName, sheetData in sheetsData.items():

        namesBaseList = createGroupsInListBy(sheetName, sheetData)
        dfBase = { 'names_base':  namesBaseList,
                   'names'     :  sheetData }
        
        objOfDfs[sheetName] = DataFrame(dfBase)
        objOfDfs[sheetName]['names_No.'] = RangeIndex(start=1, stop=len(objOfDfs[sheetName])+1, step=1)
    

    # develop the structure of the worksheet objects
    for listName in objOfDfs:
        df = objOfDfs[listName]

        # indices & their columns
        df['group_No.']          = (df.groupby('names_base', sort=False).ngroup() + 1).astype(str) + '.'
        df['names_in_group_No.'] = (df.groupby('names_base', sort=False).cumcount() + 1).astype(str) + '.'
        
        df.set_index(keys=['group_No.', 'names_base', 'names_in_group_No.'], inplace=True)
        objOfDfs[listName] = df


    return objOfDfs



def createObjForDfRowsColoring(dfWithRowsToColor=DataFrame(), keyColToGroupBy='group_No.', strToDelete='.'):
    msgText = ''
    try:
        df = dfWithRowsToColor.copy()
        # Create the object for coloring the backgrounds of odd groups.
        # get_loc() starts counting rows from 1, not 0.
        # (Column headers are excluded here.)
        # keyToGroupBy is one of the indices.
        #groupedRows = df.groupby(keyToGroupBy).apply(lambda
        #                                              group: [  df.index.get_loc(x) + 1
        #                                                        for x in group.index ]
        #                                          ).to_dict()
        dfReset = df.reset_index()
        # Create a temporary numeric index to simplify row counting.
        dfReset['idx_temp'] = dfReset.index + 1
        groupedRows = dfReset.groupby(keyColToGroupBy, sort=False)['idx_temp'].apply(list).to_dict()
        
        groupedRowsFiltered = {}
        
        for key, value in groupedRows.items():
            # convert '1.' => '1'
            convertedKey = key.replace(strToDelete,'')

            # int(x) & 1
            # Checks if the number x is odd by testing the least significant bit.
            if convertedKey.isdigit()   and   (int(convertedKey) & 1):
                groupedRowsFiltered[key] = value
        
        # Add the length of the column levels to the margin and the item's value.
        return { 'rows'      :  [ excelMargin['row'] + df.columns.nlevels + item   for groupList in groupedRowsFiltered.values()
                                                                                      for item in groupList ],
                 'colsLength':  len((df.reset_index()).columns) }
    

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating object for coloring Data Frame rows.', getTraceback(e))
    
    if msgText: print(msgText)



def writeGroupListsToExcelAndFormat(objOfDfs={}, excelFilePath=scheduleListsOwnersGroupedExcelPath):
    from src.utils.excel_styles_utils import autoFormatExcelCellSizes, addBgToExcelSheetRowsBasedOnObj
    msgText = ''

    #if not excelFilePath:
    #    excelFilePath = createFileNameWithNr()

    try:
        sheetGroups={}
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:
            
            for listName, df in objOfDfs.items():
                df.to_excel(writer, sheet_name=listName, startrow=excelMargin['row'], startcol=excelMargin['col'], merge_cells=True)
                sheetGroups[listName] = createObjForDfRowsColoring(df)
            
            addBgToExcelSheetRowsBasedOnObj(writer, sheetGroups)
            autoFormatExcelCellSizes(writer.book, excelFilePath)
        
        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg('\nError while writing group lists to excel sheets and formatting the file.', getTraceback(e))
    
    if msgText: print(msgText)

    return objOfDfs



def concatAndFilterSingleGroupListDataFrames(ownersType='', sheetsForOwnerTypes={}, ownersList=DataFrame, newDf={}, addNewCol=True):
    
    newColName = getTranslByPlural(ownersType)
    
    ownersPureGroupedList = getPureGroupedList(ownersList)

    # get group names like 'ang', '100' etc.
    for groupName, groupList in ownersPureGroupedList.items():
        
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
                if addNewCol:
                    newDf[str(groupName)] = concatAndFilterScheduleDataFrames(x, y, True, newColName, str(el))
                else:
                    newDf[str(groupName)] = concatAndFilterScheduleDataFrames(x, y)
                    
            else:
                if addNewCol:
                    newDf[str(groupName)] = filterAndConvertScheduleDataFrames(y, True, newColName, str(el))
                else:
                    newDf[str(groupName)] = y
                    
    
    return newDf