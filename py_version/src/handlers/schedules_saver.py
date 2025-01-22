from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants import scheduleExcelClassesPath, excelEngineName, scheduleExcelClassesJSONPath, scheduleClassesDfsJSONPath, scheduleClassesJSONPath
from src.utils import convertToObjOfDfs, convertObjOfDfsToJSON, createDraftSheetIfNecessary, convertExcelToDfsJSON, writeObjOfDfsToExcel, delDraftIfNecessary, compareAndUpdateFile, autoFormatScheduleExcel
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

    currExcelAsDfsJSON = convertExcelToDfsJSON()
    
    try:
        if str(currExcelAsDfsJSON) != str(classesDataDfsJSON):
            with ExcelWriter(scheduleExcelClassesPath, mode='w+', engine=excelEngineName) as writer:
                
                try:
                    writeObjOfDfsToExcel(writer, scheduleExcelClassesPath, classesDataDfs)
                    autoFormatScheduleExcel(writer.book, scheduleExcelClassesPath)

                    try:
                        delDraftIfNecessary()

                    except Exception as draftError:
                        print( handleErrorMsg( f'\nError while deleting the draft sheet in main Excel file: {draftError}' ) )


                except Exception as writeError:
                    print( handleErrorMsg( f'\nError while writing to the main Excel file: {writeError}' ) )

        else:
            print('Nothing to be updated in the main Excel file.')


    except Exception as e:
        print( handleErrorMsg( f'\nError while handling the main Excel file.', getTraceback(e) ) )


    # to avoid issues, compare file contents
    # & update if it's neccessarry
    compareAndUpdateFile(scheduleExcelClassesJSONPath, currExcelAsDfsJSON)
    compareAndUpdateFile(scheduleClassesDfsJSONPath, classesDataDfsJSON)
    compareAndUpdateFile(scheduleClassesJSONPath, classesDataJSON)


def getClassesDataDfs():
    return classesDataDfs