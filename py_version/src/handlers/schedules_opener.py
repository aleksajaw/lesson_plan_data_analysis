from src.utils import openFileWithDefApp
from src.constants import scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelClassesPath, scheduleListsExcelOwnersGrouped


def openScheduleFilesWithDefApps():
    scheduleExcelPaths = [  scheduleExcelClassesPath,
                            scheduleExcelTeachersPath,
                            scheduleExcelClassroomsPath,
                            scheduleExcelSubjectsPath,
                            scheduleListsExcelOwnersGrouped ]
    
    for excelFilePath in scheduleExcelPaths:
        openFileWithDefApp(excelFilePath)