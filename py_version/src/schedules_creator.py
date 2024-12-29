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

        # axis =1 => columns
        #      =0 => index
        # level=0, =1   level of MultiIndex in column

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
                baseDfCopy = baseDf.copy()

                # get lessons for specific el in group (teacher or classroom)
                # including their data type (integer or string)
                try:
                    elMask = baseDfCopy.xs(newScheduleOwner, axis=1, level=1) == int(el)
                except:
                    elMask = baseDfCopy.xs(newScheduleOwner, axis=1, level=1) == el

                # replace not matching whole rows with NaN
                # leave rows with any matches untouched
                elRows = baseDfCopy.where(elMask.any(axis=1))

                # divide rows into weekdays
                # replace value with NaN for not matching days
                for day in weekdays:
                    elDayMask = elMask[day]
                    elRows.loc[~elDayMask, day] = np.nan


                # restrict loop actions if row does not match mask
                if not elRows.empty:

                    # change the column name and its value
                    elRows = elRows.rename(columns={colToBeChanged: 'klasa'})
                    
                    # asign
                    # to the column "klasa" (old "nauczyciel" or "sala")
                    # mapped values of the column "klasa" to className
                    # only if current value is not NaN in numeric arrays, None or NaN in object arrays, NaT in datetimelike
                    elRows.loc[:, (weekdays, 'klasa')] = elRows.loc[:, (weekdays, 'klasa')].map(lambda x: newColValue   if pd.notna(x)   else x)
                    #print(GroupName, el)
                    
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