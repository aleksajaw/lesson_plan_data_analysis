def turnOffFutureWarnings():
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)



def getTraceback(e):
    import traceback
    import re
    import sys
    import inspect

    msgText=''
    # exception info
    excType, excValue, excTb = sys.exc_info()

    # The line below converts a traceback object into readable information about call stack frames
    # (a list of tuples). Each tuple contains details about one level of the function call.
    excTraceback = traceback.extract_tb(e.__traceback__)
    # frame where the exception was raised
    fileName, lineNr, fnName, code = excTraceback[0]
    
    # Similar to traceback.extract_tb(e.__traceback__), but inspect.stack() additionally
    # includes a frame object and works even if no exception has occurred.
    stack = inspect.stack()
    previousFrame = stack[1].frame
    if previousFrame:
        # The local variables from the previous frame as a reversed list using [::-1].
        # The list is sorted in the order of the most recently declared variables.
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