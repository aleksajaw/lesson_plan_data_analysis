import os


def doesFileExist(filePath=''):
    return bool (os.path.isfile(filePath))


def compareAndUpdateFile(filePath='', dataToCompare=''):
    if bool(filePath) and bool(dataToCompare):
        try:
            with open(filePath, "r+") as file:
                if not (file.read()==dataToCompare):
                    file.seek(0)
                    file.write(dataToCompare)
                    # make sure to delete old redundant value
                    file.truncate()
                    file.close()
                    print(f'{filePath} updated with new data.')

        except FileNotFoundError:
            with open(filePath, 'w') as file:
              file.write(dataToCompare)
              file.close()
              print(f'{filePath} updated with new data.')