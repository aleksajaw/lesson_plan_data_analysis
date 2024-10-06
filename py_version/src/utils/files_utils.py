import os

def doesFileExist(filePath=''):
    return bool (os.path.isfile(filePath))