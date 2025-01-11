def turnOffFutureWarnings():
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)



def getTraceback(e):
    import traceback
    import re
    import sys
    import inspect

    msgText=''
    # extract useful data from exception traceback
    fileName, lineNr, fnName, code = traceback.extract_tb(e.__traceback__)[0]
    excType, excValue, excTb = sys.exc_info() # exception info
    # list of tuples, each element representing a frame in the call stack;
    # each tuple contains information about one level of the function call
    stack = inspect.stack()
    previousFrame = stack[1].frame
    if previousFrame:
        # local variables from previous frame as reversed list using [::-1]
        # list sorted in the order of the most recently declared variable
        localVars = [item   for item in previousFrame.f_locals.items()   if item[0] not in ['e', 'msgText']][::-1]
    else:
        localVars = []

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
    msgText += '\n'
    
    if localVars:
        msgText += 'Local variables during the error:\n'
        for key, val in localVars:
            msgText += f'{key}: {val}'
            msgText += '\n'


    return msgText