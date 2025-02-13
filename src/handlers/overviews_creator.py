from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleClassroomsGroupedDfsJSONPath, scheduleClassroomsDfsJSONPath, scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONPath, scheduleClassroomsOverviewResourcesByDaysExcelPath, scheduleClassroomsGroupedOverviewResourcesByDaysExcelPath, scheduleClassroomsOverviewResourcesByHoursExcelPath, scheduleClassroomsGroupedOverviewResourcesByHoursExcelPath, scheduleClassroomsOverviewResourcesByDaysDfsJSONPath, scheduleClassroomsGroupedOverviewResourcesByDaysDfsJSONPath, scheduleClassroomsOverviewResourcesByHoursDfsJSONPath
from src.constants.schedule_structures_constants import noGroupMarker, wholeClassGroupName, timeIndexNames, dfRowNrAndTimeTuples, weekdaysLen
from src.constants.overview_constants import sumCellsInRowsColName, sumCellsInColsRowName, amountColName, percOfDayColName, percOfWeekColName, notApplicableVal, noLessonsVal, introColName, dataTypeColsLvlName, meanColName, nrOfOccurrColName, overviewsMainByDaysColIndexNames, overviewColIndexLastLvlName
from src.utils.converters_utils import customSorting, divisionResultAsPercentage, createTupleFromVals, convertValToPercentage, convertToRounded
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
    createOverviewMainIntro()



def createOverviewsWithResourcesBy(overviewKey):
    msgText=''
    
    try:
        overviewExcelPaths   = { 'days'  : [ scheduleClassroomsOverviewResourcesByDaysExcelPath, scheduleClassroomsGroupedOverviewResourcesByDaysExcelPath ],
                                 'hours' : [ scheduleClassroomsOverviewResourcesByHoursExcelPath, scheduleClassroomsGroupedOverviewResourcesByHoursExcelPath ] }
        overviewDfsJSONPaths = { 'days'  : [ scheduleClassroomsOverviewResourcesByDaysDfsJSONPath, scheduleClassroomsGroupedOverviewResourcesByDaysDfsJSONPath ],
                                 'hours' : [ scheduleClassroomsOverviewResourcesByHoursDfsJSONPath, scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONPath ] }

        i=-1
        for filePath in [ scheduleClassroomsDfsJSONPath, scheduleClassroomsGroupedDfsJSONPath ]:
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
                    dfBySpecificColsGroup = ( df.xs(key=colName, level=1, axis=1)
                                                .astype(str).replace('', pd.NA) )

                    if overviewKey == 'hours':
                        # Transposed DataFrame to get indexes as columns.
                        dfBySpecificColsGroup = dfBySpecificColsGroup.T

                    # Count the value occurrences there.
                    uniqueValFromColsLvl2Counter = ( dfBySpecificColsGroup.apply(lambda col: col.dropna()
                                                                                                .value_counts()
                                                                                                .astype(int)).fillna(0) )

                    if overviewKey == 'hours':
                        # Group indexes (multiple lessons at same time).
                        uniqueValFromColsLvl2Counter = ( uniqueValFromColsLvl2Counter.groupby(level=dfBySpecificColsGroup.columns.names, axis=1)
                                                                                     .sum() )


                    # Create a new col with the sum of values in the row(s).
                    uniqueValFromColsLvl2Counter[sumCellsInRowsColName] = uniqueValFromColsLvl2Counter.sum(axis=1)


                    # Create a new row with the sum of values in the col.
                    sumCellsInColsRowNameTuple = (sumCellsInColsRowName, len(uniqueValFromColsLvl2Counter.index))
                    rowForSumEntireCols = ( uniqueValFromColsLvl2Counter.sum(axis=0)
                                                                        .to_frame(name=sumCellsInColsRowNameTuple)
                                                                        .T )

                    # Create a new MultiIndex for rows.
                    indexGroupName = colName
                    for singleIndex in uniqueValFromColsLvl2Counter.index:
                        
                        if singleIndex.isdigit():
                            singleIndex = int(singleIndex)
                        
                        elif singleIndex == noGroupMarker:
                            singleIndex = wholeClassGroupName
                        
                        singleElIndexTuple = (indexGroupName, singleIndex)
                        newIndex.append(singleElIndexTuple)
                        #singleElIndexArray = [colName, singleElInCol]
                        #newIndex.append(singleElIndexArray)

                    newIndex = MultiIndex.from_tuples(tuples=newIndex, names=['Typ grupy', 'Element grupy'])
                    #newIndex = MultiIndex.from_arrays(arrays=newIndex, names=['Typ grupy', 'Element grupy'])


                    # Complete the data and concatenate with the existing data.
                    uniqueValFromColsLvl2Counter.index = newIndex
                    newIndexSorted = sorted( uniqueValFromColsLvl2Counter.index, key=lambda x: customSorting(x) )
                    uniqueValFromColsLvl2Counter = uniqueValFromColsLvl2Counter.loc[ newIndexSorted ]
                    uniqueValFromColsLvl2Counter = pd.concat([uniqueValFromColsLvl2Counter, rowForSumEntireCols])
                    
                    tempDf = uniqueValFromColsLvl2Counter
                    newDf = DataFrame(index=tempDf.index).rename_axis(axis=0, mapper=['Typ grupy', 'Element grupy'])
                    
                    mainColNames = [tempDf.columns.names[0]]   if overviewKey == 'days'   else tempDf.columns.names
                    overviewColNames = mainColNames + [overviewColIndexLastLvlName]

                    maxPercentage = notApplicableVal#convertValToPercentage(1)
                    
                    for col in tempDf.columns:
                        quantityColName = createTupleFromVals([col, amountColName])
                        #quantityColName = createListFromVals([col, amountColName])

                        newDf[quantityColName] = tempDf[col]
                        newDf.columns = MultiIndex.from_tuples(tuples=newDf.columns, names=overviewColNames)
                        #newDf.columns = MultiIndex.from_arrays(arrays=newDf.columns, names=overviewColNames)


                        if sumCellsInRowsColName not in col:
                            #colWithoutLastRow = newDf.loc[(newDf.index!=sumCellsInColsRowName), quantityColName]
                            colWithoutLastRow = newDf.loc[newDf.index[:-1], quantityColName]
                            
                            #lastCellInCol = newDf.loc[(newDf.index==sumCellsInColsRowName), quantityColName]
                            lastCellInCol = newDf.loc[newDf.index[-1], quantityColName]

                            percOfDayColNameTuple = createTupleFromVals([col, percOfDayColName])
                            #percOfDayColNameTuple = createListFromVals([col, percOfDayColName])

                            newDf.loc[newDf.index[:-1], percOfDayColNameTuple] = divisionResultAsPercentage(colWithoutLastRow, lastCellInCol)

                            newDf.loc[sumCellsInColsRowNameTuple, percOfDayColNameTuple] = maxPercentage   if lastCellInCol   else noLessonsVal
                            
                            sumValCol = tempDf[sumCellsInRowsColName]
                        
                        else:
                            sumValCol = tempDf.loc[sumCellsInColsRowNameTuple, sumCellsInRowsColName]
                        
                        
                        percOfWeekColNameTuple = createTupleFromVals([col, percOfWeekColName])
                        #percOfWeekColNameTuple = createListFromVals([col, percOfWeekColName])
                        newDf[percOfWeekColNameTuple] = divisionResultAsPercentage(newDf[quantityColName], sumValCol)

                    #newDf.loc[(newDf.index==sumCellsInColsRowName), percOfWeekColNameTuple] = maxPercentage
                    newDf.loc[newDf.index[-1], newDf.columns[-1]] = maxPercentage

                    overviewDfs[sheetName].append(newDf)


            writerForListOfObjsWithMultipleDfsToJSONAndExcel(overviewDfsJSONPaths[overviewKey][i], overviewExcelPaths[overviewKey][i], overviewDfs, False)


    except Exception as e:
        msgText = handleErrorMsg('Error while creating the overviews of schedules.', getTraceback(e))
    
    if msgText: print(msgText)



def createOverviewMain(overviewKey=''):
    msgText=''

    objOfMultiDfs = readMultiDfsJSONAsObjOfDfObjLists(scheduleClassroomsGroupedOverviewResourcesByHoursDfsJSONPath)
    lastDfRows = {}
    
    try:
        for sheetName, dfObjList in objOfMultiDfs.items():
            lastDfRows[sheetName] = {  'week_perc' : {
                                         'days' : [],
                                         'hours': []
                                       }  }
          
            for dfObj in dfObjList:
                
                df = dfObj['df']
                lastDfRow = df.loc[df.index[-1]]

                try:
                    lastDfRowDaySums = lastDfRow.loc[IndexSlice[:, :, amountColName]]
                except:
                    lastDfRowDaySums = lastDfRow.loc[IndexSlice[:, amountColName]]

                #lastDfRows[sheetName]['sums'][oKey].append( lastDfRowDaySums )
                #lastDfRows[sheetName]['day_perc']['max'].append( getMaxInDfByColName(df, percOfDayColName) )
                #lastDfRows[sheetName]['day_perc']['min'].append( getMinInDfByColName(df, percOfDayColName) )      

                for oKey in ['hours']:
                    lastDfRows[sheetName]['week_perc'][oKey].append( getMainWeekPercWithMean(oKey, lastDfRow, [amountColName, percOfWeekColName]) )


                '''for x in list(lastDfRows.values()):

                    for y in x['week_perc'].values():

                        print(sheetName)
                        print(y)'''



    except Exception as e:
        msgText = handleErrorMsg('Error while reading JSON file with Data Frames as object with Data Frames.', getTraceback(e))
    
    if msgText: print(msgText)

    #return objOfDfs



def getMaxInDfByColName(df, colName):
    return ( df.xs(colName, level=-1, axis=1)
               .iloc[:-1, :-1]
               .apply( lambda col: col.replace('%','', regex=True).astype(float)
                                      .nlargest(3, keep='all') )
               .fillna('-') )



def getMinInDfByColName(df, colName):
    return ( df.xs(colName, level=-1, axis=1)
               .iloc[:-1, :-1]
               .apply( lambda col: col.replace('%','', regex=True).astype(float)
                                      .nsmallest(3, keep='all') )
               .fillna('-') )



def getMainWeekPercWithMean(overviewKey, lastDfRow, lastDfRowColNames):
    lastDfRowCopy = lastDfRow.copy()

    if overviewKey=='hours':
        lastDfRowWeekPerc = ( lastDfRowCopy.loc[IndexSlice[:, :, lastDfRowColNames ] ][:-1]
                                       .to_frame()
                                       .T )
        overviewDfStack = [0,1]


    elif overviewKey=='days':
        newIndex = []
        i=0
        for i, el in enumerate(lastDfRow.index[:-(1*len(lastDfRowColNames))]):
            correctedI = i//3+1
            newIndex.append( tuple([correctedI]) + el )

        dayLength = len( lastDfRow.index.get_level_values(0).unique()[:-1] )

        for el in lastDfRow.index[-(1*len(lastDfRowColNames)):]:
            newIndex.append( (tuple([el[0], dayLength]) + el[1:]) )

        lastDfRowCopy.index = MultiIndex.from_tuples(newIndex)
        lastDfRowWeekPerc = ( lastDfRowCopy.loc[IndexSlice[:, :, lastDfRowColNames ] ][:-1]
                                       .to_frame()
                                       .T )
        overviewDfStack = [0,1]


    dfWeekPerc = ( lastDfRowWeekPerc.reset_index(drop=True)
                                    .stack(overviewDfStack, sort=False)
                                    .fillna(notApplicableVal)
                                    .reset_index().drop(columns='level_0') )
    

    if overviewKey=='hours':
        dfWeekPerc.at[ dfWeekPerc.index[-1], timeIndexNames[-1] ] = len(dfWeekPerc) - 1
        dfWeekPerc = dfWeekPerc.set_index(timeIndexNames)
    
    elif overviewKey=='days':
        dfWeekPerc.columns = overviewsMainByDaysColIndexNames + lastDfRowColNames
        dfWeekPerc.at[ dfWeekPerc.index[-1], overviewsMainByDaysColIndexNames[1] ] = len(dfWeekPerc) - 1
        dfWeekPerc = dfWeekPerc.set_index(overviewsMainByDaysColIndexNames)

    dfWeekPercMeanVals = ( dfWeekPerc.loc[dfWeekPerc.index[:-1], lastDfRowColNames]
                                     .replace('%','', regex=True).astype(float)
                                     .mean() )
    
    dfWeekPerc.loc[ (meanColName, ''), lastDfRowColNames[0] ] = convertToRounded( dfWeekPercMeanVals[ lastDfRowColNames[0] ] )
    dfWeekPerc.loc[ (meanColName, ''), lastDfRowColNames[1] ] =  convertValToPercentage(dfWeekPercMeanVals[ lastDfRowColNames[1] ])


    dfWeekPerc.columns = pd.MultiIndex.from_tuples([(nrOfOccurrColName, col)   for col in dfWeekPerc.columns])

    return dfWeekPerc



def createOverviewMainIntro():
    colList = [dataTypeColsLvlName, amountColName, percOfDayColName, percOfWeekColName]
    lessonsAmount = 10
    data = {
            'Typ': [
                'Jednostka jednej godziny w planie*',
                'Wykorzystane godz. lekcyjne w planie',
                'Wszystkie możliwe godziny w planie dnia',
                'Jednostka jednego dnia w planie',
                'Wykorzystane dni w planie',
                'Wszystkie możliwe dni w planie tygodnia'
            ],
            amountColName     : [ 1, lessonsAmount, len(dfRowNrAndTimeTuples), 1, 5, weekdaysLen ],
            percOfDayColName  : [ divisionResultAsPercentage( 1, len(dfRowNrAndTimeTuples) ), divisionResultAsPercentage( lessonsAmount, len(dfRowNrAndTimeTuples) ) ] + [notApplicableVal]*4,
            percOfWeekColName : [ divisionResultAsPercentage( 1, len(dfRowNrAndTimeTuples)*weekdaysLen ), divisionResultAsPercentage( lessonsAmount, len(dfRowNrAndTimeTuples)*weekdaysLen ), notApplicableVal,  divisionResultAsPercentage( 1, weekdaysLen ), divisionResultAsPercentage( 5, weekdaysLen ), notApplicableVal ]
        }
    dfTemp = DataFrame(data)
    dfTemp.columns = pd.MultiIndex.from_tuples([(introColName, col)   for col in colList])
    print(dfTemp)
