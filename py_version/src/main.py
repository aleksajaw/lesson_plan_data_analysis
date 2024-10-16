from schedules_scraper import getClassesDataFromSchoolWebPage
from schedules_saver import loadClassesDataVariables, createOrEditExcelFile, getClassesDataDfs
from schedules_creator import test

def main():
    
    classesData = getClassesDataFromSchoolWebPage()
    loadClassesDataVariables(classesData)
    createOrEditExcelFile()
    test(getClassesDataDfs())

if __name__ == "__main__":
    main()