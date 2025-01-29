from src.utils.files_utils import openFileWithDefApp
from src.constants.paths_constants import allScheduleExcelPaths, allScheduleGroupedExcelPaths, allScheduleOverviewExcelPaths, allScheduleGroupedOverviewExcelPaths


def openScheduleFilesWithDefApps():
    filePaths = allScheduleExcelPaths + allScheduleGroupedExcelPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)


def openOverviewFilesWithDefApps():
    filePaths = allScheduleOverviewExcelPaths + allScheduleGroupedOverviewExcelPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)