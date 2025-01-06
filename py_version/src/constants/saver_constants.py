# DIR PATHS
import os
currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
outputsPath = f'{srcDirPath}/schedules/'


# FILE NAMES
scheduleExcelName = 'schedule.xlsx'
scheduleExcelTeachersName = 'schedule-teachers.xlsx'
scheduleExcelClassroomsName = 'schedule-classrooms.xlsx'
scheduleExcelSubjectsName = 'schedule-subjects.xlsx'
scheduleExcelGroupListsName = 'schedule-group_lists.xlsx'
scheduleJSONName = 'schedule.json'
scheduleDfsJSONName = 'schedule_dfs.json'
scheduleExcelJSONName = 'schedule_dfs_excel.json'


# FILE PATHS
# Excel
scheduleExcelPath = outputsPath + scheduleExcelName
# For Teachers
scheduleExcelTeachersPath = outputsPath + scheduleExcelTeachersName
# For classrooms
scheduleExcelClassroomsPath = outputsPath + scheduleExcelClassroomsName
# For subjects
scheduleExcelSubjectsPath = outputsPath + scheduleExcelSubjectsName
# For schedule group lists
scheduleExcelGroupListsPath = outputsPath + scheduleExcelGroupListsName
# pure scraped data in JSON
scheduleJSONPath = outputsPath + scheduleJSONName
# DataFrames in JSON
scheduleDfsJSONPath = outputsPath + scheduleDfsJSONName
# current Excel in JSON
scheduleExcelJSONPath = outputsPath + scheduleExcelJSONName


# variables for handling pandas' Data Frame and excel
timeIndexes = ['Nr','Godz']
weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
lessonAttrs = ['przedmiot', 'nauczyciel', 'sala']
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
dfColWeekDayNamesTuples = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'nauczyciel'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'nauczyciel'), ('Piątek', 'sala')
]
dfColNamesTuples = dfRowIndexNamesTuples + dfColWeekDayNamesTuples
# dfColNamesTuples = [('Nr', ''), ('Godz', '')] + [(day, attr) for day in weekdays for attr in lessonAttrs]