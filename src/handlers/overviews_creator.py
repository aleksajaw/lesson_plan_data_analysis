from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import schedulePath, allScheduleGroupedDfsJSONPath, allScheduleDfsJSONPath, scheduleFileBaseNames, scheduleFileGroupedBaseNames
from src.constants.schedule_structures_constants import noGroupMarker, wholeClassGroupName
from src.utils.excel_utils import convertDfsJSONToObjOfDfs, writerForExcelWorksheetsWithMultipleDfs
import pandas as pd
from pandas import  MultiIndex
import numpy as np
import os



def createScheduleOverviews():
    msgText=''
    
    try:
        scheduleOverviewBaseNames = scheduleFileBaseNames + scheduleFileGroupedBaseNames[1:]
        i=-1
        for scheduleFilePath in ( allScheduleDfsJSONPath + allScheduleGroupedDfsJSONPath ):
            i=i+1
            a = convertDfsJSONToObjOfDfs(scheduleFilePath)
            
            aNew = {}
            aT = {}

            for sheetName, df in a.items():
                
                newDf = {}
                dfColLvl2Names = df.columns.get_level_values(1).unique()
                

                # Iteration through the 2nd level of the Data Frames columns.
                for colName in dfColLvl2Names:
                    newIndex = []

                    # Create the proper Series object with the chosen column for the 2nd level of the columns.
                    lvl2ColContent = df.xs(colName, level=1, axis=1).astype(str).replace('', pd.NA)
                    
                    # Count the value occurrences there.
                    try:
                        lvl2ColUniqueValCounter = lvl2ColContent.apply( lambda col: col.dropna().value_counts() ).fillna(0)
                    except:
                        lvl2ColUniqueValCounter = lvl2ColContent.apply( lambda col: col.dropna().value_counts() ).fillna(0)

                    lvl2ColUniqueValCounter['Razem'] = lvl2ColUniqueValCounter.sum(axis=1)

                    # Convert .values   =>   np.array()
                    #                .flatten()   =>   flat array
                    lvl2ColUniqueValArr = pd.unique( lvl2ColContent.values.flatten() )


                    # Create a new MultiIndex.
                    for singleElInCol in lvl2ColUniqueValArr:
                        # Ignore the empty values.
                        if pd.notna(singleElInCol):
                            if singleElInCol == noGroupMarker:
                                singleElInCol = wholeClassGroupName

                            singleElIndexTuple = (colName, singleElInCol)
                            newIndex.append(singleElIndexTuple)

                    newIndex = MultiIndex.from_tuples(newIndex)


                    # Complete the data and concatenate with the existing data.
                    lvl2ColUniqueValCounter.index = newIndex
                    newDf = lvl2ColUniqueValCounter

                    try:
                        aNew[sheetName].append(newDf)
                        aT[sheetName].append(newDf.T)
                    except:
                        aNew[sheetName] = [newDf]
                        aT[sheetName] = [newDf.T]

            scheduleOverviewFileName = f'{scheduleOverviewBaseNames[i]}_overview.xlsx'
            writerForExcelWorksheetsWithMultipleDfs( os.path.join(schedulePath, scheduleOverviewFileName), aNew, False, 'rows')


    except Exception as e:
        msgText = handleErrorMsg('Error', getTraceback(e))
    
    if msgText: print(msgText)