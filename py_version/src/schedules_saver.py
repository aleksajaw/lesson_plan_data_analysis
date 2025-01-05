from constants import scheduleExcelPath, excelEngineName, scheduleExcelJSONPath, scheduleDfsJSONPath, scheduleJSONPath
from utils import convertToObjOfDfs, convertObjOfDfsToJSON, createDraftSheetIfNecessary, convertCurrExcelToDfsJSON, writeObjOfDfsToExcel, delDraftIfNecessary, compareAndUpdateFile, autoFormatExcelFile
#, colLetterToNr
import json
from pandas import ExcelWriter


classesDataJSON = ''
classesDataDfs = None
classesDataDfsJSON = ''


def loadClassesDataVariables(classesData):
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    classesDataJSON = json.dumps(classesData, indent=4)
    classesDataDfs = convertToObjOfDfs(classesData)
    classesDataDfsJSON = convertObjOfDfsToJSON(classesDataDfs)


def createOrEditMainExcelFile():
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    createDraftSheetIfNecessary()

    currExcelAsDfsJSON = convertCurrExcelToDfsJSON()
    
    try:
        if str(currExcelAsDfsJSON) != str(classesDataDfsJSON):
            with ExcelWriter(scheduleExcelPath, mode='w+', engine=excelEngineName) as writer:
                
                try:
                    writeObjOfDfsToExcel(writer, classesDataDfs)
                    autoFormatExcelFile(writer.book, scheduleExcelPath)

                    try:
                        delDraftIfNecessary()

                    except Exception as draftError:
                        print(f"Error while deleting the draft sheet in main Excel file: {draftError}")


                except Exception as writeError:
                    print(f"Error while writing to the main Excel file: {writeError}")

        else:
            print('Nothing to be updated in the main Excel file.')


    except Exception as e:
        print(f"Error while handling the main Excel file: {e}")


    # to avoid issues, compare file contents
    # & update if it's neccessarry
    compareAndUpdateFile(scheduleExcelJSONPath, currExcelAsDfsJSON)
    compareAndUpdateFile(scheduleDfsJSONPath, classesDataDfsJSON)
    compareAndUpdateFile(scheduleJSONPath, classesDataJSON)


def getClassesDataDfs():
    return classesDataDfs