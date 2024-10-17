from schedules_scraper import getClassesDataFromSchoolWebPage
from schedules_saver import loadClassesDataVariables, createOrEditMainExcelFile, getClassesDataDfs
from schedules_creator import createOtherScheduleExcelFiles
from schedules_open import openScheduleFilesWithDefApps

def main():
    
    classesData = getClassesDataFromSchoolWebPage()
    loadClassesDataVariables(classesData)
    createOrEditMainExcelFile()
    createOtherScheduleExcelFiles(getClassesDataDfs())
    openScheduleFilesWithDefApps()

if __name__ == "__main__":
    main()