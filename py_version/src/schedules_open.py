from utils import openFileWithDefApp
from constants import scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelPath, scheduleExcelGroupListsPath


def openScheduleFilesWithDefApps():
    scheduleExcelPaths = [  scheduleExcelPath,
                            scheduleExcelTeachersPath,
                            scheduleExcelClassroomsPath,
                            scheduleExcelSubjectsPath,
                            scheduleExcelGroupListsPath ]
    
    for excelFilePath in scheduleExcelPaths:
        openFileWithDefApp(excelFilePath)