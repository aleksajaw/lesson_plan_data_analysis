from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import allScheduleGroupedDfsJSONPaths, allScheduleDfsJSONPaths, allScheduleOverviewResourcesExcelPaths, allScheduleGroupedOverviewResourcesExcelPaths, allScheduleOverviewResourcesDfsJSONPaths, allScheduleGroupedOverviewResourcesDfsJSONPaths
from src.constants.schedule_structures_constants import noGroupMarker, wholeClassGroupName, sumCellsInRowsColName, sumCellsInColsRowName, sumCellsInRowsColName
from src.utils.converters_utils import divisionResultAsPercentage, convertValToPercentage
from src.utils.readers_df_utils import readDfsJSONAsObjOfDfs
from src.utils.writers_df_utils import writerForListOfObjsWithMultipleDfsToJSONAndExcel
import pandas as pd
from pandas import  MultiIndex, DataFrame#, Series
#import numpy as np
import os



def createScheduleOverviews():
    msgText=''
    
    try:
        overviewExcelPaths = allScheduleOverviewResourcesExcelPaths + allScheduleGroupedOverviewResourcesExcelPaths
        overviewDfsJSONPaths = allScheduleOverviewResourcesDfsJSONPaths + allScheduleGroupedOverviewResourcesDfsJSONPaths

        i=-1
        for filePath in ( allScheduleDfsJSONPaths + allScheduleGroupedDfsJSONPaths ):
            i=i+1
            fileContent = readDfsJSONAsObjOfDfs(filePath)
            
            overviewDfs = {}

            for sheetName, df in fileContent.items():
                
                newDf = {}
                dfColLvl2Names = df.columns.get_level_values(1).unique()
                overviewDfs[sheetName] = []

                # Iteration through the 2nd level of the DataFrames columns.
                for colName in dfColLvl2Names:
                    newIndex = []

                    # Create the proper Series object with the chosen column for the 2nd level of the columns.
                    colLvl2Content = df.xs(key=colName, level=1, axis=1).astype(str).replace('', pd.NA)

                    #print(colLvl2Content)
                    # Count the value occurrences there.
                    uniqueValFromColsLvl2Counter = colLvl2Content.apply( lambda col: col.dropna().value_counts().astype(int) ).fillna(0)
                    

                    # Create a new col with the sum of values in the row(s).
                    uniqueValFromColsLvl2Counter[sumCellsInRowsColName] = uniqueValFromColsLvl2Counter.sum(axis=1)


                    # Convert .values   =>   np.array()
                    #                .flatten()   =>   flat array
                    uniqueValsArrFromColsLvl2 = pd.unique( colLvl2Content.values.flatten() )
                    uniqueValsArrFromColsLvl2 = [ val   for val in uniqueValsArrFromColsLvl2   if pd.notna(val)]


                    # Create a new row with the sum of values in the col.
                    sumCellsInColsRowName2Lvl = (sumCellsInColsRowName, len(uniqueValsArrFromColsLvl2))
                    rowForSumEntireCols = uniqueValFromColsLvl2Counter.sum(axis=0).to_frame(name=sumCellsInColsRowName2Lvl).T


                    # Create a new MultiIndex for rows.
                    for singleElInCol in uniqueValsArrFromColsLvl2:
                        
                        if singleElInCol.isdigit():
                            singleElInCol = int(singleElInCol)
                        
                        elif singleElInCol == noGroupMarker:
                            singleElInCol = wholeClassGroupName
                        
                        singleElIndexTuple = (colName, singleElInCol)
                        newIndex.append(singleElIndexTuple)

                    newIndex = MultiIndex.from_tuples(newIndex)


                    # Complete the data and concatenate with the existing data.
                    uniqueValFromColsLvl2Counter.index = newIndex
                    uniqueValFromColsLvl2Counter = uniqueValFromColsLvl2Counter.sort_index()
                    uniqueValFromColsLvl2Counter = pd.concat([uniqueValFromColsLvl2Counter, rowForSumEntireCols])
                    
                    tempDf = uniqueValFromColsLvl2Counter
                    newDf = DataFrame(index=tempDf.index)
                    
                    overviewColNames = [tempDf.columns.names[0], 'Typ danych']
                    maxPercentage = convertValToPercentage(1)
                    
                    for col in tempDf.columns:
                        quantityColName = (col, 'Ilość')

                        newDf[quantityColName] = tempDf[col]
                        newDf.columns = MultiIndex.from_tuples(tuples=newDf.columns, names=overviewColNames)


                        if col != sumCellsInRowsColName:
                            #colWithoutLastRow = newDf.loc[(newDf.index!=sumCellsInColsRowName), quantityColName]
                            colWithoutLastRow = newDf.loc[newDf.index[:-1], quantityColName]
                            
                            #lastCellInCol = newDf.loc[(newDf.index==sumCellsInColsRowName), quantityColName]
                            lastCellInCol = newDf.loc[newDf.index[-1], quantityColName]

                            partOfDayColName = (col, 'Udział w całości dnia')

                            newDf.loc[newDf.index[:-1], partOfDayColName] = divisionResultAsPercentage(colWithoutLastRow, lastCellInCol)
                            newDf.loc[sumCellsInColsRowName2Lvl, partOfDayColName] = maxPercentage   if lastCellInCol   else 'brak zajęć'
                            
                            sumValCol = tempDf[sumCellsInRowsColName]
                        
                        else:
                            sumValCol = tempDf.loc[sumCellsInColsRowName2Lvl, sumCellsInRowsColName]
                        
                        
                        partOfWeekColName = (col, 'Udział w całości tygodnia')
                        newDf[partOfWeekColName] = divisionResultAsPercentage(newDf[quantityColName], sumValCol)                    

                    #newDf.loc[(newDf.index==sumCellsInColsRowName), partOfWeekColName] = maxPercentage
                    newDf.loc[newDf.index[-1], newDf.columns[-1]] = maxPercentage


                    #newDf.columns = MultiIndex.from_tuples(newDf.columns)


                    overviewDfs[sheetName].append(newDf)


            writerForListOfObjsWithMultipleDfsToJSONAndExcel(overviewDfsJSONPaths[i], overviewExcelPaths[i], overviewDfs)

    except Exception as e:
        msgText = handleErrorMsg('Error while creating the overviews of schedules.', getTraceback(e))
    
    if msgText: print(msgText)