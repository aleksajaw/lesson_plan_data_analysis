# DIR PATHS
import os
currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
projectRoot = os.path.dirname(srcDirPath)
#schedulePath = os.path.join(srcDirPath, 'schedules')
schedulePath = os.path.join(projectRoot, 'schedules')
logsPath = os.path.join(projectRoot, 'logs')


# FILE NAMES
scheduleExcelClassesName = 'schedule_classes.xlsx'
scheduleExcelTeachersName = 'schedule_teachers.xlsx'
scheduleExcelClassroomsName = 'schedule_classrooms.xlsx'
scheduleExcelSubjectsName = 'schedule_subjects.xlsx'
scheduleExcelGroupsName = 'schedule_groups.xlsx'

scheduleExcelClassesGroupedName = 'schedule_classes-grouped.xlsx'
scheduleExcelTeachersGroupedName = 'schedule_teachers-grouped.xlsx'
scheduleExcelClassroomsGroupedName = 'schedule_classrooms-grouped.xlsx'
scheduleExcelSubjectsGroupedName = 'schedule_subjects-grouped.xlsx'
scheduleListsExcelOwnersGroupedName = 'schedule-lists_owners-grouped.xlsx'

scheduleClassesJSONName = 'schedule_classes.json'
scheduleClassesDfsJSONName = 'dfs_schedule-classes.json'
scheduleExcelClassesJSONName = 'dfs-excel_schedule-classes.json'


# FILE PATHS
# Excel For Classes
scheduleExcelClassesPath = os.path.join(schedulePath, scheduleExcelClassesName)
# For Teachers
scheduleExcelTeachersPath =  os.path.join(schedulePath, scheduleExcelTeachersName)
# For classrooms
scheduleExcelClassroomsPath =  os.path.join(schedulePath, scheduleExcelClassroomsName)
# For subjects
scheduleExcelSubjectsPath =  os.path.join(schedulePath, scheduleExcelSubjectsName)
# For groups: grouped all of the above
scheduleExcelGroupsPath =  os.path.join(schedulePath, scheduleExcelGroupsName)

# Excel For Classes grouped
scheduleExcelClassesGroupedPath =  os.path.join(schedulePath, scheduleExcelClassesGroupedName)
# For Teachers grouped
scheduleExcelTeachersGroupedPath =  os.path.join(schedulePath, scheduleExcelTeachersGroupedName)
# For classrooms grouped
scheduleExcelClassroomsGroupedPath =  os.path.join(schedulePath, scheduleExcelClassroomsGroupedName)
# For subjects grouped
scheduleExcelSubjectsGroupedPath =  os.path.join(schedulePath, scheduleExcelSubjectsGroupedName)
# For schedule lists with owner grouped
scheduleListsExcelOwnersGrouped =  os.path.join(schedulePath, scheduleListsExcelOwnersGroupedName)

# pure scraped data in JSON
scheduleClassesJSONPath =  os.path.join(schedulePath, scheduleClassesJSONName)
# DataFrames in JSON
scheduleClassesDfsJSONPath =  os.path.join(schedulePath, scheduleClassesDfsJSONName)
# current Excel in JSON
scheduleExcelClassesJSONPath =  os.path.join(schedulePath, scheduleExcelClassesJSONName)


# variables for handling pandas' Data Frame and excel
timeIndexNames = ['Nr','Godz']
weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
lessonAttrs3el = ['przedmiot', 'nauczyciel', 'sala']
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
dfColWeekDayNamesTuples3el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'nauczyciel'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'nauczyciel'), ('Piątek', 'sala')
]
dfColWeekDayNamesTuples4el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'klasa'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'klasa'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'nauczyciel'), ('Środa', 'klasa'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'klasa'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'nauczyciel'), ('Piątek', 'klasa'), ('Piątek', 'sala')
]
dfColNamesTuples = dfRowIndexNamesTuples + dfColWeekDayNamesTuples3el
# dfColNamesTuples = [('Nr', ''), ('Godz', '')] + [(day, attr) for day in weekdays for attr in lessonAttrs]

import numpy as np
dfColWeekDayEmptyRow = {
    ('Poniedziałek', 'przedmiot'): np.nan, ('Poniedziałek', 'nauczyciel'): np.nan, ('Poniedziałek', 'klasa'): np.nan, ('Poniedziałek', 'sala'): np.nan,
    ('Wtorek', 'przedmiot'): np.nan, ('Wtorek', 'nauczyciel'): np.nan, ('Wtorek', 'klasa'): np.nan, ('Wtorek', 'sala'): np.nan,
    ('Środa', 'przedmiot'): np.nan, ('Środa', 'nauczyciel'): np.nan, ('Środa', 'klasa'): np.nan, ('Środa', 'sala'): np.nan,
    ('Czwartek', 'przedmiot'): np.nan, ('Czwartek', 'nauczyciel'): np.nan, ('Czwartek', 'klasa'): np.nan, ('Czwartek', 'sala'): np.nan,
    ('Piątek', 'przedmiot'): np.nan, ('Piątek', 'nauczyciel'): np.nan, ('Piątek', 'klasa'): np.nan, ('Piątek', 'sala'): np.nan }