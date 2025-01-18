import sys
import os
import subprocess

# Remember to write this name to the .gitignore file.
envName='venv'
essentialEnvPaths = { 'win32':  [ os.path.join(envName, 'Scripts', 'python.exe'),
                                  os.path.join(envName, 'Scripts', 'activate') ],
                      'linux':  [ os.path.join(envName, 'bin', 'python'),
                                  os.path.join(envName, 'bin', 'activate') ],
                      'darwin': [ os.path.join(envName, 'bin', 'python'),
                                  os.path.join(envName, 'bin', 'activate') ] }
currSys = sys.platform
currEssenialEnvPaths = essentialEnvPaths[currSys]



###############################################################################################



def createVirtualEnvIfNecessary(forceReinstall=False):
    global envName, essentialEnvPaths

    isAnyPathMissing = any( (not os.path.exists(essPath))   for essPath in currEssenialEnvPaths )
    isThereAnyDirInside = not any( os.path.isdir(os.path.join(envName, entry))    for entry in os.listdir(envName))
    
    if forceReinstall   or   isAnyPathMissing   or   isThereAnyDirInside:
        
        msgText = f'\nCreating a new virtual enviroment in the directory "{envName}"'
        print(msgText + '...')

        try:
            subprocess.check_call([sys.executable, '-m', 'venv', envName])

            isThereAnyDirInside = not any( os.path.isdir(os.path.join(envName, entry))    for entry in os.listdir(envName))
            isAnyPathMissing = any( (not os.path.exists(essPath))   for essPath in currEssenialEnvPaths )

            if isAnyPathMissing   or   isThereAnyDirInside:
                
                import shutil
                shutil.rmtree(envName)
                print(f'\nHave to remove old {envName} directory.')
                setupEnvironment(True)
            
            print('Ends successfully.')
            return True

        except Exception as e:
            print(f'\nError while {msgText[0].upper() + msgText[1:]}: {e}')
            return False
        
    else:
        print(f'\nThe virtual environment "{envName}" already exists.')
    
    return True



###############################################################################################



def runVirtualEnv():
    global envName, essentialEnvPaths
    
    command = []
    
    if currSys == "win32":
        commandBefore = 'start cmd /K '
        commandMain = f'\"{currEssenialEnvPaths[1]}'

    elif currSys in ['linux', 'darwin']:
        commandBefore = 'bash -c '
        commandMain = f'\"source {currEssenialEnvPaths[1]}'
    
    try:
        command = commandBefore + commandMain + '   &&   python -c \"import main; main.main()\"   &&   deactivate   &&   exit\"'
        subprocess.check_call(command, shell=True)
        print(f'The virtual environment "{envName}" activated.')
        sys.exit()
        return True
        
    except subprocess.CalledProcessError:
        print(f'Error while activating the virtual environment "{envName}".')
        setupEnvironment(True)
        return False



###############################################################################################



def doesPackageNeedInstallation(packageName='', requiredVer=''):
    global essentialEnvPaths
    try:
        
        envPythonPath = currEssenialEnvPaths[0]
        # stdout=subprocess.PIPE: Captures the standard output (i.e., the data that the process would normally print to the screen).
        # stderr=subprocess.PIPE: Captures the standard error stream (i.e., the errors that the process would normally print to the screen).
        commandResult = subprocess.check_output([envPythonPath, '-m', 'pip', 'show', packageName], stderr=subprocess.PIPE).decode('utf-8')
        installedVer = None

        for line in commandResult.splitlines():
            if line.startswith('Version:'):
                installedVer = line.split(':')[1].strip()
                break
        
        return not (installedVer == requiredVer)
    
    except subprocess.CalledProcessError:
        return True
    
    except FileNotFoundError:
        print(f'\nFile {envPythonPath} not found.')
        setupEnvironment(True)



def installRequirements(requirementsFile='requirements.txt'):
    global envName, essentialEnvPaths

    packagesToInstall=[]

    try:
        with open(requirementsFile, 'r') as file:
            
            for line in file:
                packageLine = line.strip().split('==')
                packageName = packageLine[0]
                packageVer = packageLine[1]

                if packageName   and   doesPackageNeedInstallation(packageName, packageVer):
                    packagesToInstall.append(packageName)
            
            if len(packagesToInstall):
                raise ImportError


    except ImportError as e:
        print(f'\nSome requirements need to be installed: {packagesToInstall}')
        for packageName in packagesToInstall:
            envPythonPath = currEssenialEnvPaths[0]
            try:
                # stdout=subprocess.PIPE: Captures the standard output (i.e., the data that the process would normally print to the screen).
                # stderr=subprocess.PIPE: Captures the standard error stream (i.e., the errors that the process would normally print to the screen).
                subprocess.check_call([envPythonPath, '-m', 'pip', 'install', packageName], stderr=subprocess.PIPE)
            
            except subprocess.CalledProcessError:
                print('Error while installing requirements.')
                setupEnvironment(True)

    except FileNotFoundError:
        print(f'\nFile {requirementsFile} not found.')
        return False


    else:
        print('\nAll of the requirements already exist.')

    return True



###############################################################################################



def addToSysPath(basePath='', innerFolderName=''):
    folderPathToAdd = ( basePath  if    not innerFolderName
                                  else  basePath / innerFolderName)

    if not folderPathToAdd.exists():
        print(f'\nThe directory "{folderPathToAdd}" does not exist.')
        sys.exit()

    else:
        sys.path.append(str(folderPathToAdd))
        return True



def addAllOfTheProjectFolders():
    from pathlib import Path
    
    projectRoot = Path(__file__).resolve().parent
    srcFolder = projectRoot / 'src'

    folderList = [ 'constants', 'handlers', 'logs', 'schedules', 'utils' ]
        
    for folderName in folderList:
        addToSysPath(srcFolder, folderName)
    
    return True



###############################################################################################



def setupEnvironment(forceReinstall=False, requirementsFile='requirements.txt'):
    if forceReinstall:
        print('Reinstall environment.')
    
    try:
        noErrors = createVirtualEnvIfNecessary(forceReinstall)
        if noErrors:
            noErrors = installRequirements(requirementsFile)
          
    except Exception as e:
        print(f'Error: {e}')
        sys.exit()



###############################################################################################



def main():
    if addAllOfTheProjectFolders():
    
        from src import ( getClassesDataFromSchoolWebPage,
                          loadClassesDataVariables, createOrEditMainExcelFile, getClassesDataDfs,
                          createOtherScheduleExcelFiles,
                          openScheduleFilesWithDefApps )
        
        #turnOffFutureWarnings()

        classesData = getClassesDataFromSchoolWebPage()

        if classesData:
            loadClassesDataVariables(classesData)
            createOrEditMainExcelFile()
            createOtherScheduleExcelFiles(getClassesDataDfs())
            openScheduleFilesWithDefApps()



if __name__ == '__main__':
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', action='store_true', help='Run the configuration or add the missing modules.')
    args = parser.parse_args()

    if args.setup:
        setupEnvironment()

    try:
        runVirtualEnv()
        
    except Exception as e:
        print(f'Error: {e}\nTry command:\n\npython main.py --setup')