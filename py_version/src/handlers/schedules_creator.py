import pandas as pd
from pandas import ExcelWriter, DataFrame
import numpy as np
from src.constants import weekdays, scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelGroupListsPath, excelEngineName, timeIndexes, dfRowNrAndTimeTuples
from src.utils import writeObjOfDfsToExcel, autoFormatMainExcelFile, writeGroupListsToExcelSheets, autoFormatExcelFileCellSizes, removeLastEmptyRowsInExcel, concatAndFilterDataFrames


def createOtherScheduleExcelFiles(classSchedulesDfs):

    teacherSchedules = {}
    classroomSchedules = {}
    subjectSchedules = {}

    for className, classDf in classSchedulesDfs.items():
        #weekdays = classDf.columns.get_level_values(0).unique()

        buildGroupScheduleBasedOnCol(teacherSchedules, classDf, 'teacher', className)
        buildGroupScheduleBasedOnCol(classroomSchedules, classDf, 'classroom', className)
        buildGroupScheduleBasedOnCol(subjectSchedules, classDf, 'subject', className)
    
    groupLists = { 'teachers': list(teacherSchedules.keys()),
                   'classrooms': list(classroomSchedules.keys()),
                   'subjects': list(subjectSchedules.keys()) }

    writeGroupListsToExcel(groupLists)    
    removeLastEmptyRowsInExcel([teacherSchedules,classroomSchedules, subjectSchedules])
    
    writeGroupSchedulesToExcel(teacherSchedules, 'teacher', scheduleExcelTeachersPath)
    writeGroupSchedulesToExcel(classroomSchedules, 'classroom', scheduleExcelClassroomsPath)
    writeGroupSchedulesToExcel(subjectSchedules, 'subject', scheduleExcelSubjectsPath)



def buildGroupScheduleBasedOnCol(targetDict={}, baseDf=None, groupType='', newColValue='', newMainColKey='class'):

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

                        targetDict[str(el)] = concatAndFilterDataFrames(x, elRows)



def filterNumpyNdarray(arr=np.ndarray, shouldConvertBack=False, elToDel=''):
    # convert values to string
    arrAsStr = arr.astype(str)
    # remove specific value
    sortedArr = np.sort( arrAsStr[ arrAsStr != elToDel] )

    return np.array([val for val in sortedArr])



def writeGroupSchedulesToExcel(groupSchedules=None, groupSchedulesTitle='', scheduleExcelPath=''):
    
    #if len(groupSchedules.keys()):
    sortedGroupSchedules = {key: groupSchedules[key] for key in sorted(groupSchedules)}
    
    with ExcelWriter(scheduleExcelPath, mode='w+', engine=excelEngineName) as writer:       
        try:
            writeObjOfDfsToExcel(writer, scheduleExcelPath, sortedGroupSchedules)
            autoFormatMainExcelFile(writer.book, scheduleExcelPath)
                
        except Exception as writeError:
            print(f"Error while writing to the {groupSchedulesTitle}' Excel file: {writeError}")



def writeGroupListsToExcel(groupLists={}):
    writeGroupListsToExcelSheets(scheduleExcelGroupListsPath, groupLists)
    autoFormatExcelFileCellSizes(excelFilePath=scheduleExcelGroupListsPath)