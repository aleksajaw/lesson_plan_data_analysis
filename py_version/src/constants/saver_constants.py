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