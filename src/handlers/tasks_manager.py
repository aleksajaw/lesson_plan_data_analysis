from src.handlers.schedules_scraper import getClassesDataFromSchoolWebPage, resetGlobalClassesData
from src.handlers.scraper_saver import setCurrSchoolWebInfo, loadClassesDataVariables, createOrEditMainExcelFile
from src.handlers.schedules_creator import createScheduleExcelFiles
from src.handlers.files_opener import openScheduleFilesWithDefApps, openOverviewFilesWithDefApps
from src.handlers.overviews_creator import createScheduleOverviews
from src.constants.scraper_constants import schoolsWebInfo



def scrapeSchoolWebs():
    
    #for schoolWebInfo in [info   for info in schoolsWebInfo   if info['title']=='lojagiellonczyk']:
    for schoolWebInfo in schoolsWebInfo:

        setCurrSchoolWebInfo(schoolWebInfo)
        classesData = getClassesDataFromSchoolWebPage(schoolWebInfo)

        if classesData:
            loadClassesDataVariables(classesData)
            classesDataDfs = createOrEditMainExcelFile(schoolWebInfo)
            globalSchedules = createScheduleExcelFiles(classesDataDfs, schoolWebInfo)
            createScheduleOverviews(globalSchedules, schoolWebInfo)
            #openScheduleFilesWithDefApps()
            #openOverviewFilesWithDefApps()
        
        resetGlobalClassesData()
