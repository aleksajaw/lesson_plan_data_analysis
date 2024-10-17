import pandas as pd
from pandas import ExcelWriter
import numpy as np
from constants import weekdays, scheduleExcelTeachersPath, excelEngineName, timeIndexes, dfRowNrAndTimeTuples
from utils import writeObjOfDfsToExcel


def createOtherScheduleExcelFiles(classSchedulesDfs):

    teacherSchedules = {}

    for className, df in classSchedulesDfs.items():
        
        #weekdays = df.columns.get_level_values(0).unique()

        # axis =1 => columns   =0 => index   level=0, =1   level of MultiIndex in column
        # get the list of teachers inside the timetable
        teachers = df.xs('nauczyciel', axis=1, level=1).stack().unique()
        teachers = filterNumpyNdarray(teachers, '')

        for teacher in teachers:
            # get lessons for specific teacher
            teacherMask = df.xs('nauczyciel', axis=1, level=1) == teacher
            # replace not matching cells with ''
            teacherRows = df.where(teacherMask.any(axis=1))


            for day in weekdays:
                teacherDayMask = teacherMask[day]
                teacherRows.loc[~teacherDayMask, day] = np.nan


            if not teacherRows.empty:

                # change the column name and its value
                # so teacher can see the name of the class they have lesson with
                teacherRows = teacherRows.rename(columns={"nauczyciel": "klasa"})

                # asign to the column "klasa" (old "nauczyciel")
                # map values of the column "klasa" to className
                # only if current value is not ''
                teacherRows.loc[:, (weekdays, 'klasa')] = teacherRows.loc[:, (weekdays, 'klasa')].map(lambda x: className if pd.notna(x) else x)
                
                #print('nauczyciel', teacher)
                
                teacherRows = teacherRows.groupby(level=[0]).first()
                #indexLength = len(teacherRows.index)
                #teacherRows.insert(loc=0, column=timeIndexes[1], value=lessonTimePeriods[:indexLength])
                #print(teacherRows)

                if teacher not in teacherSchedules:
                    teacherSchedules[teacher] = teacherRows

                else:
                    x = teacherSchedules[teacher].copy()
                    y = x.combine_first(teacherRows)
                    lastNonEmptyRow = y.dropna(how='all').index[-1]
                    # keep all the rows up to the last non-empty row
                    teacherSchedules[teacher] = y.loc[:lastNonEmptyRow]
                    #teacherSchedules[teacher] = y.reindex(columns=weekdays)


    sortedTeacherSchedules = {key: teacherSchedules[key] for key in sorted(teacherSchedules)}


    with ExcelWriter(scheduleExcelTeachersPath, mode='w+', engine=excelEngineName) as writer:
                
        try:
            writeObjOfDfsToExcel(writer, sortedTeacherSchedules)
            
        except Exception as writeError:
            print(f"Error while writing to the teachers' Excel file: {writeError}")



def filterNumpyNdarray(arr=np.ndarray, el=''):
    return np.sort(arr[arr != el])