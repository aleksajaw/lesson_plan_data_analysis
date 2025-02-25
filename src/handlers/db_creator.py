from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import testExcelPath
from src.utils.writers_df_utils import writerForDfToExcelSheet
from pandas import DataFrame
import pandas as pd


def createScheduleDB(schoolWebInfo, schedules):
    
    msgText = ''
    try:
        dfs = DataFrame()
        
        for df in schedules.values():
            df = df.stack(level=[0], future_stack=True)
            df = df.reset_index()
            df['Szkoła'] = schoolWebInfo['schoolName']['short']
            dfs = pd.concat([dfs, df], ignore_index=True)

        writerForDfToExcelSheet(testExcelPath, dfs, schoolWebInfo['title'], showIndex=False, writerMode='a', mergeCells=False)
    
    except Exception as e:
        msgText = handleErrorMsg(f'\nError while creating the database for schedule data.', getTraceback(e))
    
    if msgText: print(msgText)