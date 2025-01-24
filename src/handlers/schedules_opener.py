from src.utils import openFileWithDefApp
from src.constants import scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelClassesPath, scheduleListsExcelOwnersGroupedPath, scheduleExcelTeachersGroupedPath, scheduleExcelClassroomsGroupedPath, scheduleExcelSubjectsGroupedPath


def openScheduleFilesWithDefApps():
    scheduleExcelPaths = [  scheduleExcelClassesPath,
                            scheduleExcelTeachersPath,
                            scheduleExcelClassroomsPath,
                            scheduleExcelSubjectsPath,
                            scheduleListsExcelOwnersGroupedPath,
                            scheduleExcelTeachersGroupedPath,
                            scheduleExcelClassroomsGroupedPath,
                            scheduleExcelSubjectsGroupedPath ]
    
    for excelFilePath in scheduleExcelPaths:
        openFileWithDefApp(excelFilePath)