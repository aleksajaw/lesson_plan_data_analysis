from error_utils import handleErrorMsg, getTraceback
#from src.constants.paths_constants import scheduleClassesExcelPath
from src.constants.conversion_constants import draftSheetName, JSONIndentValue#, excelEngineName
#from src.constants.excel_constants import excelMargin
from src.constants.schedule_structures_constants import dfColNameTuples, dfColNameArrays, timeIndexNames, dayAndAttrNames, colsWithNumbersNameTuples, colsWithNumbersNameArrays#, dfColWeekDayNamesTuples4el, dfColWeekDayNamesTuples5el
import json
import re
from pandas import DataFrame, MultiIndex, Series, Index#, read_excel
import numpy as np


###    CONVERTERS    ###


# DATA   =>   DATA FRAME
def convertToDf(dataToConvert):
    df = None
    msgText=''

    try:
        #if dataToConvert is None:
        #    dataToConvert = {}
        
        df = DataFrame(dataToConvert[1:])
        # Multi-dimensional column names.
        df.columns = MultiIndex.from_tuples(tuples=dfColNameTuples, names=dayAndAttrNames)
        #df.columns = MultiIndex.from_arrays(arrays=dfColNameArrays, names=dayAndAttrNames)

        df = correctDfContent(df)
        
        df.set_index(keys=timeIndexNames, inplace=True)
            
    except Exception as e:
        msgText = handleErrorMsg('\nError while converting data do DataFrame.', getTraceback(e))

    if msgText: print(msgText)  
    
    return df



# DATA   =>   OBJECT OF DATA FRAMES 
def convertToObjOfDfs(dataToConvert):
    if dataToConvert:
        return {sheetName: convertToDf(dataToConvert[sheetName])   for sheetName in dataToConvert}

    else:
        return {draftSheetName: DataFrame()}



# OBJECT OF DATA FRAMES   =>   JSON
def convertObjOfDfsToJSON(dataToConvert):
    msgText = ''
    objOfDfsJSON = {}

    try:
        #if dataToConvert is None:
        #    dataToConvert = {}
        
        for sheetName, df in dataToConvert.items():
            df = correctDfContent(df)
            
            objOfDfsJSON[sheetName] = df.to_json(orient='split')

    except Exception as e:
        msgText = handleErrorMsg('\nError while converting object of DataFrames to JSON.', getTraceback(e))

    if msgText: print(msgText)

    return json.dumps(objOfDfsJSON, indent=JSONIndentValue)



def correctDfContent(df, forceCorrect=False):
    #if df is None:
    #    df = DataFrame
    
    # Use an empty string instead of null/NaN
    df = df.fillna('')
    # Restore 111 from values like '111.0'.
    return correctValsInColsWithNumbers(df, forceCorrect)



def correctValsInColsWithNumbers(df, forceCorrect=False):
    #if df is None:
    #    df = DataFrame
    
    dfColsToCorrectList = df.select_dtypes(include=['object', 'float']).columns.tolist()
    
    if len(dfColsToCorrectList):
        colsList = dfColsToCorrectList   if forceCorrect   else colsWithNumbersNameTuples
        #colsList = dfColsToCorrectList   if forceCorrect   else colsWithNumbersNameArrays
        
        for colWithNrs in colsList:
            if forceCorrect   or   (not forceCorrect   and   colWithNrs in df.columns):

              if 'obj' in str(df[colWithNrs].dtype):
                  df[colWithNrs] = df[colWithNrs].map(convertFloatToInt)
              
              else:
                  df[colWithNrs] = df[colWithNrs].astype(int)

    return df



# 111.0   =>   111
def convertFloatToInt(value):
    isValueFloatAndInt = isinstance(value, float)   and   value.is_integer()

    return int(value)   if isValueFloatAndInt   else   value


# '1'   =>   1
def convertDigitInStrToInt(text):
    return int(text)   if str.isdigit(text)   else text


# DataFrame column with values like
# 3 / 4   =>   '0,75%'
def divisionResultAsPercentage(val1, val2):
    if isinstance(val1, (int, float))   and   isinstance(val2, (int, float)):
        divisionResult = (val1 / val2)
    
    else:
        divisionResult = (val1 / val2).fillna(0)

    return convertDfColValToPercentage(divisionResult)



# DataFrame column with values like
# 0,75   =>   '75%'
def convertDfColValToPercentage(value):
    if isinstance(value, Series):
        return (value * 100).round(2).astype(str) + '%'
    
    elif isinstance(value, (int, float)):
        return f'{round((value * 100), 2)}%'
    
    else:
        return None



# 0,75   =>   '75%'
def convertValToPercentage(value):
    if not isinstance(value, float):
        value = float(value)

    return str(round((value * 100), 2)) + '%'



def convertToRounded(value):
    return round(value, 2)



# 'example', 'example2'   =>   ('example', 'example2')
# ('example'), 'example2'   =>   ('example', 'example2')
# 7, 'example2'   =>   (7, 'example2')
def createTupleFromVals(valList):
    convertedValList = []
    for val in valList:
        # Check if a value is iterable or convert it to one.
        if not isinstance(val, tuple):
            if not hasattr(val, '__iter__')   or   isinstance(val, str):
                val = [val]
            val = tuple(val)

        convertedValList.append(tuple(val))
        
    return sum(convertedValList, ())



# 'example', 'example2'   =>   []'example', 'example2']
# []'example'], 'example2'   =>   []'example', 'example2']
# 7, 'example2'   =>   [7, 'example2']
def createListFromVals(valList):
    convertedValList = []
    # Check if a value is iterable or convert it to one.
    for val in valList:
        if not isinstance(val, list):
            val = list(val)
        
        convertedValList = convertedValList + val

    return convertedValList



# <br>
# <br />   =>   \n
def convertBrInText(text):
    if isinstance(text, str):
        text = text.replace("<br>", "\n").replace("<br />", "\n")

    return text



# <p>
#   <span>hello</span> <span>world!&nbsp;</span>
# </p>
#   =>   helloworld!
def splitHTMLAndRemoveTags(HTMLText):
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
def delInvalidChars(name, target='sheetName'):
    if target=='sheetName':
        invalidScheetNameChars = ['/', '\\', ':', '*', '?', '[', ']']
        # replace invalid characters with character '_'
        return ''.join('_'   if c in invalidScheetNameChars   else c   for c in name)
    
    return name
    


# for example,
# {'key1':[], 'key2':[]}   =>   ['key1', 'key2']
def getListOfKeys(obj):
    #if obj is None:
    #    obj = {}
    
    return list(obj.keys())



# Sort the object keys. More below.
def sortObjKeys(dataToSort):
    msgText = ''

    try:
        #if dataToSort is None:
        #    dataToSort = {}

        for key in dataToSort.keys():
            # sort by numbers (which are keys here) inside list elements,
            # especially for classroom names like _08, s1, 1, 100
            # moreover, it prevents missorting like 1, 10, 100, 2, 20, 200 :)
            #dataToEnter[key].sort( key = lambda x: int( re.findall(r'\d+', x)[0] ) )

            # also add sorting strings between the values with numbers like: 1, s1, st1, 2, _02, s2
            # so we will have s1, s2, st1, _02, 1, 2
            dataToSort[key].sort( key=customSorting )
            # convert strings to integer, if it is possible
            dataToSort[key] = [int(x)   if x.isdigit()   else x   for x in dataToSort[key]]
    
    except Exception as e:
        msgText = handleErrorMsg('\nError while sorting schedule owner lists.', getTraceback(e))

    if msgText: print(msgText)

    return dataToSort



def customSorting(el):
    pattern = re.compile(r'\d+')

    if hasattr(el, '__iter__')   and   not isinstance(el, str):
    #if isinstance(el, tuple):
        el = el[-1]
    
    el = str(el)

    return ( # False values are treated as smaller,
             # so they will appear earlier in the sorted list
             # so at first sort by letters
             not el[0].isalpha(),
             # put values like _07 before digits
             # for easier grouping
             el.isdigit(),
             el.lower()   if isinstance(el, str)   and   el[0].isalpha()
                          # sort by first digit in elements
                          else  int(pattern.search(el).group(0))
                              if pattern.search(el)
                              # if element does not have digit,
                              # use inf(inity) to move element
                              # at the end of the sorting here
                              else float('inf') )



# Convert the keys in an object using the order from the listOfOrderedKeys.
def convertObjKeysToDesiredOrder(obj, listOfOrderedKeys, convertToStr=False):
    #if obj is None:
    #    obj = {}
    
    objToReturn = {}

    for key in listOfOrderedKeys:

        if convertToStr:
            objToReturn[str(key)] = obj[str(key)]

        else:
            objToReturn[key] = obj[key]
    
    return objToReturn



# Filter nd.array
def filterNumpyNdarray(arr, elToDel=''):
    #if arr is None:
    #    arr = np.ndarray
    
    # convert values to string
    arrAsStr = arr.astype(str)
    filteredArrAsStr = arrAsStr[ arrAsStr != elToDel]
    # remove specific value
    #sortedArr = np.sort( arrAsStr[ arrAsStr != elToDel] )
    
    return np.array([val   for val in filteredArrAsStr])



# Group items by their base names, which are the common parts of some (full) names.
def getPureGroupedList(df, colToGroupBy='names_base', colToCreateList='names'):
    #if df is None:
    #    df = DataFrame
    
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
def getPureList(df, colToCreateList='names'):
    #if df is None:
    #    df = DataFrame
    
    newDf = None
    if colToCreateList in df.columns:
        newDf = list(df[colToCreateList])

    return newDf