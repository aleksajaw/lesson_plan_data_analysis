from src.utils.error_utils import handleErrorMsg, getTraceback
from src.constants.paths_constants import scheduleClassroomsGroupedDfsJSONPath, scheduleClassroomsDfsJSONPath, scheduleClassroomsGroupedResourceAllocByHoursDfsJSONPath, scheduleClassroomsResourceAllocByDaysExcelPath, scheduleClassroomsGroupedResourceAllocByDaysExcelPath, scheduleClassroomsResourceAllocByHoursExcelPath, scheduleClassroomsGroupedResourceAllocByHoursExcelPath, scheduleClassroomsResourceAllocByDaysDfsJSONPath, scheduleClassroomsGroupedResourceAllocByDaysDfsJSONPath, scheduleClassroomsResourceAllocByHoursDfsJSONPath, scheduleClassroomsWideAndVertOverviewByNumbersDfsJSONPath, scheduleClassroomsWideAndVertOverviewByNumbersExcelPath
from src.constants.schedule_structures_constants import noGroupMarker, wholeClassGroupName, timeIndexNames, dfRowNrAndTimeTuples, weekdaysLen, classGroupsOwnerName
from src.constants.overview_constants import sumColName, sumRowName, meanRowName, amountColName, percOfDayColName, percOfWeekColName, notApplicableVal, noLessonsVal, introColName, dataTypeColsLvlName, meanColName, nrOfOccurrColName, overviewsMainByDaysColIndexNames, overviewColIndexLastLvlName, nrOfClassesPerHourName, classroomOccupancyTableName, classroomGapsTableName, classroomAvailabilityTableName, basicTableTitleLvlName
from src.utils.df_utils import createNewMultiIndexWithNewFirstLvl, addNewSumColToDf, addNewMeanColToDf, setNewDfColsTitle, writeDfColSumToCell, writeDfColMeanToCell, convertDfValsToCounters, retainOnlyFirstCellsInDfGroups, convertDfValsToBinaryStates, getDfValidIndices, addNewCalcRowsToDf, createNewMultiIndexForSumRow, setGroupCounterInDfSumRowIndex
from src.utils.writers_df_utils import writerForListOfObjsWithMultipleDfsToJSONAndExcel
from src.utils.converters_utils import customSorting, divisionResultAsPercentage, createTupleFromVals, convertValToPercentage, convertToRounded, convertDigitInStrToInt
from src.utils.readers_df_utils import readDfsJSONAsObjOfDfs, readMultiDfsJSONAsObjOfDfObjLists
from src.utils.writers_df_utils import writerForListOfObjsWithMultipleDfsToJSONAndExcel
import pandas as pd
from pandas import  MultiIndex, DataFrame, IndexSlice
import numpy as np
import os



def createScheduleOverviews(globalSchedules, schoolWebInfo):
    createOverviewsWithResourcesAllocBy(globalSchedules, 'days', schoolWebInfo)
    createOverviewsWithResourcesAllocBy(globalSchedules, 'hours', schoolWebInfo)
    #createOverviewMain()
    #createOverviewMainIntro()



def createOverviewsWithLessonsByNrs(objOfDfs):
    msgText=''

    try:
        newObjOfDfsByNumbers = {}

        # Get the 1st DataFrame in the list
        # dfKey is here a name of for example class, classroom, teacher
        for dfName, newDfBasic in objOfDfs.items():
            
            newObjOfDfsByNumbers[dfName] = []
            
            # Prepare the DataFrame to retain only the count values. (Remove the redundant cells.)
            newDfByNumbers = retainOnlyFirstCellsInDfGroups(newDfBasic.copy())

            # Convert the col names from str to int and add a title for the table (DataFrame). 
            newMultiIndexCols = createNewMultiIndexWithNewFirstLvl(newDfByNumbers, classroomOccupancyTableName, basicTableTitleLvlName)
            newDfByNumbers.columns = newMultiIndexCols

            newDfByNumbers = convertDfValsToCounters(newDfByNumbers, lvlList=[0,1,2], retainOnlyLastRows=True)
            newDfByNumbers = addNewCalcRowsToDf(newDfByNumbers, sumRowName, isRowIndexFirstLvlADay=True)
            newDfByNumbers = addNewCalcRowsToDf(newDfByNumbers, meanRowName, nrOfClassesPerHourName, isRowIndexFirstLvlADay=True)
            

            newDfByNumbersGaps = newDfByNumbers.copy()
            newDfByNumbersAvailability = convertDfValsToBinaryStates(newDfByNumbers.copy())


            for col in newDfByNumbers.columns:
                
                for dayName in newDfByNumbers.index.get_level_values(0).unique():

                    colData = newDfByNumbersGaps.xs(dayName, level=0)[col]
                    (firstValidIdx, lastValidIdx) = getDfValidIndices(colData)

                    dayName = createTupleFromVals(dayName)

                    sumKey = createNewMultiIndexForSumRow(newDfByNumbers.index.names, dayName, sumRowName, '')
                    meanKey = createNewMultiIndexForSumRow(newDfByNumbers.index.names, dayName, meanRowName, nrOfClassesPerHourName)


                    newDfByNumbersAvailability = writeDfColSumToCell(newDfByNumbersAvailability, sumKey, col, firstLvlRowMultiIndex=dayName)
                    newDfByNumbersAvailability = writeDfColMeanToCell(newDfByNumbersAvailability, meanKey, col, firstLvlRowMultiIndex=dayName)


                    if firstValidIdx is not None   and   lastValidIdx is not None:
                        
                        (firstIndex, lastIndex) = (dayName + firstValidIdx, dayName + lastValidIdx)

                        newDfByNumbersGaps.loc[firstIndex:lastIndex, col] = convertDfValsToBinaryStates(newDfByNumbersGaps.loc[firstIndex:lastIndex, col])
                    
                        newDfByNumbers = writeDfColSumToCell(newDfByNumbers, sumKey, col, firstValidIndex=firstIndex, lastValidIndex=lastIndex)
                        newDfByNumbers = writeDfColMeanToCell(newDfByNumbers, meanKey, col, firstLvlRowMultiIndex=dayName)

                        newDfByNumbersGaps = writeDfColSumToCell(newDfByNumbersGaps, sumKey, col, firstValidIndex=firstIndex, lastValidIndex=lastIndex)
                        newDfByNumbersGaps = writeDfColMeanToCell(newDfByNumbersGaps, meanKey, col, firstLvlRowMultiIndex=dayName)


                    else:
                        newDfByNumbers = writeDfColSumToCell(newDfByNumbers, sumKey, col, newVal=0.0)
                        newDfByNumbers = writeDfColMeanToCell(newDfByNumbers, meanKey, col, newVal=0.0)

                        newDfByNumbersGaps = writeDfColSumToCell(newDfByNumbersGaps, sumKey, col, newVal=0.0)
                        newDfByNumbersGaps = writeDfColMeanToCell(newDfByNumbersGaps, meanKey, col, newVal=0.0)


            newDfByNumbers = setGroupCounterInDfSumRowIndex(newDfByNumbers)
            newDfByNumbersGaps = setGroupCounterInDfSumRowIndex(newDfByNumbersGaps)
            newDfByNumbersAvailability = setGroupCounterInDfSumRowIndex(newDfByNumbersAvailability)


            newDfByNumbers = addNewSumColToDf(newDfByNumbers)
            newDfByNumbers = addNewMeanColToDf(newDfByNumbers)

            newDfByNumbersAvailability = setNewDfColsTitle(newDfByNumbersAvailability, classroomAvailabilityTableName)
            newDfByNumbersAvailability = addNewSumColToDf(newDfByNumbersAvailability)
            newDfByNumbersAvailability = addNewMeanColToDf(newDfByNumbersAvailability)

            newDfByNumbersGaps = setNewDfColsTitle(newDfByNumbersGaps, classroomGapsTableName)
            newDfByNumbersGaps = addNewSumColToDf(newDfByNumbersGaps)
            newDfByNumbersGaps = addNewMeanColToDf(newDfByNumbersGaps)


            # Number of classes assigned to rooms at specific hours during the day
            #print(newDfByNumbers)
            
            # Number of hours per room on a daily basis
            #print(newDfByNumbers.groupby(axis=0, level=0).sum())
            
            # Number of rooms occupied per hour throughout the day
            #print(newDfByNumbers.sum(axis=1))
            
            # Number of rooms occupied for specific hours across the week
            #print(newDfByNumbers.groupby(axis=0, level=[1,2]).sum())
            
            # Number of hours per room across the week
            #print(newDfByNumbers.sum(axis=0))


            newObjOfDfsByNumbers[dfName].extend([newDfByNumbers, newDfByNumbersAvailability, newDfByNumbersGaps])

        dfsByNumbersInLineLimit = len( newObjOfDfsByNumbers[ next(iter(newObjOfDfsByNumbers)) ] )


        writerForListOfObjsWithMultipleDfsToJSONAndExcel(scheduleClassroomsWideAndVertOverviewByNumbersDfsJSONPath, scheduleClassroomsWideAndVertOverviewByNumbersExcelPath, newObjOfDfsByNumbers, dfsInRowLimit=dfsByNumbersInLineLimit)

    except Exception as e:
        msgText = handleErrorMsg('\nError while creating the Excel file with all the schedules written in wide and vertical format.', getTraceback(e))

    if msgText: print(msgText)



def createOverviewsWithResourcesAllocBy(globalSchedules, overviewKey, schoolWebInfo):
    msgText=''
    
    try:
        overviewExcelPaths   = { 'days'  : [ scheduleClassroomsResourceAllocByDaysExcelPath, scheduleClassroomsGroupedResourceAllocByDaysExcelPath ],
                                 'hours' : [ scheduleClassroomsResourceAllocByHoursExcelPath, scheduleClassroomsGroupedResourceAllocByHoursExcelPath ] }
        overviewDfsJSONPaths = { 'days'  : [ scheduleClassroomsResourceAllocByDaysDfsJSONPath, scheduleClassroomsGroupedResourceAllocByDaysDfsJSONPath ],
                                 'hours' : [ scheduleClassroomsResourceAllocByHoursDfsJSONPath, scheduleClassroomsGroupedResourceAllocByHoursDfsJSONPath ] }

        i=-1
        filteredGlobalSchedules = { key: value   for key, value in globalSchedules.items()   if 'classroom' in key}

        for scheduleType, objOfDfs in filteredGlobalSchedules.items():
        #for filePath in [ ]:
            i=i+1
            #fileContent = readDfsJSONAsObjOfDfs(filePath)

            # It is needed to transform the fn to doesn't repeat read the file.
            overviewDfs = {}

            for sheetName, df in objOfDfs.items():
                
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
                    uniqueValFromColsLvl2Counter[sumColName] = uniqueValFromColsLvl2Counter.sum(axis=1)


                    # Create a new row with the sum of values in the col.
                    sumRowNameTuple = (sumRowName, len(uniqueValFromColsLvl2Counter.index))
                    rowForSumEntireCols = ( uniqueValFromColsLvl2Counter.sum(axis=0)
                                                                        .to_frame(name=sumRowNameTuple)
                                                                        .T )

                    # Create a new MultiIndex for rows.
                    indexGroupName = colName
                    for singleIndex in uniqueValFromColsLvl2Counter.index:
                        
                        singleIndex = convertDigitInStrToInt(singleIndex)
                        
                        if singleIndex == noGroupMarker   and   indexGroupName == classGroupsOwnerName:
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


                        if sumColName not in col:
                            #colWithoutLastRow = newDf.loc[(newDf.index!=sumRowName), quantityColName]
                            colWithoutLastRow = newDf.loc[newDf.index[:-1], quantityColName]
                            
                            #lastCellInCol = newDf.loc[(newDf.index==sumRowName), quantityColName]
                            lastCellInCol = newDf.loc[newDf.index[-1], quantityColName]

                            percOfDayColNameTuple = createTupleFromVals([col, percOfDayColName])
                            #percOfDayColNameTuple = createListFromVals([col, percOfDayColName])

                            newDf.loc[newDf.index[:-1], percOfDayColNameTuple] = divisionResultAsPercentage(colWithoutLastRow, lastCellInCol)

                            newDf.loc[sumRowNameTuple, percOfDayColNameTuple] = maxPercentage   if lastCellInCol   else noLessonsVal
                            
                            sumValCol = tempDf[sumColName]
                        
                        else:
                            sumValCol = tempDf.loc[sumRowNameTuple, sumColName]
                        
                        
                        percOfWeekColNameTuple = createTupleFromVals([col, percOfWeekColName])
                        #percOfWeekColNameTuple = createListFromVals([col, percOfWeekColName])
                        newDf[percOfWeekColNameTuple] = divisionResultAsPercentage(newDf[quantityColName], sumValCol)

                    #newDf.loc[(newDf.index==sumRowName), percOfWeekColNameTuple] = maxPercentage
                    newDf.loc[newDf.index[-1], newDf.columns[-1]] = maxPercentage

                    overviewDfs[sheetName].append(newDf)


            writerForListOfObjsWithMultipleDfsToJSONAndExcel(overviewDfsJSONPaths[overviewKey][i], overviewExcelPaths[overviewKey][i], overviewDfs, False)


    except Exception as e:
        msgText = handleErrorMsg('Error while creating the overviews of schedules.', getTraceback(e))
    
    if msgText: print(msgText)



def createOverviewMain(overviewKey=''):
    msgText=''

    objOfMultiDfs = readMultiDfsJSONAsObjOfDfObjLists(scheduleClassroomsGroupedResourceAllocByHoursDfsJSONPath)
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
