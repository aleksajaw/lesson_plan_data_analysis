from src.handlers.schedules_scraper import getClassesDataFromSchoolWebPage
from src.handlers.scraper_saver import loadClassesDataVariables, createOrEditMainExcelFile, getClassesDataDfs
from src.handlers.schedules_creator import createScheduleExcelFiles
from src.handlers.files_opener import openScheduleFilesWithDefApps, openOverviewFilesWithDefApps
from src.handlers.overviews_creator import createScheduleOverviews
from src.constants.scraper_constants import schoolsWebInfo



def scrapeSchoolWebs():
    
    for schoolWebInfo in [schoolsWebInfo['lojagiellonczyk']]:

        classesData = getClassesDataFromSchoolWebPage(schoolWebInfo)

        if classesData:
            loadClassesDataVariables(classesData)
            createOrEditMainExcelFile(schoolWebInfo)
            createScheduleExcelFiles(getClassesDataDfs(), schoolWebInfo)
            createScheduleOverviews(schoolWebInfo)
            #openScheduleFilesWithDefApps()
            #openOverviewFilesWithDefApps()
