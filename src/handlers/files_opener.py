from src.utils.files_utils import openFileWithDefApp
from src.constants.paths_constants import allScheduleExcelPaths, allScheduleGroupedExcelPaths, allScheduleResourceAllocExcelPaths, allScheduleGroupedResourceAllocExcelPaths


def openScheduleFilesWithDefApps():
    filePaths = allScheduleExcelPaths + allScheduleGroupedExcelPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)


def openOverviewFilesWithDefApps():
    filePaths = allScheduleResourceAllocExcelPaths + allScheduleGroupedResourceAllocExcelPaths
    for filePath in filePaths:
        openFileWithDefApp(filePath)