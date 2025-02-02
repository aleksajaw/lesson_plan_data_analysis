from error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleClassesExcelPath
from src.constants.conversion_constants import excelEngineName, draftSheetName, JSONIndentValue
from src.constants.schedule_structures_constants import dfColNamesTuples, timeIndexNames, dayAndAttrNames, dfColWeekDayNamesTuples4el, dfColWeekDayNamesTuples5el, colWithNumbersNames, excelMargin
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
            # Multi-dimensional column names.
            df.columns = MultiIndex.from_tuples(tuples=dfColNamesTuples, names=dayAndAttrNames)

            # Use an empty string instead of null/NaN.
            df = df.fillna('')
            
            # Restore 111 from values like '111.0'.
            df = correctValsInColsWithNumbers(df)
            
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
            # Use an empty string instead of null/NaN
            df = df.fillna('')
            # Restore 111 from values like '111.0'.
            df = correctValsInColsWithNumbers(df)
            
            objOfDfsJSON[sheetName] = df.to_json(orient='split')

    except Exception as e:
        msgText = handleErrorMsg('\nError while converting object of DataFrames to JSON.', getTraceback(e))

    if msgText: print(msgText)

    return json.dumps(objOfDfsJSON, indent=JSONIndentValue)



# EXCEL CONTENT   =>   OBJECT OF DATA FRAMES   =>   JSON
def convertExcelToDfsJSON(excelFilePath=scheduleClassesExcelPath):
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



def correctValsInColsWithNumbers(df=DataFrame, forceCorrect=False):
    if forceCorrect:
        for col in df.columns:
            df[col] = df[col].map(convertFloatToInt)
    
    else:
        for colWithNrTuple in colWithNumbersNames:
            if colWithNrTuple in df.columns:
                df[colWithNrTuple] = df[colWithNrTuple].map(convertFloatToInt)

    return df


# 111.0   =>   111
def convertFloatToInt(value=None):
    isValueFloatAndInt = isinstance(value, float)   and   value.is_integer()

    return int(value)   if isValueFloatAndInt   else   value


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



# Sort the object keys. More below.
def sortObjKeys(dataToSort=None):
    msgText = ''
    try:
        pattern = re.compile(r'\d+')

        for key in dataToSort.keys():
            # sort by numbers (which are keys here) inside list elements,
            # especially for classroom names like _08, s1, 1, 100
            # moreover, it prevents missorting like 1, 10, 100, 2, 20, 200 :)
            #dataToEnter[key].sort( key = lambda x: int( re.findall(r'\d+', x)[0] ) )

            # also add sorting strings between the values with numbers like: 1, s1, st1, 2, _02, s2
            # so we will have s1, s2, st1, _02, 1, 2
            dataToSort[key].sort( key=lambda x: (
                                      # False values are treated as smaller,
                                      # so they will appear earlier in the sorted list
                                      # so at first sort by letters
                                      not x[0].isalpha(),
                                      # put values like _07 before digits
                                      # for easier grouping
                                      x.isdigit(),
                                      x.lower() if isinstance(x, str) and x[0].isalpha()
                                                # sort by first digit in elements
                                                else  int(pattern.search(x).group(0))
                                                      if pattern.search(x)
                                                      # if element does not have digit,
                                                      # use inf(inity) to move element
                                                      # at the end of the sorting here
                                                      else float('inf')
                                  )
                                )
            # convert strings to integer, if it is possible
            dataToSort[key] = [int(x)   if x.isdigit()   else x   for x in dataToSort[key]]
        
    except Exception as e:
        msgText = handleErrorMsg('\nError while sorting schedule owner lists.', getTraceback(e))

    if msgText: print(msgText)

    return dataToSort



# Convert the keys in an object using the order from the listOfOrderedKeys.
def convertObjKeysToDesiredOrder(obj={}, listOfOrderedKeys=[], convertToStr=False):
    objToReturn={}

    for key in listOfOrderedKeys:

        if convertToStr:
            objToReturn[str(key)] = obj[str(key)]

        else:
            objToReturn[key] = obj[key]
    
    return objToReturn



# Filter nd.array
def filterNumpyNdarray(arr=np.ndarray, elToDel=''):
    # convert values to string
    arrAsStr = arr.astype(str)
    filteredArrAsStr = arrAsStr[ arrAsStr != elToDel]
    # remove specific value
    #sortedArr = np.sort( arrAsStr[ arrAsStr != elToDel] )
    
    return np.array([val   for val in filteredArrAsStr])



# Group items by their base names, which are the common parts of some (full) names.
def getPureGroupedList(df=DataFrame, colToGroupBy='names_base', colToCreateList='names'):
    # Group data in Data Frame by unique values in column (index) colToGroupBy.
    # Then, make the list from the values in the column named colToCreateList.
    newDf = None
    dataToReturn = []

    if colToGroupBy in df.index.names   and   colToCreateList in df.columns:
        newDf = df.groupby(colToGroupBy, sort=False)[colToCreateList]
        # Ignore the column names. Get the values as a list. 
        newDfWithoutCols = newDf.apply(list)
        dataToReturn = newDfWithoutCols.to_dict()

    return dataToReturn



# Make the list with the pure values from the column named colToCreateList.
def getPureList(df=DataFrame, colToCreateList='names'):
    newDf = None
    if colToCreateList in df.columns:
        newDf = list(df[colToCreateList])

    return newDf