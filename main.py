import sys
import os
import subprocess
import time

startTime=None



# Remember to write this name to the .gitignore file.
envName='venv'
essentialEnvPaths = { 'win32':  [ os.path.join(envName, 'Scripts', 'python.exe'),
                                  os.path.join(envName, 'Scripts', 'activate') ],
                      'linux':  [ os.path.join(envName, 'bin', 'python'),
                                  os.path.join(envName, 'bin', 'activate') ],
                      'darwin': [ os.path.join(envName, 'bin', 'python'),
                                  os.path.join(envName, 'bin', 'activate') ] }
currSys = sys.platform
currEssentialEnvPaths = essentialEnvPaths[currSys]



######################################################################################################################################################



def checkIfNotExists(pathEl=''):
    return not os.path.exists(pathEl)



def checkIsAnyPathMissing():
    global currEssentialEnvPaths
    return any( checkIfNotExists(essPath)   for essPath in currEssentialEnvPaths )



def checkIsDir(baseName='', entry=''):
    return os.path.isdir(os.path.join(baseName, entry))



def checkIsAnyDirInside():
    global envName
    doesEnvDirExist = not checkIfNotExists(envName)
    dirEntries = os.listdir(envName)
    return any( checkIsDir(envName, entry)   for entry in dirEntries )   if doesEnvDirExist   else False



######################################################################################################################################################



def createVirtualEnvIfNecessary(forceReinstall=False):
    global envName, currEssentialEnvPaths
        
    if forceReinstall  or  checkIfNotExists(envName)  or  checkIsAnyPathMissing()  or  not checkIsAnyDirInside():
        
        msgText = f'Creating a new virtual enviroment in the directory "{envName}"'
        print('\n' + msgText + '...')

        try:
            subprocess.check_call(f'{sys.executable} -m venv {envName}')

            if checkIsAnyPathMissing():
                import shutil
                shutil.rmtree(envName)
                print(f'\nHad to remove the old {envName} directory.')
                setupEnvironment(True)
            
            # Ensure that pip is upgraded to the latest version.
            subprocess.check_call(f'{currEssentialEnvPaths[0]} -m pip install --upgrade pip')
            # Automatic installation of the requirements.
            subprocess.check_call(f'{currEssentialEnvPaths[0]} -m pip install -r requirements.txt')

            print('Ends successfully.')


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
        cBefore = 'cmd /c \"'

    elif currSys in ['linux', 'darwin']:
        cBefore = 'bash -c \"source '
    
    try:
        # Remove the comment characters in this function if you want to automate 
        # installation of the missing virtual environment or needed packages.
        # Remember to correct the indentations.
    #if not checkIsAnyPathMissing()   and   checkIsAnyDirInside():
        cActivatePart = currEssentialEnvPaths[1]
        cInfo = f'echo The virtual environment \"{envName}\" activated.'
        cMain = 'python -c \"import main; main.main()\"'
        cDeactivate = 'deactivate'

        command = cBefore + cActivatePart + ' && ' + cInfo + ' && ' + cMain + ' && ' + cDeactivate + '\"'

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
    dirPathToAdd = ( basePath  if    not innerDirName
                                  else  os.path.join(basePath, innerDirName) )

    if checkIfNotExists(dirPathToAdd):
        print(f'\nThe directory "{dirPathToAdd}" does not exist.')
        
        execTime  = (time.perf_counter() - startTime)
        print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')

        raise Exception(FileNotFoundError)

    else:
        sys.path.append(str(dirPathToAdd))
    
    return True



def addAllOfTheProjectDirs():
    
    projectRoot = os.path.dirname(__file__)
    srcDir = os.path.join(projectRoot, 'src')

    for dirName in ['logs', 'schedules']:
        addToSysPath(projectRoot, dirName)

    dirList = [ 'constants', 'handlers', 'utils' ]
        
    for dirName in dirList:
        addToSysPath(srcDir, dirName)
    
    return True



######################################################################################################################################################



def setupEnvironment(forceReinstall=False, requirementsFile='requirements.txt'):
    if forceReinstall:
        print('\nReinstall environment.')
    
    try:
      createVirtualEnvIfNecessary(forceReinstall)
        
    except Exception as e:
        print(f'\nError: {e}')

        execTime  = (time.perf_counter() - startTime)
        print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')



######################################################################################################################################################



def main():
    if addAllOfTheProjectDirs():
    
        from src.handlers.schedules_scraper import getClassesDataFromSchoolWebPage
        from src.handlers.schedules_saver import loadClassesDataVariables, createOrEditMainExcelFile, getClassesDataDfs
        from src.handlers.schedules_creator import createScheduleExcelFiles
        from src.handlers.schedules_opener import openScheduleFilesWithDefApps
        
        #turnOffFutureWarnings()

        classesData = getClassesDataFromSchoolWebPage()

        if classesData:
            loadClassesDataVariables(classesData)
            createOrEditMainExcelFile()
            createScheduleExcelFiles(getClassesDataDfs())
            #openScheduleFilesWithDefApps()



def chooseStart(args=None):
    global startTime
    startTime = time.perf_counter()
    
    if args.setup:
        setupEnvironment(args.force)

    # The 2nd part of the condition prevents the situation where '--force' is the only flag being used.
    # Also, it allows running the program without any flags.
    if args.start   or   (not args.setup and not args.force):
        try:
            runVirtualEnv(args.force)
            
        except Exception as e:
            print(f'\nError: {e}\n\nTry command: python main.py --setup\n')
        
        execTime  = (time.perf_counter() - startTime)
        if round(execTime%60, 2):
            print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')
    
    else:
        execTime  = (time.perf_counter() - startTime)
        if round(execTime%60, 2):
            print(f'\nProgram took {int(execTime//60)} min and {execTime%60:.2f} sec.')

        raise Exception('The "--force" argument cannot be used alone.')



if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('--setup', action='store_true', help='Run the automatic setup or add the missing or corrupted packages.')
    parser.add_argument('--force', action='store_true', help='Force the action.')
    parser.add_argument('--start', action='store_true', help='Activate the virtual environment.')
    args = None

    try:
        args = parser.parse_args()
        chooseStart(args)

    except Exception as e:
        print(f'\nSomething went wrong. It seems like you are trying to use unrecognized arguments or a combination of them.\n\n{e}\n')
        parser.print_help()

        sys.exit(1)