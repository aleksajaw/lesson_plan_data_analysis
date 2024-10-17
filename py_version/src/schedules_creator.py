import pandas as pd
from pandas import ExcelWriter, DataFrame
import numpy as np
from constants import weekdays, scheduleExcelTeachersPath, scheduleExcelClassroomsPath, excelEngineName, timeIndexes, dfRowNrAndTimeTuples
from utils import writeObjOfDfsToExcel


def createOtherScheduleExcelFiles(classSchedulesDfs):

    teacherSchedules = {}
    classroomSchedules = {}

    for className, df in classSchedulesDfs.items():
        #weekdays = df.columns.get_level_values(0).unique()

        # axis =1 => columns   =0 => index   level=0, =1   level of MultiIndex in column
        # get the list of teachers inside the timetable
        teacherColName = 'nauczyciel'
        classroomColName = 'sala'
        
        teachers = df.xs(teacherColName, axis=1, level=1).stack().unique()
        teachers = filterNumpyNdarray(teachers)

        classrooms = df.xs(classroomColName, axis=1, level=1).stack().unique()
        classrooms = filterNumpyNdarray(classrooms, True)

        createSchedule(teacherSchedules, df, teachers, teacherColName, className)
        createSchedule(classroomSchedules, df, classrooms, classroomColName, className)


    sortedTeacherSchedules = {key: teacherSchedules[key] for key in sorted(teacherSchedules)}
    sortedClassroomSchedules = {key: classroomSchedules[key] for key in sorted(classroomSchedules)}


    with ExcelWriter(scheduleExcelTeachersPath, mode='w+', engine=excelEngineName) as writer:
                
        try:
            writeObjOfDfsToExcel(writer, sortedTeacherSchedules)
            
        except Exception as writeError:
            print(f"Error while writing to the teachers' Excel file: {writeError}")


    with ExcelWriter(scheduleExcelClassroomsPath, mode='w+', engine=excelEngineName) as writer:
                
        try:
            writeObjOfDfsToExcel(writer, sortedClassroomSchedules)
            
        except Exception as writeError:
            print(f"Error while writing to the classrooms' Excel file: {writeError}")



def filterNumpyNdarray(arr=np.ndarray, shouldConvertBack=False, elToDel=''):
    arrAsStr = arr.astype(str)
    sortedArr = np.sort( arrAsStr[ arrAsStr != elToDel] )

    return np.array([val for val in sortedArr])



def createSchedule(schedulesDict={}, df=None, group=np.ndarray, elColName='', newColValue=''):
    
    if (isinstance(df,DataFrame)) and (len(group)) and (elColName!='') and (newColValue!=''):
        for el in group:
          
            dfCopy = df.copy()
            # get lessons for specific el
            try:
                elMask = dfCopy.xs(elColName, axis=1, level=1) == int(el)
            except:
                elMask = dfCopy.xs(elColName, axis=1, level=1) == el

            # replace not matching cells with ''
            elRows = dfCopy.where(elMask.any(axis=1))


            for day in weekdays:
                elDayMask = elMask[day]
                elRows.loc[~elDayMask, day] = np.nan


            if not elRows.empty:

                # change the column name and its value
                elRows = elRows.rename(columns={elColName: 'klasa'})
                
                # asign to the column "klasa" (old "nauczyciel")
                # map values of the column "klasa" to className
                # only if current value is not ''
                elRows.loc[:, (weekdays, 'klasa')] = elRows.loc[:, (weekdays, 'klasa')].map(lambda x: newColValue   if pd.notna(x)   else x)
                #print(colName, el)
                
                elRows = elRows.groupby(level=[0]).first()
                #indexLength = len(elRows.index)
                #elRows.insert(loc=0, column=timeIndexes[1], value=lessonTimePeriods[:indexLength])

                if el not in schedulesDict:
                    schedulesDict[str(el)] = elRows

                else:
                    x = schedulesDict[str(el)].copy()
                    y = x.combine_first(elRows)
                    #print('yyyyyyyy', y)
                    lastNonEmptyRow = y.dropna(how='all').index[-1]
                    # keep all the rows up to the last non-empty row
                    schedulesDict[str(el)] = y.loc[:lastNonEmptyRow]
                    #schedulesDict[el] = y.reindex(columns=weekdays)