from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import allScheduleGroupedDfsJSONPaths, allScheduleDfsJSONPaths, allScheduleOverviewResourcesExcelPaths, allScheduleGroupedOverviewResourcesExcelPaths, allScheduleOverviewResourcesDfsJSONPaths, allScheduleGroupedOverviewResourcesDfsJSONPaths, allScheduleOverviewResourcesByDaysExcelPaths, allScheduleGroupedOverviewResourcesByDaysExcelPaths, allScheduleOverviewResourcesByDaysDfsJSONPaths, allScheduleGroupedOverviewResourcesByDaysDfsJSONPaths,allScheduleOverviewResourcesByHoursExcelPaths, allScheduleGroupedOverviewResourcesByHoursExcelPaths, allScheduleOverviewResourcesByHoursDfsJSONPaths, allScheduleGroupedOverviewResourcesByHoursDfsJSONPaths
from src.constants.schedule_structures_constants import noGroupMarker, wholeClassGroupName, sumCellsInRowsColName, sumCellsInColsRowName, sumCellsInRowsColName
from src.utils.converters_utils import customSorting, divisionResultAsPercentage, createTupleFromVals#, convertValToPercentage
from src.utils.readers_df_utils import readDfsJSONAsObjOfDfs
from src.utils.writers_df_utils import writerForListOfObjsWithMultipleDfsToJSONAndExcel
import pandas as pd
from pandas import  MultiIndex, DataFrame#, Series
#import numpy as np
import os



def createScheduleOverviews():
    createOverviewsWithResourcesBy('days')
    createOverviewsWithResourcesBy('hours')



def createOverviewsWithResourcesBy(overviewKey):
    msgText=''
    
    try:
        overviewExcelPaths   = { 'days'  : allScheduleOverviewResourcesByDaysExcelPaths + allScheduleGroupedOverviewResourcesByDaysExcelPaths,
                                 'hours' : allScheduleOverviewResourcesByHoursExcelPaths + allScheduleGroupedOverviewResourcesByHoursExcelPaths }
        overviewDfsJSONPaths = { 'days'  : allScheduleOverviewResourcesByDaysDfsJSONPaths + allScheduleGroupedOverviewResourcesByDaysDfsJSONPaths,
                                 'hours' : allScheduleOverviewResourcesByHoursDfsJSONPaths + allScheduleGroupedOverviewResourcesByHoursDfsJSONPaths }

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
                    # level=1   is equal   df.columns.names[1]
                    dfBySpecificColsGroup = df.xs(key=colName, level=1, axis=1).astype(str).replace('', pd.NA)

                    if overviewKey == 'hours':
                        # Transposed DataFrame to get indexes as columns.
                        dfBySpecificColsGroup = dfBySpecificColsGroup.T

                    # Count the value occurrences there.
                    uniqueValFromColsLvl2Counter = dfBySpecificColsGroup.apply( lambda col: col.dropna().value_counts().astype(int) ).fillna(0)

                    if overviewKey == 'hours':
                        # Group indexes (multiple lessons at same time).
                        uniqueValFromColsLvl2Counter = uniqueValFromColsLvl2Counter.groupby(level=dfBySpecificColsGroup.columns.names, axis=1).sum()


                    # Create a new col with the sum of values in the row(s).
                    uniqueValFromColsLvl2Counter[sumCellsInRowsColName] = uniqueValFromColsLvl2Counter.sum(axis=1)


                    # Create a new row with the sum of values in the col.
                    sumCellsInColsRowNameTuple = (sumCellsInColsRowName, len(uniqueValFromColsLvl2Counter.index))
                    rowForSumEntireCols = uniqueValFromColsLvl2Counter.sum(axis=0).to_frame(name=sumCellsInColsRowNameTuple).T


                    # Create a new MultiIndex for rows.
                    for singleElInCol in uniqueValFromColsLvl2Counter.index:
                        
                        if singleElInCol.isdigit():
                            singleElInCol = int(singleElInCol)
                        
                        elif singleElInCol == noGroupMarker:
                            singleElInCol = wholeClassGroupName
                        
                        singleElIndexTuple = (colName, singleElInCol)
                        newIndex.append(singleElIndexTuple)

                    newIndex = MultiIndex.from_tuples(tuples=newIndex, names=['Typ grupy', 'Element grupy'])


                    # Complete the data and concatenate with the existing data.
                    uniqueValFromColsLvl2Counter.index = newIndex
                    newIndexSorted = sorted(uniqueValFromColsLvl2Counter.index, key=lambda x: customSorting(x))
                    uniqueValFromColsLvl2Counter = uniqueValFromColsLvl2Counter.loc[ newIndexSorted ]
                    uniqueValFromColsLvl2Counter = pd.concat([uniqueValFromColsLvl2Counter, rowForSumEntireCols])
                    
                    tempDf = uniqueValFromColsLvl2Counter
                    newDf = DataFrame(index=tempDf.index).rename_axis(axis=0, mapper=['Typ grupy', 'Element grupy'])
                    
                    mainColNames = [tempDf.columns.names[0]]   if overviewKey == 'days'   else tempDf.columns.names
                    overviewColNames = mainColNames + ['Typ danych']

                    maxPercentage = 'nie dotyczy'#convertValToPercentage(1)
                    
                    for col in tempDf.columns:
                        quantityColName = createTupleFromVals(col, 'Ilość')

                        newDf[quantityColName] = tempDf[col]
                        newDf.columns = MultiIndex.from_tuples(tuples=newDf.columns, names=overviewColNames)


                        if sumCellsInRowsColName not in col:
                            #colWithoutLastRow = newDf.loc[(newDf.index!=sumCellsInColsRowName), quantityColName]
                            colWithoutLastRow = newDf.loc[newDf.index[:-1], quantityColName]
                            
                            #lastCellInCol = newDf.loc[(newDf.index==sumCellsInColsRowName), quantityColName]
                            lastCellInCol = newDf.loc[newDf.index[-1], quantityColName]

                            partOfDayColName = createTupleFromVals(col, 'Udział w dniu')

                            newDf.loc[newDf.index[:-1], partOfDayColName] = divisionResultAsPercentage(colWithoutLastRow, lastCellInCol)
                            newDf.loc[sumCellsInColsRowNameTuple, partOfDayColName] = maxPercentage   if lastCellInCol   else 'brak zajęć'
                            
                            sumValCol = tempDf[sumCellsInRowsColName]
                        
                        else:
                            sumValCol = tempDf.loc[sumCellsInColsRowNameTuple, sumCellsInRowsColName]
                        
                        
                        partOfWeekColName = createTupleFromVals(col, 'Udział w tygodniu')
                        newDf[partOfWeekColName] = divisionResultAsPercentage(newDf[quantityColName], sumValCol)                    

                    #newDf.loc[(newDf.index==sumCellsInColsRowName), partOfWeekColName] = maxPercentage
                    newDf.loc[newDf.index[-1], newDf.columns[-1]] = maxPercentage


                    #newDf.columns = MultiIndex.from_tuples(newDf.columns)


                    overviewDfs[sheetName].append(newDf)


            writerForListOfObjsWithMultipleDfsToJSONAndExcel(overviewDfsJSONPaths[overviewKey][i], overviewExcelPaths[overviewKey][i], overviewDfs, False)

    except Exception as e:
        msgText = handleErrorMsg('Error while creating the overviews of schedules.', getTraceback(e))
    
    if msgText: print(msgText)