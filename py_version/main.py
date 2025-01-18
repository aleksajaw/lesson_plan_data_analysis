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



def createVirtualEnvIfNecessary():
    global envName, essentialEnvPaths

    if any( (not os.path.exists(essPath))   for essPath in currEssenialEnvPaths ):
        
        msgText = f'\nCreating a new virtual enviroment in the directory "{envName}"'
        print(msgText + '...')

        try:
            subprocess.check_call([sys.executable, '-m', 'venv', envName])

            if any( (not os.path.exists(essPath))   for essPath in currEssenialEnvPaths ): 
                import shutil
                shutil.rmtree(envName)
                print(f'\nHave to remove old {envName} directory.')
                createVirtualEnvIfNecessary()
            
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
        subprocess.run(command, shell=True, check=True)
        print(f'The virtual environment "{envName}" activated.')
        sys.exit()
        return True
        
    except subprocess.CalledProcessError:
        print(f'Error while activating the virtual environment "{envName}".')
        return False



###############################################################################################



def doesPackageNeedInstallation(packageName='', requiredVer=''):
    global essentialEnvPaths
    try:
        
        envPythonPath = currEssenialEnvPaths[0]
        commandResult = subprocess.check_output([envPythonPath, '-m', 'pip', 'show', packageName]).decode('utf-8')
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
        createVirtualEnvIfNecessary()



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
            subprocess.check_call([envPythonPath, '-m', 'pip', 'install', packageName])


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



def setupEnvironment(requirementsFile='requirements.txt'):
    try:
        noErrors = createVirtualEnvIfNecessary()
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