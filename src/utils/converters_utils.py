from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleExcelClassesPath
from src.constants.conversion_constants import excelEngineName, draftSheetName, JSONIndentValue
from src.constants.schedule_structures_constants import dfColNamesTuples, timeIndexNames, dayAndAttrNames, dfColWeekDayNamesTuples4el, dfColWeekDayNamesTuples5el, excelMargin
import json
import re
from pandas import DataFrame, MultiIndex, read_excel
import numpy as np


###    CONVERTERS    ###


# DATA   =>   DATA FRAME
def convertToDf(dataToConvert=None):
    df = None
    msgText=''

    try:
        if(dataToConvert):
            df = DataFrame(dataToConvert[1:])
            # multi-dimensional column names
            df.columns = MultiIndex.from_tuples(tuples=dfColNamesTuples, names=dayAndAttrNames)

            # use empty string instead of null/NaN
            df = df.fillna('')
            
            # Restore 111 from '111.0'.
            # The problem is probably caused by the creation of the DataFrame.
            df = df.map(convertFloatToInt)
            
            df.set_index(keys=timeIndexNames, inplace=True)
            
    except Exception as e:
        msgText = handleErrorMsg('\nError while converting data do DataFrame.', getTraceback(e))

    if msgText: print(msgText)  
    
    return df



# DATA   =>   OBJECT OF DATA FRAMES 
def convertToObjOfDfs(dataToConvert=None):
    if dataToConvert:
        return {sheetName: convertToDf(dataToConvert[sheetName])   for sheetName in dataToConvert}

    else:
        return {draftSheetName: DataFrame()}



# OBJECT OF DATA FRAMES   =>   JSON
def convertObjOfDfsToJSON(dataToConvert=None):
    msgText = ''
    objOfDfsJSON = {}

    try:
        for sheetName, df in dataToConvert.items():
            # use empty string instead of null/NaN
            df = df.fillna('')
            objOfDfsJSON[sheetName] = df.to_json(orient='split')

    except Exception as e:
        msgText = handleErrorMsg('\nError while converting object of DataFrames to JSON.', getTraceback(e))

    if msgText: print(msgText)

    return json.dumps(objOfDfsJSON, indent=JSONIndentValue)



# EXCEL CONTENT   =>   OBJECT OF DATA FRAMES   =>   JSON
def convertExcelToDfsJSON(excelFilePath=scheduleExcelClassesPath):
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
                    df = df.drop(unnamedColIndices, axis=1)

                dataToConvert[sheetName] = df.to_json(orient='split')

        except Exception as e:
            msgText = handleErrorMsg('\nError converting existing schedule Excel file to JSON.', getTraceback(e))

        if msgText: print(msgText)


    return json.dumps(dataToConvert, indent=JSONIndentValue)



# JSON WITH OBJECT OF DATA FRAMES
#    =>   OBJECT OF DATA FRAMES
def convertDfsJSONToObjOfDfs(JSONFilePath = ''):
    msgText=''
    objOfDfs = {}

    try:
        with open(JSONFilePath, 'r') as file:
            objOfDfsTemp = json.load(file)
            
            
        for dfName, dfData in objOfDfsTemp.items():
          dfData = json.loads(dfData)
          dfData['index'] = MultiIndex.from_tuples(dfData['index'], names=timeIndexNames)

          try:
              dfData['columns'] = MultiIndex.from_tuples(dfColWeekDayNamesTuples5el, names=dayAndAttrNames)
              objOfDfs[dfName] = DataFrame(data=dfData['data'], index=dfData['index'], columns=dfData['columns'])

          except:
              dfData['columns'] = MultiIndex.from_tuples(dfColWeekDayNamesTuples4el, names=dayAndAttrNames)
              objOfDfs[dfName] = DataFrame(data=dfData['data'], index=dfData['index'], columns=dfData['columns'])


    except Exception as e:
        msgText = handleErrorMsg('Error while converting JSON file with Data Frames to object with Data Frames.', getTraceback(e))
    
    if msgText: print(msgText)

    return objOfDfs



# 111.0   =>   111
def convertFloatToInt(value=None):
    isValueFloat = isinstance(value, float)   and   value.is_integer()
    if isValueFloat:
        return int(value)
    return value


# '1'   =>   1
def convertDigitInStrToInt(text=''):
    return int(text)   if str.isdigit(text)   else text


# <br>
# <br />   =>   \n
def convertBrInText(text=''):
    if isinstance(text, str):
        text = text.replace("<br>", "\n").replace("<br />", "\n")

    return text



# <p>
#   <span>hello</span> <span>world!&nbsp;</span>
# </p>
#   =>   helloworld!
def splitHTMLAndRemoveTags(HTMLText=''):
    #patternSub = r'&nbsp;|\s+'
    patternSub = r'&nbsp;'
    HTMLTextStripped = re.sub(patternSub, '', HTMLText)
    textParts = []
    convertedTextParts = []

    if HTMLTextStripped:
        # pattern to get e.g. string 'text' from <span class='p'>text</span>
        pattern = r'<[^>]+>([^<]+)</[^>]+>'
        textParts = re.findall(pattern, HTMLTextStripped)   or   [HTMLTextStripped]
        convertedTextParts = [convertDigitInStrToInt(part)   for part in textParts]      

    return convertedTextParts



# 'part 1/2'    =>   'part 1_2'
# or '[part1]'   =>   '_part1_'
def delInvalidChars(name='', target='sheetName'):
    if target=='sheetName':
        invalidScheetNameChars = ['/', '\\', ':', '*', '?', '[', ']']
        # replace invalid characters with character '_'
        return ''.join('_'   if c in invalidScheetNameChars   else c   for c in name)
    else:
        return name
    


# for example,
# {'key1':[], 'key2':[]}   =>   ['key1', 'key2']
def getListOfKeys(obj={}):
    return list(obj.keys())



def filterNumpyNdarray(arr=np.ndarray, elToDel=''):
    # convert values to string
    arrAsStr = arr.astype(str)
    filteredArrAsStr = arrAsStr[ arrAsStr != elToDel]
    # remove specific value
    #sortedArr = np.sort( arrAsStr[ arrAsStr != elToDel] )
    
    return np.array([val   for val in filteredArrAsStr])



def getPureGroupList(df=DataFrame, colToGroupBy='names_base', colToCreateList='names'):
    # Group data in Data Frame by unique values in column (index) colToGroupBy.
    # Then, make list from colToCreateList.
    newDf = None
    if colToGroupBy in df.index.names   and   colToCreateList in df.columns:
        newDf = df.groupby(colToGroupBy, sort=False)[colToCreateList].apply(list).to_dict()

    return newDf



def getPureList(df=DataFrame, colToCreateList='names'):
    # Make list from colToCreateList.
    newDf = None
    if colToCreateList in df.columns:
        newDf = list(df[colToCreateList])

    return newDf