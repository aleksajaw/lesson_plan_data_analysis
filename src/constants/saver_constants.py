# DIR PATHS
import os
currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
projectRoot = os.path.dirname(srcDirPath)
#schedulePath = os.path.join(srcDirPath, 'schedules')
schedulePath = os.path.join(projectRoot, 'schedules')
scheduleJSONPath = os.path.join(schedulePath, 'json')
logsPath = os.path.join(projectRoot, 'logs')


# FILE NAMES
scheduleExcelClassesName = 'schedule_classes.xlsx'
scheduleExcelTeachersName = 'schedule_teachers.xlsx'
scheduleExcelClassroomsName = 'schedule_classrooms.xlsx'
scheduleExcelSubjectsName = 'schedule_subjects.xlsx'

scheduleListsExcelOwnersGroupedName = 'schedule-lists_owners-grouped.xlsx'

scheduleExcelClassesGroupedName = 'schedule_classes-grouped.xlsx'
scheduleExcelTeachersGroupedName = 'schedule_teachers-grouped.xlsx'
scheduleExcelClassroomsGroupedName = 'schedule_classrooms-grouped.xlsx'
scheduleExcelSubjectsGroupedName = 'schedule_subjects-grouped.xlsx'

scheduleClassesBaseJSONName = 'base_schedule_classes.json'

scheduleListsOwnersGroupedJSONName = 'dfs_schedule-lists_owners-grouped.json'

scheduleClassesGroupedJSONName = 'dfs_schedule_classes-grouped.json'
scheduleTeachersGroupedJSONName = 'dfs_schedule_teachers-grouped.json'
scheduleClassroomsGroupedJSONName = 'dfs_schedule_classrooms-grouped.json'
scheduleSubjectsGroupedJSONName = 'dfs_schedule_subjects-grouped.json'

scheduleClassesDfsJSONName = 'dfs_schedule_classes.json'
scheduleTeachersDfsJSONName = 'dfs_schedule_teachers.json'
scheduleClassroomsDfsJSONName = 'dfs_schedule_classrooms.json'
scheduleSubjectsDfsJSONName = 'dfs_schedule_subjects.json'

scheduleExcelClassesJSONName = 'dfs_schedule-excel_classes.json'


# FILE PATHS
# Excel
# For classes
scheduleExcelClassesPath = os.path.join(schedulePath, scheduleExcelClassesName)
# For teachers
scheduleExcelTeachersPath =  os.path.join(schedulePath, scheduleExcelTeachersName)
# For classrooms
scheduleExcelClassroomsPath =  os.path.join(schedulePath, scheduleExcelClassroomsName)
# For subjects
scheduleExcelSubjectsPath =  os.path.join(schedulePath, scheduleExcelSubjectsName)


# For schedule lists with grouped owners
scheduleListsExcelOwnersGroupedPath =  os.path.join(schedulePath, scheduleListsExcelOwnersGroupedName)

# For classes grouped
scheduleExcelClassesGroupedPath =  os.path.join(schedulePath, scheduleExcelClassesGroupedName)
# For teachers grouped
scheduleExcelTeachersGroupedPath =  os.path.join(schedulePath, scheduleExcelTeachersGroupedName)
# For classrooms grouped
scheduleExcelClassroomsGroupedPath =  os.path.join(schedulePath, scheduleExcelClassroomsGroupedName)
# For subjects grouped
scheduleExcelSubjectsGroupedPath =  os.path.join(schedulePath, scheduleExcelSubjectsGroupedName)


# JSON
# Pure scraped classes
scheduleClassesBaseJSONPath =  os.path.join(scheduleJSONPath, scheduleClassesBaseJSONName)


# JSON with Data Frames
# For schedule lists with grouped owners
scheduleListsOwnersGroupedJSONPath =  os.path.join(scheduleJSONPath, scheduleListsOwnersGroupedJSONName)

# For classes grouped
scheduleClassesGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassesGroupedJSONName)
# For teachers grouped
scheduleTeachersGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleTeachersGroupedJSONName)
# For classrooms grouped
scheduleClassroomsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassroomsGroupedJSONName)
# For subjects grouped
scheduleSubjectsGroupedDfsJSONPath = os.path.join(scheduleJSONPath, scheduleSubjectsGroupedJSONName)


# For classes
scheduleClassesDfsJSONPath =  os.path.join(scheduleJSONPath, scheduleClassesDfsJSONName)
# For teachers
scheduleTeachersDfsJSONPath = os.path.join(scheduleJSONPath, scheduleTeachersDfsJSONName)
# For classrooms
scheduleClassroomsDfsJSONPath = os.path.join(scheduleJSONPath, scheduleClassroomsDfsJSONName)
# For subjects
scheduleSubjectsDfsJSONPath = os.path.join(scheduleJSONPath, scheduleSubjectsDfsJSONName)


# Data read from the current basic Excel
scheduleExcelClassesDfsJSONPath =  os.path.join(scheduleJSONPath, scheduleExcelClassesJSONName)


JSONIndentValue = 4


# variables for handling pandas' Data Frame and excel
timeIndexNames = ['Nr','Godz']
weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
lessonAttrs3el = ['przedmiot', 'grupa', 'nauczyciel', 'sala']
lessonAttrs4el = ['przedmiot', 'nauczyciel', 'klasa', 'sala']
dfRowIndexNamesTuples = [
    ('Nr', ''),
    ('Godz', '')
]
lessonTimePeriods = [
    '8:00-8:45',
    '8:50-9:35',
    '9:40-10:25',
    '10:40-11:25',
    '11:30-12:15',
    '12:20-13:05',
    '13:10-13:55',
    '14:10-14:55',
    '15:00-15:45',
    '15:50-16:35',
    '16:40-17:25',
    '17:30-18:15'
]
dfRowNrAndTimeTuples = [
    (1, '8:00-8:45'),
    (2, '8:50-9:35'),
    (3, '9:40-10:25'),
    (4, '10:40-11:25'),
    (5, '11:30-12:15'),
    (6, '12:20-13:05'),
    (7, '13:10-13:55'),
    (8, '14:10-14:55'),
    (9, '15:00-15:45'),
    (10, '15:50-16:35'),
    (11, '16:40-17:25'),
    (12, '17:30-18:15')
]
dfColWeekDayNamesTuples4el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'grupa'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'grupa'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'grupa'), ('Środa', 'nauczyciel'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'grupa'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'grupa'), ('Piątek', 'nauczyciel'), ('Piątek', 'sala')
]
dfColWeekDayNamesTuples5el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'grupa'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'klasa'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'grupa'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'klasa'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'grupa'), ('Środa', 'nauczyciel'), ('Środa', 'klasa'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'grupa'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'klasa'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'grupa'), ('Piątek', 'nauczyciel'), ('Piątek', 'klasa'), ('Piątek', 'sala')
]
dfColNamesTuples = dfRowIndexNamesTuples + dfColWeekDayNamesTuples4el
# dfColNamesTuples = [('Nr', ''), ('Godz', '')] + [(day, attr) for day in weekdays for attr in lessonAttrs]

import numpy as np
dfColWeekDayEmptyRow = {
    ('Poniedziałek', 'przedmiot'): np.nan, ('Poniedziałek', 'grupa'): np.nan, ('Poniedziałek', 'nauczyciel'): np.nan, ('Poniedziałek', 'klasa'): np.nan, ('Poniedziałek', 'sala'): np.nan,
    ('Wtorek', 'przedmiot'): np.nan, ('Wtorek', 'grupa'): np.nan, ('Wtorek', 'nauczyciel'): np.nan, ('Wtorek', 'klasa'): np.nan, ('Wtorek', 'sala'): np.nan,
    ('Środa', 'przedmiot'): np.nan, ('Środa', 'grupa'): np.nan, ('Środa', 'nauczyciel'): np.nan, ('Środa', 'klasa'): np.nan, ('Środa', 'sala'): np.nan,
    ('Czwartek', 'przedmiot'): np.nan, ('Czwartek', 'grupa'): np.nan, ('Czwartek', 'nauczyciel'): np.nan, ('Czwartek', 'klasa'): np.nan, ('Czwartek', 'sala'): np.nan,
    ('Piątek', 'przedmiot'): np.nan, ('Piątek', 'grupa'): np.nan, ('Piątek', 'nauczyciel'): np.nan, ('Piątek', 'klasa'): np.nan, ('Piątek', 'sala'): np.nan }