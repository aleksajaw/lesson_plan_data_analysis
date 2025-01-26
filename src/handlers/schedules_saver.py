from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleExcelClassesPath, scheduleExcelClassesDfsJSONPath, scheduleClassesDfsJSONPath, scheduleClassesBaseJSONPath
from src.constants.conversion_constants import excelEngineName, JSONIndentValue
from src.utils.converters_utils import convertToObjOfDfs, convertObjOfDfsToJSON, convertExcelToDfsJSON
from src.utils.excel_utils import createDraftSheetIfNecessary, delDraftIfNecessary
from src.utils.excel_styles_utils import autoFormatScheduleExcel
from src.utils.files_utils import compareAndUpdateFile
from src.utils.writers_df_utils import writeObjOfDfsToExcel
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
        if not currExcelAsDfsJSON.strip()   or   ( currExcelAsDfsJSON.strip() != classesDataDfsJSON.strip() ):
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
    compareAndUpdateFile(scheduleClassesBaseJSONPath, classesDataJSON)



def getClassesDataDfs():
    return classesDataDfs