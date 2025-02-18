from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.excel_constants import excelMargin
from src.constants.schedule_structures_constants import weekdays
from src.constants.paths_constants import classroomsName, scheduleClassroomsExcelPath, scheduleClassroomsWideAndVertDfsJSONPath, scheduleClassroomsWideAndVertExcelPath, scheduleClassroomsExcelPath, scheduleClassroomsGroupedExcelPath, scheduleListsOwnersGroupedExcelPath, scheduleClassroomsGroupedDfsJSONPath, scheduleClassroomsDfsJSONPath, scheduleListsOwnersGroupedJSONPath
from src.constants.conversion_constants import excelEngineName
from src.handlers.overviews_creator import createOverviewsWithLessonsByNrs
from src.utils.converters_utils import getListOfKeys, filterNumpyNdarray, getPureGroupedList, getPureList, convertObjKeysToDesiredOrder, sortObjKeys
from src.utils.excel_utils import removeLastEmptyRowsInDataFrames, dropnaInDfByAxis
#from src.utils.files_utils import createFileNameWithNr
from src.utils.schedule_utils import concatAndFilterScheduleDataFrames, createGroupsInListBy, filterAndConvertScheduleDataFrames
from src.utils.df_utils import combineTwoDfsWithDifferentIndices, completelyTransformDfToVerticalOrder
from src.utils.writers_df_utils import writeObjOfDfsToJSON, writerForObjOfDfsToJSONAndExcel
from src.utils.readers_df_utils import readExcelFileAsObjOfDfs
from src.utils.transl_utils import getTranslation, getTranslByPlural
import pandas as pd
from pandas import ExcelWriter, DataFrame, RangeIndex
import numpy as np
#import re
import os


classSchedules, classroomSchedules, classroomGroupedSchedules, groupedOwnerLists = {}, {}, {}, {}


def createScheduleExcelFiles(classSchedulesDfs, schoolWebInfo):
    global classSchedules, classroomSchedules, classroomGroupedSchedules
    #if classSchedulesDfs is None:
    #    classSchedulesDfs = {}
    
    classSchedules = classSchedulesDfs.copy()

    createScheduleExcelFilesByOwnerTypes(schoolWebInfo)
    createScheduleExcelFileVertical(schoolWebInfo)
    #createScheduleExcelFileForOwnerLists()
    createScheduleExcelFilesByGroupedOwnerLists(schoolWebInfo)
    return { 'classSchedules'            : classSchedules,
             'classroomSchedules'        : classroomSchedules,
             'classroomGroupedSchedules' : classroomGroupedSchedules }



def createScheduleExcelFileVertical(schoolWebInfo):
    global classroomSchedules
    msgText=''

    try:
        newObjOfDfs = {}
        sheetNames = [ getTranslByPlural(ownerTypeName, True)   for ownerTypeName in [classroomsName] ]
        i = 0

        for excelFilePath in [scheduleClassroomsExcelPath]:
            
            #objOfDfs = readExcelFileAsObjOfDfs(excelFilePath)
            objOfDfs = classroomSchedules.copy()
            newDfBasic = DataFrame()
            currSheetName = sheetNames[i]

            #for day in weekdays:
            #    newObjOfDfs[currSheetName + ' - ' + day] = []
            
            # Get the 1st DataFrame in the list
            # dfKey is here a name of for example class, classroom, teacher
            for dfName, df in objOfDfs.items():
                
                # Transform DataFrame into a vertical order where column names become the 1st level of the MultiIndex for the rows.
                dfVert = completelyTransformDfToVerticalOrder(df, dfName, currSheetName)
                
                # THE IMPORTANT WAY TO COMBINE TWO DATAFRAMES WHICH DIFFER IN INDICES.
                newDfBasic = combineTwoDfsWithDifferentIndices(newDfBasic, dfVert)   if not newDfBasic.empty   else dfVert

            newDfBasicByDays = {day: newDfBasic.xs(day, level=0, drop_level=False)   for day in newDfBasic.index.get_level_values(0).unique()}

            # Save sheets.
            for day in weekdays:
                #newObjOfDfs[currSheetName + ' - ' + day].append( newDfBasicByDays[day] )
                newObjOfDfs[currSheetName + ' - ' + day] = newDfBasicByDays[day]

            i=i+1


        writerForObjOfDfsToJSONAndExcel(scheduleClassroomsWideAndVertDfsJSONPath, scheduleClassroomsWideAndVertExcelPath, newObjOfDfs)
        createOverviewsWithLessonsByNrs(newObjOfDfs)

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the Excel file with all the schedules written in wide and vertical format.', getTraceback(e))

    if msgText: print(msgText)



def createScheduleExcelFilesByOwnerTypes(schoolWebInfo):
    global classSchedules, classroomSchedules, groupedOwnerLists
    msgText=''

    classroomSchedulesTemp = {}

    try:
        for className, classDf in classSchedules.items():
            
            buildOwnersTypeScheduleBasedOnCol(classroomSchedulesTemp, classDf, 'classrooms', className)

        removeLastEmptyRowsInDataFrames([classroomSchedulesTemp])
        
        classroomSchedules = classroomSchedulesTemp.copy()
    
        createScheduleExcelFileForOwnerLists()

        classroomSchedules = convertObjKeysToDesiredOrder(classroomSchedulesTemp, getPureList(groupedOwnerLists['classrooms']), True)
        writerForObjOfDfsToJSONAndExcel(scheduleClassroomsDfsJSONPath, scheduleClassroomsExcelPath, classroomSchedules)
        
        
    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files (by owner types).', getTraceback(e))

    if msgText: print(msgText)



def createScheduleExcelFileForOwnerLists():
    global classroomSchedules, groupedOwnerLists
    msgText=''

    try:
        ownerLists = { 'classrooms':  getListOfKeys(classroomSchedules)}
        
        groupedOwnerLists = createScheduleGroupedOwnerObjOfDfs(ownerLists)
        
        if writeObjOfDfsToJSON(scheduleListsOwnersGroupedJSONPath, groupedOwnerLists):
            writeGroupListsToExcelAndFormat(groupedOwnerLists)
    

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files for the owner lists.', getTraceback(e))
    
    if msgText: print(msgText)



def createScheduleExcelFilesByGroupedOwnerLists(schoolWebInfo):
    global classroomSchedules, classroomGroupedSchedules
    msgText=''

    try:
        classroomGroupedSchedules = fullConstructAndWriteScheduleByGroup('classrooms', classroomSchedules, scheduleClassroomsGroupedDfsJSONPath, scheduleClassroomsGroupedExcelPath)

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the schedule Excel files by grouped owner lists.', getTraceback(e))

    if msgText: print(msgText)



def fullConstructAndWriteScheduleByGroup(ownersType, schedulesObj, dfsJSONFilePath, excelFilePath):
    global groupedOwnerLists
    msgText=''

    schedulesByGroups = {}
    try:
        schedulesByGroups = concatAndFilterSingleGroupListDataFrames(ownersType, schedulesObj, groupedOwnerLists[ownersType])

        writerForObjOfDfsToJSONAndExcel(dfsJSONFilePath, excelFilePath, schedulesByGroups)


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while constructing the {ownersType} schedules by grouped owner list and writing them to the Excel file.', getTraceback(e))
    
    if msgText: print(msgText)

    return schedulesByGroups



def buildOwnersTypeScheduleBasedOnCol(targetDict, baseDf, ownersType, newColValue, newMainColKey='class'):
    msgText=''
    #if targetDict is None:
    #    targetDict = {}
    #if baseDf is None:
    #    baseDf = DataFrame
    
    try:
        # column name in timetable to be changed
        colToBeChanged = getTranslByPlural(ownersType)

        # make life (program) easier to understand:)
        newScheduleOwner = colToBeChanged

        # main column in basic schedule is subject
        newMainColName = getTranslation(newMainColKey)
                
        # get the list of teachers/classrooms/subjects inside the timetable
        group = ( baseDf.xs(newScheduleOwner, axis=1, level=1)
                        .stack(sort=False)
                        .unique() )
        group = filterNumpyNdarray(group)

        if len(group):

            # loop for each teacher/classroom/subject
            for el in group:

                # axis  =1 => columns
                #       =0 => index
                #
                # level of MultiIndex in column
                # level =1 => weekdays
                #       =2 => subject, teacher, classroom
                newScheduleOwnerTempData = baseDf.xs(newScheduleOwner, axis=1, level=1)
                
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
                elRows = baseDf.where(maskToFindDesiredPartOfLessons.any(axis=1), emptyValue)

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
                    elRows.loc[:,(weekdays, newMainColName)] = ( elRows.loc[:, (weekdays, newMainColName)]
                                                                      .map( lambda x: newColValue   if pd.notna(x)
                                                                                                    else x ) )

                    elRows = ( elRows.groupby(level=[0,1], sort=False)
                                    .first() )
                    #indexLength = len(elRows.index)
                    #elRows.insert(loc=0, column=timeIndexNames[1], value=lessonTimePeriods[:indexLength])

                    if el not in targetDict:
                        targetDict[str(el)] = elRows

                    else:
                        x = targetDict[str(el)].copy()
                        #y = x.combine_first(elRows)
                        #y = x.join(elRows)

                        targetDict[str(el)] = concatAndFilterScheduleDataFrames(x, elRows)

    except Exception as e:
        msgText = handleErrorMsg(f'\nError while building the {ownersType} schedule based on the DataFrame column.', getTraceback(e))
    
    if msgText: print(msgText)



def createScheduleGroupedOwnerObjOfDfs(dataToEnter):
    msgText = ''
    #if dataToEnter is None:
    #    dataToEnter = {}

    objOfDfs = {}
    try:
        
        dataToEnterSorted = sortObjKeys(dataToEnter)
        sheetsData = { sheetName: dataToEnterSorted[sheetName]   for sheetName in dataToEnterSorted.keys() }


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
            df['group_No.']          = ( (df.groupby('names_base', sort=False)
                                            .ngroup() + 1)
                                            .astype(str) + '.' )
            
            df['names_in_group_No.'] = ( (df.groupby('names_base', sort=False)
                                            .cumcount() + 1)
                                            .astype(str) + '.' )
            
            df.set_index(keys=['group_No.', 'names_base', 'names_in_group_No.'], inplace=True)
            objOfDfs[listName] = df


    except Exception as e:
        msgText = handleErrorMsg(f'\nError while creating a DataFrame object with grouped schedule owners.', getTraceback(e))
    
    if msgText: print(msgText)

    return objOfDfs



def createObjForDfRowsColoring(dfWithRowsToColor, keyColToGroupBy='group_No.', strToDelete='.'):
    msgText = ''

    try:
        #if dfWithRowsToColor is None:
        #    dfWithRowsToColor = DataFrame
        
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
        groupedRows = ( dfReset.groupby(keyColToGroupBy, sort=False)['idx_temp']
                               .apply(list).to_dict() )
        
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



def writeGroupListsToExcelAndFormat(objOfDfs):
    from src.utils.excel_styles_utils import autoFormatExcelCellSizes, addBgToExcelSheetRowsBasedOnObj
    msgText = ''

    #if not excelFilePath:
    #    excelFilePath = createFileNameWithNr()

    try:
        #if objOfDfs is None:
        #    objOfDfs = {}

        excelFilePath = scheduleListsOwnersGroupedExcelPath
        sheetGroups={}
        
        with ExcelWriter(excelFilePath, mode='w+', engine=excelEngineName) as writer:
            
            for listName, df in objOfDfs.items():
                df.to_excel(writer, sheet_name=listName, startrow=excelMargin['row'], startcol=excelMargin['col'], merge_cells=True)
                sheetGroups[listName] = createObjForDfRowsColoring(df)
            
            wb = writer.book
            addBgToExcelSheetRowsBasedOnObj(wb, sheetGroups)
            autoFormatExcelCellSizes(wb)
        
        msgText = f'\nThe data has been loaded into the {(os.path.splitext(excelFilePath)[1][1:]).upper()} file   {os.path.basename(excelFilePath)}'

    except Exception as e:
        msgText = handleErrorMsg('\nError while writing group lists to excel sheets and formatting the file.', getTraceback(e))
    
    if msgText: print(msgText)

    return objOfDfs



def concatAndFilterSingleGroupListDataFrames(ownersType, sheetsForOwnerTypes, ownersList, addNewCol=True):
    msgText=''
    
    #if sheetsForOwnerTypes is None:
    #    sheetsForOwnerTypes = {}
    #if ownersList is None:
    #    ownersList = DataFrame
    objOfDfs = {}

    try:
        newColName = getTranslByPlural(ownersType)
        ownersPureGroupedList = getPureGroupedList(ownersList)

        # get group names like 'ang', '100' etc.
        for groupName, groupList in ownersPureGroupedList.items():
            
            if not isinstance(groupName, str):
                groupName = str(groupName)

            # get elements like 'ang.r', '101' etc.
            for el in groupList:
                x = objOfDfs[groupName]   if groupName in objOfDfs.keys()   else None
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
                        objOfDfs[groupName] = concatAndFilterScheduleDataFrames(x, y, True, newColName, el)
                    else:
                        objOfDfs[groupName] = concatAndFilterScheduleDataFrames(x, y)
                    
                else:
                    if addNewCol:
                        objOfDfs[groupName] = filterAndConvertScheduleDataFrames(y, True, newColName, el)
                    else:
                        objOfDfs[groupName] = y

    except Exception as e:
        msgText = handleErrorMsg('\nError while filtering the single owners group list and concatenating the DataFrames.', getTraceback(e))
                    
    if msgText: print(msgText)
    
    return objOfDfs