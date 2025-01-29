from src.utils.files_utils import openFileWithDefApp
from src.constants.paths_constants import allScheduleExcelPaths, allScheduleGroupedExcelPaths, allScheduleOverviewResourcesExcelPaths, allScheduleGroupedOverviewResourcesExcelPaths


def openScheduleFilesWithDefApps():
    filePaths = allScheduleExcelPaths + allScheduleGroupedExcelPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)


def openOverviewFilesWithDefApps():
    filePaths = allScheduleOverviewResourcesExcelPaths + allScheduleGroupedOverviewResourcesExcelPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)