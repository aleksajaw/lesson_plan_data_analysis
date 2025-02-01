import sys
import os
import subprocess
import time

startTime=None



# Remember to write this name to the .gitignore file.
# Have to change envName to the two-level directory name due to the problem with removing the venv/Scripts/python.exe.
envName=os.path.join('venv','venv')
essentialEnvPaths = { 'win32':  [ os.path.join(envName, 'Scripts', 'python.exe'),
                                  os.path.join(envName, 'Scripts', 'activate') ],
                      'linux':  [ os.path.join(envName, 'bin', 'python'),
                                  os.path.join(envName, 'bin', 'activate') ],
                      'darwin': [ os.path.join(envName, 'bin', 'python'),
                                  os.path.join(envName, 'bin', 'activate') ] }
currSys = sys.platform
currEssentialEnvPaths = essentialEnvPaths[currSys]



######################################################################################################################################################



def checkIfExists(pathEl=''):
    return os.path.exists(pathEl)



def checkIfNotExists(pathEl=''):
    return not checkIfExists(pathEl)



def checkIsAnyPathMissing():
    global currEssentialEnvPaths
    return any( checkIfNotExists(essPath)   for essPath in currEssentialEnvPaths )



def checkIsDir(baseName='', entry=''):
    return os.path.isdir(os.path.join(baseName, entry))



def checkIsAnyDirInside():
    global envName
    doesEnvDirExist = checkIfExists(envName)
    dirEntries = os.listdir(envName)
    return any( checkIsDir(envName, entry)   for entry in dirEntries )   if doesEnvDirExist   else False



######################################################################################################################################################



def createVirtualEnvIfNecessary(forceReinstall=False):
    global envName, currEssentialEnvPaths
        
    if forceReinstall  or  checkIfNotExists(envName)  or  checkIsAnyPathMissing()  or  not checkIsAnyDirInside():
        
        msgText = f'Creating a new virtual enviroment in the directory "{envName}"'
        print('\n' + msgText + '...')

        try:
            subprocess.check_call(f'"{sys.executable}" -m venv {envName}')

            if checkIsAnyPathMissing():
                removeEnvironment()
                setupEnvironment(True)
            
            # Ensure that pip is upgraded to the latest version.
            subprocess.check_call(f'"{currEssentialEnvPaths[0]}" -m pip install --upgrade pip')
            # Automatic installation of the requirements.
            subprocess.check_call(f'"{currEssentialEnvPaths[0]}" -m pip install -r requirements.txt')

            print(f'\n{msgText} ends successfully.')

        except Exception as e:
            print(f'\nError while {msgText[0].lower() + msgText[1:]}: {e}')
            raise Exception(e)
        
    else:
        print(f'\nThe virtual environment "{envName}" already exists.')

    return True



######################################################################################################################################################



def runVirtualEnv(forceStart=False):
    global envName, currEssentialEnvPaths
    
    command = []

    if currSys == "win32":
        cBefore = 'cmd /c "'

    elif currSys in ['linux', 'darwin']:
        cBefore = 'bash -c "source '
    
    try:
        # Remove the comment characters in this function if you want to automate 
        # installation of the missing virtual environment or needed packages.
        # Remember to correct the indentations.
    #if not checkIsAnyPathMissing()   and   checkIsAnyDirInside():
        cActivatePart = f'"{currEssentialEnvPaths[1]}"'
        cInfo = f'echo The virtual environment \"{envName}\" activated.'
        cMain = 'python -c "import main; main.main()"'
        cDeactivate = 'deactivate'

        command = cBefore + cActivatePart + ' && ' + cInfo + ' && ' + cMain + ' && ' + cDeactivate + '"'

        subprocess.run(command, shell=True, check=True, text=True, stderr=subprocess.PIPE)


    except (subprocess.CalledProcessError, UnicodeDecodeError) as e:
        errorMsg = ( '\n' + e.stderr   if hasattr(e, 'stderr')
                                       else '' )
        print(f'\nError while activating the virtual environment "{envName}".{errorMsg}')

        # The 1st version of quitting the function.
        # Automatically (re)install the environment if the program cannot run without any issues.
        if forceStart:
            setupEnvironment(True)
            runVirtualEnv()



######################################################################################################################################################



def addToSysPath(basePath='', innerDirName=''):
    dirPathToAdd = ( basePath   if    not innerDirName
                                else  os.path.join(basePath, innerDirName) )

    if checkIfNotExists(dirPathToAdd):
        print(f'\nThe directory "{dirPathToAdd}" does not exist.')
        
        execTime = (time.perf_counter() - startTime)
        if round(execTime%60, 2):
            print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')

        raise Exception(FileNotFoundError)

    else:
        sys.path.append(str(dirPathToAdd))
    
    return True



def addAllOfTheProjectDirs():
    projectRoot = os.path.dirname(__file__)
    srcDir = os.path.join(projectRoot, 'src')

    for dirName in ['logs', 'processing_files', 'documents']:
        addToSysPath(projectRoot, dirName)

    dirList = [ 'constants', 'handlers', 'utils' ]
        
    for dirName in dirList:
        addToSysPath(srcDir, dirName)
    
    return True



######################################################################################################################################################



def removeEnvironment(endHere=False):
    global envName
    
    if checkIfExists(envName):
        import shutil

        try:
            shutil.rmtree(envName)
            print(f'\nThe directory "{envName}" has been removed.')

        except Exception as e:
            msgText = f'\nError while removing the environmental directory "{envName}".'
            msgText += f' Probably you will have to remove some files manually.\n{e}'
            print(msgText)
            shutil.rmtree(envName, ignore_errors=True)
            sys.exit()

    else:
        print(f'\nThe directory "{envName}" does not exist.')

    if endHere:
        execTime = (time.perf_counter() - startTime)
        if round(execTime%60, 2):
            print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')



def removeFiles(endHere=False, isClearLogs=False):
    projectRoot = os.path.dirname(__file__)
    
    if not isClearLogs:
        #schedulesDir = os.path.join(projectRoot, 'schedules')
        documentsDir = os.path.join(projectRoot, 'documents')
        processingFilesDir = os.path.join(projectRoot, 'processing_files')
        dirList = [documentsDir, processingFilesDir]
    else:
        logsDir = os.path.join(projectRoot, 'logs')
        dirList = [logsDir]

    dirListBasenames = [os.path.basename(dirName)   for dirName in dirList]

    try:
        for mainDir in dirList:
            for dirPath, dirNames, fileNames in os.walk(mainDir):
                for fileName in fileNames:
                    if fileName != '.gitkeep'   and   'prototypes' not in dirPath:
                        filePath = os.path.join(dirPath, fileName)
                        os.remove(filePath)

        print(f'\nFiles inside the { ', '.join(f'"{directory}"' for directory in dirListBasenames) } directory have been removed, if they exist.')

    except Exception as e:
        print(f'\nError while removing the files in the directory { ', '.join(f'"{directory}"' for directory in dirListBasenames) }: {e}')

    if endHere:
        execTime = (time.perf_counter() - startTime)
        if round(execTime%60, 2):
            print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')



######################################################################################################################################################



def setupEnvironment(forceReinstall=False, requirementsFile='requirements.txt'):
    if forceReinstall:
        print('\nReinstall environment.')
    
    try:
        createVirtualEnvIfNecessary(forceReinstall)
        
    except Exception as e:
        print(f'\nError while setting up the environment: {e}')

        execTime = (time.perf_counter() - startTime)
        if round(execTime%60, 2):
            print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')



######################################################################################################################################################



def main():
    if addAllOfTheProjectDirs():
    
        from src.handlers.schedules_scraper import getClassesDataFromSchoolWebPage
        from src.handlers.schedules_saver import loadClassesDataVariables, createOrEditMainExcelFile, getClassesDataDfs
        from src.handlers.schedules_creator import createScheduleExcelFiles
        from src.handlers.files_opener import openScheduleFilesWithDefApps, openOverviewFilesWithDefApps
        from src.handlers.overviews_creator import createScheduleOverviews
        
        #turnOffFutureWarnings()

        classesData = getClassesDataFromSchoolWebPage()

        if classesData:
            loadClassesDataVariables(classesData)
            createOrEditMainExcelFile()
            createScheduleExcelFiles(getClassesDataDfs())
            createScheduleOverviews()
            #openScheduleFilesWithDefApps()
            #openOverviewFilesWithDefApps()



def chooseStart(args=None):
    global startTime
    startTime = time.perf_counter()
    
    isStart = args.start
    isSetup = args.setup
    isSetupOrStart = isSetup or isStart

    isClearLogs = args.clear_logs
    isRmFiles = args.rm_files
    isRmVenv = args.rm_venv
    isRemove = isRmFiles or isRmVenv
    isRemoveOnly = isRemove and not isSetupOrStart
    isClearLogsOnly = isClearLogs and not (isRemove or isSetupOrStart)

    isForce = args.force
    isForceOnly = isForce and not isSetupOrStart

    noFlags =  not any(vars(args).values())

    if isClearLogs:
        removeFiles(isClearLogsOnly, True)

    if isRmFiles:
        removeFiles(isRemoveOnly and not isRmVenv)
    
    if isRmVenv:
        removeEnvironment(isRemoveOnly)

    if isSetupOrStart   or   noFlags:
        if isSetup:
            setupEnvironment(isForce)

        # The 2nd part of the condition prevents the situation where '--force' is the only flag being used.
        # Also, it allows running the program without any flags.
        if isStart   or   noFlags:
            try:
                runVirtualEnv(isForce)
                
            except Exception as e:
                print(f'\nError: {e}\n\nTry command: python main.py --setup\n')
            
            execTime = (time.perf_counter() - startTime)
            if round(execTime%60, 2):
                print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')
        
        elif not isSetup:
            execTime = (time.perf_counter() - startTime)
            if round(execTime%60, 2):
                print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')

    if isForceOnly:
        raise Exception('The "--force" argument cannot be used alone.')



if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('--setup', action='store_true', help='Run the automatic setup or add the missing or corrupted packages.')
    parser.add_argument('--start', action='store_true', help='Activate the virtual environment.')
    parser.add_argument('--force', action='store_true', help='Force the action.')
    parser.add_argument('--rm-files', action='store_true', help='Remove recursively all of the output files placed in /documents and /processing_files.')
    parser.add_argument('--rm-venv', action='store_true', help=f'Remove the directory for the virtual environment {envName}.')
    parser.add_argument('--clear-logs', action='store_true', help='Remove the logs.')
    args = None

    try:
        args = parser.parse_args()
        chooseStart(args)

    except Exception as e:
        print(f'\nSomething went wrong. It seems like you are trying to use unrecognized arguments or a combination of them.\n\n{e}\n')
        parser.print_help()

        sys.exit(1)