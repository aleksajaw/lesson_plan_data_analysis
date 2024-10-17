from utils import openFileWithDefApp
from constants import scheduleExcelTeachersPath, scheduleExcelClassroomsPath, scheduleExcelPath


def openScheduleFilesWithDefApps():
    for excelFilePath in [scheduleExcelPath, scheduleExcelTeachersPath, scheduleExcelClassroomsPath]:
        openFileWithDefApp(excelFilePath)