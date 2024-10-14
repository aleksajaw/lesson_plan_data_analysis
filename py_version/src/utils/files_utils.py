import os
from constants import scheduleExcelPath
from openpyxl import load_workbook
from openpyxl.styles import Alignment as openpyxlAlignment
from openpyxl.utils import column_index_from_string



def doesFileExist(filePath=''):
    msgText = f'File   {os.path.basename(filePath)}   '
    doesFileExistBool = bool (os.path.isfile(filePath))

    if doesFileExistBool:
        msgText += 'exists.'
    else:
        msgText += 'does not exist.'

    print(msgText)

    return doesFileExistBool



def compareAndUpdateFile(filePath='', dataToCompare=''):
    
    isFileChanged = False
    if bool(filePath) and bool(dataToCompare):
        msgText = ''

        try:
            with open(filePath, "r+") as file:
                
                if not (file.read()==dataToCompare):
                    file.seek(0)
                    file.write(dataToCompare)
                    # make sure to delete old redundant value
                    file.truncate()
                    msgText = f'\nFile   {os.path.basename(filePath)}   updated with new data.'
                    isFileChanged = True
                    
                else:
                    msgText = f'\nNothing to be updated in file   {os.path.basename(filePath)}.'

                file.close()
                print(msgText)

        except FileNotFoundError as e:
            
            with open(filePath, 'w') as file:
              file.write(dataToCompare)
              file.close()

              print(f'File   {os.path.basename(filePath)}   not found. Created a new file and complete it with data.')
        
        except Exception as e:
            print('Error while comparing and updating file content: ', e)


        return isFileChanged



def autoFormatExcelFile():
    from excel_utils import get1stNotMergedCell

    try:
                
        wb = load_workbook(scheduleExcelPath)
        
        if (wb):
            rowsCounter = 0


            for ws in wb.worksheets:

                rowsCounter+=1
                rowsLines = {}
                colsLength = {}


                for col in ws.columns:

                    colLetter = get1stNotMergedCell(col).column_letter
                    colIndex = column_index_from_string(colLetter)
                    
                    # init content length for specific column in worksheet
                    colsLength[colIndex] = 1


                    for cell in col:

                        if cell.row not in rowsLines:
                            rowsLines[cell.row] = 1

                        maxRowLines = rowsLines[cell.row]
                        maxColLength = colsLength[cell.column]
                        
                        if isinstance(cell.value, str) and '\n' in cell.value:

                            linesCount = cell.value.count('\n') + 1
                            rowsLines[cell.row] = max(maxRowLines, linesCount)
                            temp = cell.value.split('\n')

                            for t in temp:
                                colsLength[cell.column] = max(maxColLength, len(str(t)))

                        else:
                            colsLength[cell.column] = max(maxColLength, len(str(cell.value)))

                        cell.alignment = openpyxlAlignment(wrap_text=True, horizontal='center', vertical='center')


                    ws.column_dimensions[colLetter].width = colsLength[colIndex] + 1


            wb.save(scheduleExcelPath)


    except Exception as e:
        print('Error while formatting the Excel file:', e)