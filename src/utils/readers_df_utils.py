from error_utils import handleErrorMsg, getTraceback
#from src.constants.paths_constants import scheduleClassesExcelPath
from src.constants.conversion_constants import excelEngineName, JSONIndentValue
from src.constants.excel_constants import excelMargin
from src.constants.schedule_structures_constants import timeIndexNames, dayAndAttrNames, dfColWeekDayNameTuples5el, dfColWeekDayNameTuples4el, dfColWeekDayNameArrays5el, dfColWeekDayNameArrays4el
from src.constants.overview_constants import overviewsByDaysColIndexNames, overviewsByHoursColIndexNames
from df_utils import removeDfUnnamedCols
from pandas import read_excel, MultiIndex, DataFrame, IndexSlice
import json



def readExcelFileAsObjOfDfs(excelFilePath):
    from files_utils import doesFileExist
    dataToConvert = {}
    msgText = ''

    if doesFileExist(excelFilePath):
        try:
            excelData = read_excel( io=excelFilePath, sheet_name=None, engine=excelEngineName, keep_default_na=False,
                                    header=[excelMargin['row'], excelMargin['row']+1], index_col=[excelMargin['col'], excelMargin['col']+1])

            for sheetName, df in excelData.items():
                excelData[sheetName] = removeDfUnnamedCols(df)

            dataToConvert = excelData


        except Exception as e:
            msgText = handleErrorMsg('\nError converting existing schedule Excel file to JSON.', getTraceback(e))

        if msgText: print(msgText)

    return dataToConvert



# JSON WITH OBJECT OF DATA FRAMES
#    =>   OBJECT OF DATA FRAMES
def readDfsJSONAsObjOfDfs(JSONFilePath):
    msgText=''
    objOfDfs = {}

    try:
        with open(JSONFilePath, 'r') as file:
            objOfDfsTemp = json.load(file)
            
            
        for dfName, dfData in objOfDfsTemp.items():
          dfData = json.loads(dfData)
          dfData['index'] = MultiIndex.from_tuples(tuples=dfData['index'], names=timeIndexNames)
          #dfData['index'] = MultiIndex.from_arrays(arrays=dfData['index'], names=timeIndexNames)

          dfData['columns'] = MultiIndex.from_tuples(tuples=dfData['columns'], names=dayAndAttrNames)
          #dfData['columns'] = MultiIndex.from_arrays(arrays=dfData['columns'], names=dayAndAttrNames)
          objOfDfs[dfName] = DataFrame(data=dfData['data'], index=dfData['index'], columns=dfData['columns'])


    except Exception as e:
        msgText = handleErrorMsg('Error while reading JSON file with Data Frames as object with Data Frames.', getTraceback(e))
    
    if msgText: print(msgText)

    return objOfDfs



# JSON WITH OBJECT WITH LISTS OF MULTIPLE DATA FRAME OBJECTS
#    =>   OBJECT WITH LISTS OF MULTIPLE CONVERTED DATA FRAMES
def readMultiDfsJSONAsObjOfDfObjLists(JSONFilePath):
    msgText=''

    objOfMultiDfs = {}
    try:
        with open(JSONFilePath, 'r') as file:
            objOfMultiDfsTemp = json.load(file)

        for sheetName, dfObjList in objOfMultiDfsTemp.items():
          objOfMultiDfs[sheetName] = []

          for dfObj in dfObjList:
              objTemp = dfObj.copy()

              dfTemp = json.loads(objTemp['df'])
              indexNames = overviewsByDaysColIndexNames   if len(dfTemp['columns'][0]) == len(overviewsByDaysColIndexNames)   else overviewsByHoursColIndexNames
              dfTemp = DataFrame( index=MultiIndex.from_tuples(dfTemp['index']), columns=MultiIndex.from_tuples(dfTemp['columns'], names=indexNames), data=dfTemp['data'] )
              
              objTemp['df'] = dfTemp

              objOfMultiDfs[sheetName].append(objTemp)
              

    except Exception as e:
        msgText = handleErrorMsg('Error while reading JSON file as object with lists of converted Data Frame objects.', getTraceback(e))
    
    if msgText: print(msgText)

    return objOfMultiDfs



# EXCEL CONTENT
#    =>   OBJECT OF DATA FRAMES
#       =>   JSON
def readExcelAsDfsJSON(excelFilePath):
    from files_utils import doesFileExist
    dataToConvert = {}
    msgText = ''

    if doesFileExist(excelFilePath):
        try:
            excelData = read_excel( io=excelFilePath, sheet_name=None, engine=excelEngineName, keep_default_na=False,
                                    header=[excelMargin['row'], excelMargin['row']+1], index_col=[excelMargin['col'], excelMargin['col']+1])

            for sheetName, df in excelData.items():
                df = removeDfUnnamedCols(df)
                dataToConvert[sheetName] = df.to_json(orient='split')


        except Exception as e:
            msgText = handleErrorMsg('\nError converting existing schedule Excel file to JSON.', getTraceback(e))

        if msgText: print(msgText)

    return json.dumps(dataToConvert, indent=JSONIndentValue)