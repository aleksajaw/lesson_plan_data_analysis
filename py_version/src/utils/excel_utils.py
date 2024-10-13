from constants import scheduleExcelPath, excelEngineName, draftSheetName
from files_utils import doesFileExist
import json
import re
from pandas import ExcelWriter, DataFrame, read_excel


def doesSheetExist(workbook=ExcelWriter.book, sheetName=''):
    return bool(sheetName in workbook.sheetnames and len(workbook.sheetnames)>0)


def createDraftSheet(excelFilePath=scheduleExcelPath):
    writer = ExcelWriter(excelFilePath, engine=excelEngineName)
    draftDf = DataFrame()
    draftDf.to_excel(writer, sheet_name=draftSheetName, index=False)
    writer.close()


def createDraftSheetIfNecessary():
    if not doesFileExist(scheduleExcelPath):
        createDraftSheet()


def delDraftIfNecessary(workbook=ExcelWriter.book):
    if ((len(workbook.sheetnames)>1) & doesSheetExist(workbook, draftSheetName)):
        deleteExcelSheet(workbook, draftSheetName)


def compareAndUpdateFile(filePath='',dataToCompare=''):
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


def writingObjOfDfsToExcel(writer=ExcelWriter, dataToEnter=None, isConverted = True):
    try:
        classDfs = convertToObjOfDfs(dataToEnter) if not isConverted else dataToEnter

        for className in classDfs:
            classDfs[className].to_excel(writer, sheet_name=className, index=False)

        print('Data loaded to the schedule Excel file.')

    except Exception as e:
        print(f'Error loading complete classes data: {e}')


def writingToExcelSheet(writer=ExcelWriter, sheetName='', dataToEnter=None):
    try:
        df = convertToDf(dataToEnter)
        df.to_excel(writer, sheet_name=sheetName, index=False)
        print(f'Data for sheet {sheetName} loaded.')

    except Exception as e:
        print(f'Error loading data to {sheetName}: {e}')


def deleteExcelSheet(workbook=ExcelWriter.book, sheetName=''):
    try:
        del workbook[sheetName]
        msgText = f'The sheet {sheetName} deleted.'

    except Exception as e:
        msgText = f'Error deleting the sheet {sheetName}: {e}'

    print(msgText)


def convertCurrExcelToDfsJSON():
    excelJSON = {}

    try:
        excelDfs = read_excel(scheduleExcelPath, sheet_name=None)
        excelJSON = convertObjOfDfsToJSON(excelDfs)

    except Exception as e:
        print(f'Error converting existing schedule Excel file to JSON: {e}')

    return excelJSON 


# CONVERTERS #
def convertObjOfDfsToJSON(dataToConvert=None):
    objOfDfsJSON = {}

    for sheet_name, df in dataToConvert.items():
        objOfDfsJSON[sheet_name] = df.to_json(orient='split')

    return json.dumps(objOfDfsJSON, indent=4)


def convertToDf(dataToConvert=None):
    df = None

    if(dataToConvert):
        lessonsCols = dataToConvert[0][:2] + [day for day in dataToConvert[0][2:] for _ in range(3)]
        lessonRows = dataToConvert[1:]

        df = DataFrame(data=lessonRows, columns=lessonsCols)

    return df


def convertToObjOfDfs(dataToConvert=None):
    if dataToConvert:
        return {sheet_name: convertToDf(dataToConvert[sheet_name]) for sheet_name in dataToConvert}

    else:
        return DataFrame()


def convertDigitInStrToInt(text=''):
    return int(text) if str.isdigit(text) else text


def convertBrInText(text=''):
    if isinstance(text, str):
        if '<br>' in text:
            text.replace("<br>", "\n")

        elif '<br />' in text:
            text.replace("<br />", "\n")

    return text


def splitHTMLAndRemoveTags(HTMLText=''):
    HTMLText = re.sub(r'&nbsp;|\s+', '', HTMLText)
    parts = re.split(r'(<[^>]+>)', HTMLText)
    textParts = []

    for part in parts:
        if part and not part.startswith('<'):
            textParts.append(convertDigitInStrToInt(part))

    return textParts