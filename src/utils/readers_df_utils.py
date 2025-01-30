from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleClassesExcelPath
from src.constants.conversion_constants import excelEngineName
from src.constants.schedule_structures_constants import excelMargin
from converters_utils import convertExcelToDfsJSON
from pandas import read_excel



def readExcelFileAsObjOfDfs(excelFilePath=scheduleClassesExcelPath):
    from files_utils import doesFileExist
    dataToConvert = {}
    msgText = ''

    if doesFileExist(excelFilePath):
        try:
            excelData = read_excel( io=excelFilePath, sheet_name=None, engine=excelEngineName, keep_default_na=False,
                                    header=[excelMargin['row'], excelMargin['row']+1], index_col=[excelMargin['col'], excelMargin['col']+1])

            for sheetName, df in excelData.items():
                unnamedColIndices = [col   for i, col in enumerate(df.columns)   if 'Unnamed' in str(col[0])]

                if len(unnamedColIndices):
                    excelData[sheetName] = df.drop(unnamedColIndices, axis=1)

            dataToConvert = excelData
        except Exception as e:
            msgText = handleErrorMsg('\nError converting existing schedule Excel file to JSON.', getTraceback(e))

        if msgText: print(msgText)


    return dataToConvert