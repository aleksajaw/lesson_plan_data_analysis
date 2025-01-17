import sys
import os
import subprocess

# Remember to write this name to the .gitignore file.
envName='venv'



###############################################################################################



def createVirtualEnvIfNecessary():
    global envName

    if not os.path.exists(envName):
        
        msgText = f'\nCreating a new virtual enviroment in the directory "{envName}"'
        print(msgText + '...')

        try:
            subprocess.check_call([sys.executable, '-m', 'venv', envName])
            print(msgText + ' ends successfully.')
            return True

        except Exception as e:
            print(f'\nError while {msgText[0].upper() + msgText[1:]}: {e}')
            return False
        
    else:
        print(f'\nThe virtual environment "{envName}" already exists.')
    
    return True



###############################################################################################



def runVirtualEnv():
    global envName
    import platform
    
    command = []
    
    if platform.system() == 'Windows':
        activateScript = os.path.join(envName, 'Scripts', 'activate.bat')
        commandBefore = 'start cmd /K '
        commandMain = f'\"{activateScript}'

    elif platform.system() in ['Linux', 'Darwin']:
        activateScript = os.path.join(envName, 'bin', 'activate')
        commandBefore = 'bash -c '
        commandMain = f'\"source {activateScript}'
    
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
    try:
        
        pythonPath = os.path.join(envName, 'Scripts', 'python.exe')
        commandResult = subprocess.check_output([pythonPath or 'python', '-m', 'pip', 'show', packageName]).decode('utf-8')
        installedVer = None

        for line in commandResult.splitlines():
            if line.startswith('Version:'):
                installedVer = line.split(':')[1].strip()
                break
        
        return not (installedVer == requiredVer)
    
    
    except subprocess.CalledProcessError:
        return True



def installRequirements(requirementsFile='requirements.txt'):
    global envName

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
            pipPath = os.path.join(envName, 'Scripts', 'pip')
            subprocess.check_call([pipPath or 'pip', 'install', packageName])


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