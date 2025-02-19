from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleClassesExcelPath, scheduleClassesExcelDfsJSONPath, scheduleClassesDfsJSONPath, scheduleClassesBaseJSONPath
from src.constants.conversion_constants import excelEngineName, JSONIndentValue
from src.utils.converters_utils import convertToObjOfDfs, convertObjOfDfsToJSON
from src.utils.excel_utils import createDraftSheetIfNecessary, delDraftIfNecessary
from src.utils.excel_styles_utils import autoFormatScheduleExcel
from src.utils.files_utils import compareAndUpdateFile, extendFilePathWithCurrSchoolTitle
from src.utils.writers_df_utils import writeObjOfDfsToExcel
from src.utils.readers_df_utils import readExcelAsDfsJSON
import json
from pandas import ExcelWriter
import os


currSchoolWebInfo = None
classesDataJSON = ''
classesDataDfs = None
classesDataDfsJSON = ''


def setCurrSchoolWebInfo(schoolWebInfo):
    global currSchoolWebInfo

    currSchoolWebInfo = schoolWebInfo



def getCurrSchoolWebInfo():
    global currSchoolWebInfo

    return currSchoolWebInfo



def loadClassesDataVariables(classesData):
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    classesDataJSON = json.dumps(classesData, indent=JSONIndentValue)
    classesDataDfs = convertToObjOfDfs(classesData)
    classesDataDfsJSON = convertObjOfDfsToJSON(classesDataDfs)



def createOrEditMainExcelFile(schoolWebInfo):
    
    global classesDataJSON, classesDataDfs, classesDataDfsJSON

    convertedScheduleClassesExcelPath = extendFilePathWithCurrSchoolTitle(scheduleClassesExcelPath)

    createDraftSheetIfNecessary(convertedScheduleClassesExcelPath)

    currExcelAsDfsJSON = readExcelAsDfsJSON(convertedScheduleClassesExcelPath)

    try:
        if not currExcelAsDfsJSON.strip()   or   ( currExcelAsDfsJSON.strip() != classesDataDfsJSON.strip() ):
            with ExcelWriter(convertedScheduleClassesExcelPath, mode='w+', engine=excelEngineName) as writer:
                
                try:
                    writeObjOfDfsToExcel(writer, convertedScheduleClassesExcelPath, classesDataDfs)
                    wb = writer.book
                    autoFormatScheduleExcel(wb)

                    try:
                        delDraftIfNecessary(wb, convertedScheduleClassesExcelPath)

                    except Exception as draftError:
                        print( handleErrorMsg( f'\nError while deleting the draft sheet in main Excel file: {draftError}' ) )


                except Exception as writeError:
                    print( handleErrorMsg( f'\nError while writing to the main Excel file: {writeError}' ) )

        else:
            print(f'\nNothing to be updated in the {(os.path.splitext(convertedScheduleClassesExcelPath)[1][1:]).upper()} file   {os.path.basename(convertedScheduleClassesExcelPath)}.')



    except Exception as e:
        print( handleErrorMsg( f'\nError while handling the main Excel file.', getTraceback(e) ) )


    # to avoid issues, compare file contents
    # & update if it's neccessarry
    compareAndUpdateFile(extendFilePathWithCurrSchoolTitle(scheduleClassesExcelDfsJSONPath), currExcelAsDfsJSON)
    compareAndUpdateFile(extendFilePathWithCurrSchoolTitle(scheduleClassesDfsJSONPath), classesDataDfsJSON)
    compareAndUpdateFile(extendFilePathWithCurrSchoolTitle(scheduleClassesBaseJSONPath), classesDataJSON)

    return classesDataDfs