from src.utils.files_utils import openFileWithDefApp
from src.constants.paths_constants import allScheduleExcelPaths, allScheduleExcelGroupedPaths, allScheduleExcelOverviewPaths, allScheduleExcelGroupedOverviewPaths


def openScheduleFilesWithDefApps():
    filePaths = allScheduleExcelPaths + allScheduleExcelGroupedPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)


def openOverviewFilesWithDefApps():
    filePaths = allScheduleExcelOverviewPaths + allScheduleExcelGroupedOverviewPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)