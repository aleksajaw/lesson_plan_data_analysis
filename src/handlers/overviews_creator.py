from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import schedulePath, scheduleClassesGroupedDfsJSONPath, scheduleClassroomsGroupedDfsJSONPath, scheduleTeachersGroupedDfsJSONPath, scheduleSubjectsGroupedDfsJSONPath
from src.utils.excel_utils import convertDfsJSONToObjOfDfs, writerForWriteObjOfDfsToExcel
import pandas as pd
from pandas import  MultiIndex
import numpy as np
import os



def createScheduleOverviews():
    msgText=''
    try:
        a = convertDfsJSONToObjOfDfs(scheduleClassroomsGroupedDfsJSONPath)

        for sheetName, df in a.items():
            
            newDf = {}
            dfColLvl2Names = df.columns.get_level_values(1).unique()
            

            # Iteration through the 2nd level of the Data Frames columns.
            for colName in dfColLvl2Names:
                newIndex = []

                # Create the proper Series object with the chosen column for the 2nd level of the columns.
                lvl2ColContent = df.xs(colName, level=1, axis=1).replace('', pd.NA)
                # Count the value occurrences there.
                lvl2ColUniqueValCounter = lvl2ColContent.apply(lambda col: col.value_counts())
                # Convert .values   =>   np.array()
                #                .flatten()   =>   flat array
                lvl2ColUniqueValArr = pd.unique( lvl2ColContent.values.flatten() )


                # Create a new MultiIndex.
                for singleElInCol in lvl2ColUniqueValArr:
                    # Ignore the empty values.
                    if pd.notna(singleElInCol):
                        singleElIndexTuple = (colName, singleElInCol)
                        newIndex.append( singleElIndexTuple)

                newIndex = MultiIndex.from_tuples(newIndex)


                # Complete the data and concatenate with the existing data.
                lvl2ColUniqueValCounter.index = newIndex
                try:
                    newDf = pd.concat([newDf, lvl2ColUniqueValCounter])
                except:
                    newDf = lvl2ColUniqueValCounter


            a[sheetName] = newDf

        writerForWriteObjOfDfsToExcel(os.path.join(schedulePath,'text.xlsx'), a, False)


    except Exception as e:
        msgText = handleErrorMsg('Error', getTraceback(e))
    
    if msgText: print(msgText)