from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import allScheduleGroupedDfsJSONPaths, allScheduleDfsJSONPaths, allScheduleOverviewResourcesExcelPaths, allScheduleGroupedOverviewResourcesExcelPaths, allScheduleOverviewResourcesDfsJSONPaths, allScheduleGroupedOverviewResourcesDfsJSONPaths, allScheduleOverviewResourcesByDaysExcelPaths, allScheduleGroupedOverviewResourcesByDaysExcelPaths, allScheduleOverviewResourcesByDaysDfsJSONPaths, allScheduleGroupedOverviewResourcesByDaysDfsJSONPaths,allScheduleOverviewResourcesByHoursExcelPaths, allScheduleGroupedOverviewResourcesByHoursExcelPaths, allScheduleOverviewResourcesByHoursDfsJSONPaths, allScheduleGroupedOverviewResourcesByHoursDfsJSONPaths
from src.constants.schedule_structures_constants import noGroupMarker, wholeClassGroupName
from src.constants.overview_constants import sumCellsInRowsColName, sumCellsInColsRowName, amountColName, percOfDayColName, percOfWeekColName, notApplicableVal, noLessonsVal
from src.utils.converters_utils import customSorting, divisionResultAsPercentage, createTupleFromVals, createListFromVals#, convertValToPercentage
from src.utils.readers_df_utils import readDfsJSONAsObjOfDfs, readMultiDfsJSONAsObjOfDfObjLists
from src.utils.writers_df_utils import writerForListOfObjsWithMultipleDfsToJSONAndExcel
import pandas as pd
from pandas import  MultiIndex, DataFrame, IndexSlice#, Series
import numpy as np
import os



def createScheduleOverviews():
    createOverviewsWithResourcesBy('days')
    createOverviewsWithResourcesBy('hours')
    createOverviewMain()



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
                        #singleElIndexArray = [colName, singleElInCol]
                        #newIndex.append(singleElIndexArray)

                    newIndex = MultiIndex.from_tuples(tuples=newIndex, names=['Typ grupy', 'Element grupy'])
                    #newIndex = MultiIndex.from_arrays(arrays=newIndex, names=['Typ grupy', 'Element grupy'])


                    # Complete the data and concatenate with the existing data.
                    uniqueValFromColsLvl2Counter.index = newIndex
                    newIndexSorted = sorted(uniqueValFromColsLvl2Counter.index, key=lambda x: customSorting(x))
                    uniqueValFromColsLvl2Counter = uniqueValFromColsLvl2Counter.loc[ newIndexSorted ]
                    uniqueValFromColsLvl2Counter = pd.concat([uniqueValFromColsLvl2Counter, rowForSumEntireCols])
                    
                    tempDf = uniqueValFromColsLvl2Counter
                    newDf = DataFrame(index=tempDf.index).rename_axis(axis=0, mapper=['Typ grupy', 'Element grupy'])
                    
                    mainColNames = [tempDf.columns.names[0]]   if overviewKey == 'days'   else tempDf.columns.names
                    overviewColNames = mainColNames + ['Typ danych']

                    maxPercentage = notApplicableVal#convertValToPercentage(1)
                    
                    for col in tempDf.columns:
                        quantityColName = createTupleFromVals(col, amountColName)
                        #quantityColName = createListFromVals(col, amountColName)

                        newDf[quantityColName] = tempDf[col]
                        newDf.columns = MultiIndex.from_tuples(tuples=newDf.columns, names=overviewColNames)
                        #newDf.columns = MultiIndex.from_arrays(arrays=newDf.columns, names=overviewColNames)


                        if sumCellsInRowsColName not in col:
                            #colWithoutLastRow = newDf.loc[(newDf.index!=sumCellsInColsRowName), quantityColName]
                            colWithoutLastRow = newDf.loc[newDf.index[:-1], quantityColName]
                            
                            #lastCellInCol = newDf.loc[(newDf.index==sumCellsInColsRowName), quantityColName]
                            lastCellInCol = newDf.loc[newDf.index[-1], quantityColName]

                            percOfDayColName = createTupleFromVals(col, percOfDayColName)
                            #percOfDayColName = createListFromVals(col, percOfDayColName)

                            newDf.loc[newDf.index[:-1], percOfDayColName] = divisionResultAsPercentage(colWithoutLastRow, lastCellInCol)
                            newDf.loc[sumCellsInColsRowNameTuple, percOfDayColName] = maxPercentage   if lastCellInCol   else noLessonsVal
                            
                            sumValCol = tempDf[sumCellsInRowsColName]
                        
                        else:
                            sumValCol = tempDf.loc[sumCellsInColsRowNameTuple, sumCellsInRowsColName]
                        
                        
                        percOfWeekColName = createTupleFromVals(col, percOfWeekColName)
                        #percOfWeekColName = createListFromVals(col, percOfWeekColName)
                        newDf[percOfWeekColName] = divisionResultAsPercentage(newDf[quantityColName], sumValCol)                    

                    #newDf.loc[(newDf.index==sumCellsInColsRowName), percOfWeekColName] = maxPercentage
                    newDf.loc[newDf.index[-1], newDf.columns[-1]] = maxPercentage


                    #newDf.columns = MultiIndex.from_tuples(newDf.columns)


                    overviewDfs[sheetName].append(newDf)


            writerForListOfObjsWithMultipleDfsToJSONAndExcel(overviewDfsJSONPaths[overviewKey][i], overviewExcelPaths[overviewKey][i], overviewDfs, False)


    except Exception as e:
        msgText = handleErrorMsg('Error while creating the overviews of schedules.', getTraceback(e))
    
    if msgText: print(msgText)



def createOverviewMain():
    msgText=''

    objOfMultiDfs = readMultiDfsJSONAsObjOfDfObjLists(allScheduleGroupedOverviewResourcesByHoursDfsJSONPaths[0])
    lastDfRows = {}
    
    try:
        for sheetName, dfObjList in objOfMultiDfs.items():
          lastDfRows[sheetName] = {
                                     'day_sums'  : [],
                                     'day_perc'  : {
                                         'max' : [],
                                         'min' : []
                                     },
                                     'week_perc' : {
                                         'max' : [],
                                         'min' : []
                                     }
                                  }
          
          for dfObj in dfObjList:
              df = dfObj['df']

              lastDfRowDaySums  = df.loc[df.index[-1], IndexSlice[:, :, amountColName]]

              lastDfRowsDayPercMax = df.xs(percOfDayColName, level=2, axis=1).iloc[:-1, :-1].apply(
                                                                                                     lambda col: ( col.replace(f'%','', regex=True) ).astype( float ).nlargest( 3, keep='all' )
                                                                                                  ).fillna('-')
              lastDfRowsDayPercMin = df.xs(percOfDayColName, level=2, axis=1).iloc[:-1, :-1].apply(
                                                                                                     lambda col: ( col.replace(f'%','', regex=True) ).astype( float ).nsmallest( 3, keep='all' )
                                                                                                  ).fillna('-')


              lastDfRowsWeekPercMax = df.xs(percOfWeekColName, level=2, axis=1).iloc[:-1, :-1].apply(
                                                                                                       lambda row: ( row.replace(f'%','', regex=True) ).astype( float ).replace([0.0], np.nan).nlargest( 3, keep='all' ),
                                                                                                       axis=1
                                                                                                    ).fillna('-')
              lastDfRowsWeekPercMin = df.xs(percOfWeekColName, level=2, axis=1).iloc[:-1, :-1].apply(
                                                                                                       lambda row: ( row.replace(f'%','', regex=True)).astype( float ).nsmallest( 3, keep='all' ),
                                                                                                       axis=1
                                                                                                    ).fillna('-')
              
              lastDfRows[sheetName]['day_sums'].append( lastDfRowDaySums )

              lastDfRows[sheetName]['day_perc']['max'].append( lastDfRowsDayPercMax )
              lastDfRows[sheetName]['day_perc']['min'].append( lastDfRowsDayPercMin )

              lastDfRows[sheetName]['week_perc']['max'].append( lastDfRowsWeekPercMax )
              lastDfRows[sheetName]['week_perc']['min'].append( lastDfRowsWeekPercMin )
              
              print('\n\n\n\n\n\n', sheetName)
              print(list(lastDfRows.values())[0]['week_perc']['max'])


    except Exception as e:
        msgText = handleErrorMsg('Error while reading JSON file with Data Frames as object with Data Frames.', getTraceback(e))
    
    if msgText: print(msgText)

    #return objOfDfs