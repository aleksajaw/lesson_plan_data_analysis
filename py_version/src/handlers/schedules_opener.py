from src.utils import openFileWithDefApp
from src.constants import scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelClassesPath, scheduleListsExcelOwnersGrouped, scheduleExcelTeachersGroupedPath, scheduleExcelClassroomsGroupedPath, scheduleExcelSubjectsGroupedPath


def openScheduleFilesWithDefApps():
    scheduleExcelPaths = [  scheduleExcelClassesPath,
                            scheduleExcelTeachersPath,
                            scheduleExcelClassroomsPath,
                            scheduleExcelSubjectsPath,
                            scheduleListsExcelOwnersGrouped,
                            scheduleExcelTeachersGroupedPath,
                            scheduleExcelClassroomsGroupedPath,
                            scheduleExcelSubjectsGroupedPath ]
    
    for excelFilePath in scheduleExcelPaths:
        openFileWithDefApp(excelFilePath)