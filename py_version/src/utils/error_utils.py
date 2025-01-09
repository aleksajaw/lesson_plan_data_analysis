def turnOffFutureWarnings():
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)



def getTraceback(e):
    import traceback
    import re
    import sys

    msgText=''
    fileName, lineNr, fnName, code = traceback.extract_tb(e.__traceback__)[0]
    excType, excValue, excTb = sys.exc_info()

    defaultSpace = '  '
    lineStarter = f'{re.split(r'[\\/]', fileName)[-1]}, line {lineNr} in{defaultSpace}'
    lineSpaces = f'{ len(lineStarter) * ' '}'

    errorName = excType.__name__ + f':{defaultSpace}'
    errorNameLen = len(errorName)
    fnName = fnName + f':{defaultSpace}'
    fnNameLen = len(str(fnName))

    if errorNameLen < fnNameLen:
        diff = fnNameLen-errorNameLen
        errorName = diff * ' ' + errorName
    
    elif errorNameLen > fnNameLen:
        diff = errorNameLen-fnNameLen
        fnName = diff * ' ' + fnName
        
    msgText += '\n'
    msgText += f'{lineStarter}'
    msgText += f'{fnName}'
    msgText += f'{code}'
    msgText += f'\n{lineSpaces}'
    msgText += f'{errorName}'
    msgText += f'{excValue}'
    msgText +='\n'


    return msgText