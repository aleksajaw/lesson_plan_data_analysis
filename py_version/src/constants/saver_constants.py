# DIR PATHS
import os
currDirPath = os.path.dirname(__file__)
srcDirPath = os.path.dirname(currDirPath)
outputsPath = f'{srcDirPath}/schedules/'


# FILE NAMES
scheduleExcelName = 'schedule.xlsx'
scheduleJSONName = 'schedule.json'
scheduleDfsJSONName = 'schedule_dfs.json'
scheduleExcelJSONName = 'schedule_dfs_excel.json'


# FILE PATHS
# Excel
scheduleExcelPath = outputsPath + scheduleExcelName
# pure scraped data in JSON
scheduleJSONPath = outputsPath + scheduleJSONName
# DataFrames in JSON
scheduleDfsJSONPath = outputsPath + scheduleDfsJSONName
# current Excel in JSON
scheduleExcelJSONPath = outputsPath + scheduleExcelJSONName


# variables for handling pandas' Data Frame and excel
timeIndexes = ['Nr','Godz']
weekDays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
lessonAttr = ['przedmiot', 'nauczyciel', 'sala']
dfRowIndexNamesTuples = [
    ('Nr', ''),
    ('Godz', '')
]
dfColWeekDayNamesTuples = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'nauczyciel'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'nauczyciel'), ('Piątek', 'sala')
]
dfColNamesTuples = dfRowIndexNamesTuples + dfColWeekDayNamesTuples
# dfColNamesTuples = [('Nr', ''), ('Godz', '')] + [(day, attr) for day in weekDays for attr in lessonAttr]