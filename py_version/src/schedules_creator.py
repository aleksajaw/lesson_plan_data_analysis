import pandas as pd
from pandas import ExcelWriter, DataFrame
import numpy as np
from constants import weekdays, scheduleExcelTeachersPath, scheduleExcelClassroomsPath, excelEngineName, timeIndexes, dfRowNrAndTimeTuples
from utils import writeObjOfDfsToExcel


def createOtherScheduleExcelFiles(classSchedulesDfs):

    teacherSchedules = {}
    classroomSchedules = {}

    for className, classDf in classSchedulesDfs.items():
        #weekdays = classDf.columns.get_level_values(0).unique()

        buildGroupScheduleBasedOnCol(teacherSchedules, classDf, 'teacher', className)
        buildGroupScheduleBasedOnCol(classroomSchedules, classDf, 'classroom', className)

    writeGroupSchedulesToExcel(teacherSchedules, 'teacher', scheduleExcelTeachersPath)
    writeGroupSchedulesToExcel(classroomSchedules, 'classroom', scheduleExcelClassroomsPath)



def buildGroupScheduleBasedOnCol(targetDict={}, baseDf=None, groupType='', newColValue=''):

    if (isinstance(baseDf,DataFrame)) and (groupType!='') and (newColValue!=''):
        
        groupTypes = {'teacher': 'nauczyciel',
                      'classroom': 'sala'}

        # column name in timetable
        colToBeChanged = groupTypes[groupType]

        # make life (program) easier to understand:)
        newScheduleOwner = colToBeChanged
        
        # get the list of teachers/classrooms inside the timetable
        group = baseDf.xs(newScheduleOwner, axis=1, level=1).stack().unique()
        group = filterNumpyNdarray(group)

        if len(group):

            # loop for each teacher/classroom
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
               
                # get cells with value of specific el in group (teacher or classroom)
                # e.g. 110 or KJ
                # not whole subject, classroom and teacher 
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


                # restrict loop actions if row does not match mask
                if not elRows.empty:

                    # change the column name and its value
                    elRows = elRows.rename(columns={colToBeChanged: 'klasa'})

                    # asign
                    #   to the column "klasa" (old "nauczyciel" or "sala")
                    #   mapped values of the column "klasa" to className
                    # only if current value is not NaN in numeric arrays,
                    #   None or NaN in object arrays,
                    #   NaT in datetimelike
                    elRows.loc[:,(weekdays, 'klasa')] = elRows.loc[:, (weekdays, 'klasa')].map(lambda x: newColValue   if pd.notna(x)   else x)

                    elRows = elRows.groupby(level=[0]).first()
                    #indexLength = len(elRows.index)
                    #elRows.insert(loc=0, column=timeIndexes[1], value=lessonTimePeriods[:indexLength])

                    if el not in targetDict:
                        targetDict[str(el)] = elRows

                    else:
                        x = targetDict[str(el)].copy()
                        y = x.combine_first(elRows)
                        #print('yyyyyyyy', y)
                        lastNonEmptyRow = y.dropna(how='all').index[-1]
                        # keep all the rows up to the last non-empty row
                        targetDict[str(el)] = y.loc[:lastNonEmptyRow]
                        #schedulesDict[el] = y.reindex(columns=weekdays)



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
            writeObjOfDfsToExcel(writer, sortedGroupSchedules)
                
        except Exception as writeError:
            print(f"Error while writing to the {groupSchedulesTitle}' Excel file: {writeError}")