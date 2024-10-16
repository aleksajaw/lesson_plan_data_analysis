import pandas as pd
import numpy as np
from constants import weekdays


def test(classSchedulesDfs):

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
            #teacherRows = teacherRows.where(~teacherMask.any(axis=1), '')

            for day in weekdays:
                teacherDayMask = teacherMask[day]
                teacherRows.loc[~teacherDayMask, day] = ''


            if not teacherRows.empty:

                # change the column name and its value
                # so teacher can see the name of the class they have lesson with
                teacherRows = teacherRows.rename(columns={"nauczyciel": "klasa"})

                # asign to the column "klasa" (old "nauczyciel")
                # map values of the column "klasa" to className
                # only if current value is not ''
                teacherRows.loc[:, (weekdays, 'klasa')] = teacherRows.loc[:, (weekdays, 'klasa')].map(lambda x: className if x != '' else x)
                
                print('nauczyciel', teacher)
                print(teacherRows)

                if teacher not in teacherSchedules:
                    teacherSchedules[teacher] = teacherRows
                else:
                    teacherSchedules[teacher] = pd.concat([teacherSchedules[teacher], teacherRows], axis=0)


    for teacher, df in teacherSchedules.items():
        #print(df)
        df.to_excel(f"timetable_{teacher}.xlsx")



def filterNumpyNdarray(arr=np.ndarray, el=''):
    return arr[arr != el]