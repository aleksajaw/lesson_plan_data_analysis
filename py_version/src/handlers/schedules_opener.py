from src.utils import openFileWithDefApp
from src.constants import scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelClassesPath, scheduleListsExcelOwnersGrouped, scheduleExcelGroupsPath


def openScheduleFilesWithDefApps():
    scheduleExcelPaths = [  scheduleExcelClassesPath,
                            scheduleExcelTeachersPath,
                            scheduleExcelClassroomsPath,
                            scheduleExcelSubjectsPath,
                            scheduleListsExcelOwnersGrouped,
                            scheduleExcelGroupsPath ]
    
    for excelFilePath in scheduleExcelPaths:
        openFileWithDefApp(excelFilePath)