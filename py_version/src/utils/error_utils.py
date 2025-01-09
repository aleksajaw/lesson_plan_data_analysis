def turnOffFutureWarnings():
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)



def getTraceback(e):
    import traceback
    import re
    fileName, lineNo, funcName, code = traceback.extract_tb(e.__traceback__)[0]
    return f'{re.split(r'[\\/]', fileName)[-1]}\n{lineNo} line: {funcName}\n{code}\n'