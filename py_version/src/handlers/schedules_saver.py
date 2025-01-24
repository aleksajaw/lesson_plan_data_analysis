from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants import scheduleExcelClassesPath, excelEngineName, scheduleExcelClassesDfsJSONPath, scheduleClassesDfsJSONPath, scheduleClassesJSONPath, JSONIndentValue
from src.utils import convertToObjOfDfs, convertObjOfDfsToJSON, createDraftSheetIfNecessary, convertExcelToDfsJSON, writeObjOfDfsToExcel, delDraftIfNecessary, compareAndUpdateFile, autoFormatScheduleExcel
import json
from pandas import ExcelWriter
import os


classesDataJSON = ''
classesDataDfs = None
classesDataDfsJSON = ''


def loadClassesDataVariables(classesData):
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    classesDataJSON = json.dumps(classesData, indent=JSONIndentValue)
    classesDataDfs = convertToObjOfDfs(classesData)
    classesDataDfsJSON = convertObjOfDfsToJSON(classesDataDfs)



def createOrEditMainExcelFile():
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    createDraftSheetIfNecessary()

    currExcelAsDfsJSON = convertExcelToDfsJSON()

    try:
        if currExcelAsDfsJSON.strip() != classesDataDfsJSON.strip():
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
            print(f'\nNothing to be updated in the {(os.path.splitext(scheduleExcelClassesPath)[1][1:]).upper()} file   {os.path.basename(scheduleExcelClassesPath)}.')



    except Exception as e:
        print( handleErrorMsg( f'\nError while handling the main Excel file.', getTraceback(e) ) )


    # to avoid issues, compare file contents
    # & update if it's neccessarry
    compareAndUpdateFile(scheduleExcelClassesDfsJSONPath, currExcelAsDfsJSON)
    compareAndUpdateFile(scheduleClassesDfsJSONPath, classesDataDfsJSON)
    compareAndUpdateFile(scheduleClassesJSONPath, classesDataJSON)



def getClassesDataDfs():
    return classesDataDfs