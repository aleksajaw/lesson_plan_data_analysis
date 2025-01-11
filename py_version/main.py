from src import (  getClassesDataFromSchoolWebPage,
                        loadClassesDataVariables, createOrEditMainExcelFile, getClassesDataDfs,
                        createOtherScheduleExcelFiles,
                        openScheduleFilesWithDefApps )

import sys
from pathlib import Path


projectRoot = Path(__file__).resolve().parent
srcFolder = projectRoot / 'src'

sys.path.append(str(srcFolder))

for fName in ['constants', 'handlers', 'schedules', 'utils']:
    sys.path.append(str(srcFolder / fName))



def main():
    #turnOffFutureWarnings()

    classesData = getClassesDataFromSchoolWebPage()
    if classesData:
        loadClassesDataVariables(classesData)
        createOrEditMainExcelFile()
        createOtherScheduleExcelFiles(getClassesDataDfs())
        openScheduleFilesWithDefApps()


if __name__ == "__main__":
    main()