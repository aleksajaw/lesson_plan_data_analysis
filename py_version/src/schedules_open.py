from utils import openFileWithDefApp
from constants import scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath, scheduleExcelPath


def openScheduleFilesWithDefApps():
    for excelFilePath in [scheduleExcelPath, scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelSubjectsPath]:
        openFileWithDefApp(excelFilePath)