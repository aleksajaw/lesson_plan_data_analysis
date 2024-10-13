from schedules_scraper import getClassesDataFromSchoolWebPage
from schedules_saver import loadClassesDataVariables, createOrEditExcelFile


def main():
    
    classesData = getClassesDataFromSchoolWebPage()
    loadClassesDataVariables(classesData)
    createOrEditExcelFile()


if __name__ == "__main__":
    main()