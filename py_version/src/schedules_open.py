from utils import openFileWithDefApp
from constants import scheduleExcelTeachersPath, scheduleExcelPath


def openScheduleFilesWithDefApps():
    for excelFilePath in [scheduleExcelPath, scheduleExcelTeachersPath]:
        openFileWithDefApp(excelFilePath)