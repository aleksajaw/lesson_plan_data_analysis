from constants.overview_constants import sumColName, sumRowName, meanRowName, meanColName, percOfDayColName, percOfDayRowName, notApplicableVal, notAvailableVal
from src.constants.schedule_structures_constants import weekdaysCatDtype
import pandas as pd
from pandas import MultiIndex
import numpy as np



def createNewMultiIndexWithNewFirstLvl(df, newFirstLvlVal, newLvlName='', isColumns=True, convertIndex=True):
    from src.utils.converters_utils import convertDigitInStrToInt
    
    indexBase = df.columns   if isColumns   else df.index

    indexData = [convertDigitInStrToInt(el)   for el in indexBase]   if convertIndex   else indexBase
    newFirstLvlVal = convertDigitInStrToInt(newFirstLvlVal)   if convertIndex   else newFirstLvlVal

    return MultiIndex.from_product([[newFirstLvlVal], indexData], names=[newLvlName]+indexBase.names)



def createNewMultiIndexForSumRow(indexNames, firstLvlVal, secondLvlVal=sumRowName, thirdLvlVal=''):
    return MultiIndex.from_tuples(tuples=[firstLvlVal + (secondLvlVal, thirdLvlVal)], names=indexNames)



def addNewCalcRowsToDf(df, calcRowName, lastIndexLvl='', isRowIndexFirstLvlADay=True):
    newMultiIndexRows = MultiIndex.from_tuples([(day, calcRowName, lastIndexLvl)   for day in df.index.get_level_values(0).unique()], names=df.index.names)
    calcRows = pd.DataFrame(data=[[np.nan] * len(df.columns)], index=newMultiIndexRows, columns=df.columns)
    df = pd.concat([df, calcRows])

    if isRowIndexFirstLvlADay:
        df = setDfLvlAsType(df, weekdaysCatDtype, sortingType='index', lvlNr=0)

    return df



def addNewSumColToDf(df, groupName=''):
    excludedIndices = [sumRowName, meanRowName, percOfDayRowName]
    excludedCols = [sumColName, meanColName, percOfDayColName]
    
    tableTitle = df.columns.get_level_values(0)[0]
    sumColTuple = (tableTitle, sumColName)

    #if groupName=='':
    indexNotExcludedMask = ~df.index.get_level_values(1).isin(excludedIndices)
    colNotExcludedMask = ~df.columns.get_level_values(1).isin(excludedCols)
        
    df.loc[indexNotExcludedMask, sumColTuple] = df.loc[indexNotExcludedMask, colNotExcludedMask].sum(axis=1, skipna=True)

    '''else:
        chosenDay = df.loc[groupName]
        indexNotExcludedMask = ~chosenDay.index.get_level_values(1).isin(excludedIndices)
        colNotExcludedMask = ~chosenDay.columns.get_level_values(1).isin(excludedCols)

        df.loc[groupName].loc[indexNotExcludedMask, sumColTuple] = chosenDay.loc[indexNotExcludedMask ].sum(axis=1, skipna=True)'''

    for indexPart in excludedIndices:
        df.loc[ (df.index.get_level_values(0), indexPart), sumColTuple ] = notApplicableVal

    return df



def addNewMeanColToDf(df, groupName=''):
    excludedIndices = [meanRowName, percOfDayRowName]
    excludedCols = [meanColName, percOfDayColName]

    tableTitle = df.columns.get_level_values(0)[0]
    meanColTuple = (tableTitle, meanColName)

    #if groupName=='':
    indexNotExcludedMask = ~df.index.get_level_values(1).isin(excludedIndices)
    colNotExcludedMask = ~df.columns.get_level_values(1).isin(excludedCols)

    df[meanColTuple] = df.loc[indexNotExcludedMask, colNotExcludedMask].fillna(0.0).mean(axis=1).round(2)

    '''else:
        chosenDay = df.loc[groupName]
        indexNotExcludedMask = ~chosenDay.index.get_level_values(1).isin(excludedIndices)
        colNotExcludedMask = ~chosenDay.columns.get_level_values(1).isin(excludedCols)

        df.loc[groupName, meanColTuple] = df.loc[indexNotExcludedMask, colNotExcludedMask].loc[groupName].fillna(0.0).mean(axis=1).round(2)'''
    
    for indexPart in excludedIndices:
        df.loc[ (df.index.get_level_values(0), indexPart), meanColTuple ] = notApplicableVal

    return df



def addNewPercColToDf(df, groupName=''):
    from converters_utils import divisionResultAsPercentage
    excludedIndices = [meanRowName, percOfDayRowName]

    tableTitle = df.columns.get_level_values(0)[0]
    percOfDayColTuple = (tableTitle, percOfDayColName)
    sumColTuple = (tableTitle, sumColName)

    #if groupName=='':
    indexNotExcludedMask = ~df.index.get_level_values(1).isin(excludedIndices)
    sumSeries = df.loc[:, sumColTuple].loc[indexNotExcludedMask]
    
    df.loc[:, percOfDayColTuple] = divisionResultAsPercentage(sumSeries, sumSeries.iloc[-1])

    '''else:
        chosenDay = df.loc[groupName]
        indexNotExcludedMask = ~chosenDay.index.get_level_values(1).isin(excludedIndices)
        sumSeries = chosenDay.loc[indexNotExcludedMask, sumColTuple]
    
        df.loc[groupName, percOfDayColTuple] = divisionResultAsPercentage(sumSeries, sumSeries.iloc[-1])'''

    for indexPart in excludedIndices:
        df.loc[ (df.index.get_level_values(0), indexPart), percOfDayColTuple ] = notApplicableVal

    return df



def setNewDfColsTitle(df, newFirstLvlVal):
    df.columns = df.columns.set_levels([newFirstLvlVal], level=0)

    return df



# Making the 1st lvl a concrete data type (for example CategoricalDType) to simplify the sorting proccess.
#
# REMINDER:
# If a CategoricalDType or a similar structure is used for the index or columns of a DataFrame,
# it will not be recommended to use df.levels[0] instead of df.get_level_values(0).unique(), because
# the former returns all possible values of the CategoricalDType, not just the unique ones present in the data.
#
# Below is the last and probably the only opportunity to use df.levels[0] in that program
# that does not present any opportunities for problems.
def setDfLvlAsType(df, dataType, sortingType='', lvlNr=0, isIndex=True):
    if isIndex:
        df.index = df.index.set_levels( df.index.levels[0].astype(dataType), level=lvlNr)

        if sortingType=='index':
            df = df.sort_index()

        elif sortingType=='values':
            df = df.sort_values(df.index.names[:-1])

    return df



def setGroupCounterInDfSumRowIndex(df, sumRowName=sumRowName):
    counterList = []

    for groupName in df.index.get_level_values(0).unique():
        counterList.append(countNonEmptyRowsInGroup(df, groupName))

    newTuples = []
    i=0

    for (idxLvl1, idxLvl2, idxLvl3) in df.index:
        
        if idxLvl2 == sumRowName:
            tupleTemp = (idxLvl1, idxLvl2, counterList[i])
            i = i+1
        else:
            tupleTemp = (idxLvl1, idxLvl2, idxLvl3)

        newTuples.append(tupleTemp)

    df.index = pd.MultiIndex.from_tuples(newTuples, names=df.index.names)

    return df



def getDfValidIndices(df):
    return (df.first_valid_index(), df.last_valid_index())



def fillMissingValsInColRowPairs(df, missingFill=notAvailableVal):
    # Fill missing values in column-row pairs, ensuring that empty cells within grouped column structures are replaced with a specified value.
    for group in df.columns.get_level_values(0).unique():
        mask = df[group].ne('').any(axis=1)
        
        for col in df[group].columns:
            df.loc[mask, (group, col)] = df.loc[mask, (group, col)].replace('', np.nan).fillna(missingFill)

    return df



def writeDfMeanOfColsToCells(df, multipleCols=True, meanKey=None, colKey=None, newVal=None, firstValidIndex=None, lastValidIndex=None, firstLvlRowMultiIndex=None):
    excludedIndices = [sumRowName, meanRowName, percOfDayRowName]
    excludedCols = [meanColName, percOfDayColName]
    keysAreNotNone = meanKey is not None   and   colKey is not None
    
    if multipleCols:
        indexNotExcludedMask = ~df.index.get_level_values(1).isin(excludedIndices)
        colNotExcludedMask = ~df.columns.get_level_values(1).isin(excludedCols)
        meanRowIndex = df.index[df.index.get_level_values(1) == meanRowName].tolist()[0]

        df.loc[meanRowIndex, colNotExcludedMask] = df.loc[indexNotExcludedMask, colNotExcludedMask].fillna(0.0).mean().round(2).values
    
    '''elif keysAreNotNone   and   newVal is not None:
        df.loc[meanKey, colKey] = newVal

    elif keysAreNotNone   and   firstValidIndex is not None   and   lastValidIndex is not None:
        df.loc[meanKey, colKey] = df.loc[firstValidIndex:lastValidIndex, colKey].fillna(0.0).mean().round(2)
        
    elif keysAreNotNone   and   firstLvlRowMultiIndex is not None:
        chosenCol = df.loc[firstLvlRowMultiIndex, colKey]
        indexNotExcludedMask = ~chosenCol.index.get_level_values(1).isin(excludedIndices)
        
        df.loc[meanKey, colKey] = chosenCol[indexNotExcludedMask].fillna(0.0).mean().round(2)'''

    return df



def writeDfSumOfColsToCells(df, multipleCols=True, sumKey=None, colKey=None, newVal=None, firstValidIndex=None, lastValidIndex=None, firstLvlRowMultiIndex=None):
    excludedIndices = [sumRowName, meanRowName, percOfDayRowName]
    excludedCols = [meanColName, percOfDayColName]
    keysAreNotNone = sumKey is not None   and   colKey is not None

    if multipleCols:
        indexNotExcludedMask = ~df.index.get_level_values(1).isin(excludedIndices)
        colNotExcludedMask = ~df.columns.get_level_values(1).isin(excludedCols)
        sumRowIndex = df.index[df.index.get_level_values(1) == sumRowName].tolist()[0]

        df.loc[sumRowIndex, colNotExcludedMask] = df.loc[indexNotExcludedMask, colNotExcludedMask].sum(skipna=True).values

    '''elif keysAreNotNone   and   newVal is not None:
        df.loc[sumKey, colKey] = newVal

    elif keysAreNotNone   and   firstValidIndex is not None   and   lastValidIndex is not None:
        df.loc[sumKey, colKey] = df.loc[firstValidIndex:lastValidIndex, colKey].sum(skipna=True)
        
    elif keysAreNotNone   and   firstLvlRowMultiIndex is not None:
        chosenCol = df.loc[firstLvlRowMultiIndex, colKey]
        indexNotExcludedMask = ~chosenCol.index.get_level_values(1).isin(excludedIndices)
        
        df.loc[sumKey, colKey] = chosenCol[indexNotExcludedMask].sum(skipna=True)'''

    return df



def writeDfColPercOfDayToCells(df, multipleCols=True, percKey=None, colKey=None, newVal=None, firstValidIndex=None, lastValidIndex=None, firstLvlRowMultiIndex=None):
    from src.utils.converters_utils import divisionResultAsPercentage
    excludedCols = [meanColName, percOfDayColName]
    keysAreNotNone = percKey is not None   and   colKey is not None

    if multipleCols:
        colNotExcludedMask = ~df.columns.get_level_values(1).isin(excludedCols)
        percOfDayRowIndex = df.index[df.index.get_level_values(1) == percOfDayRowName].tolist()[0]
        sumRowIndex = df.index[df.index.get_level_values(1) == sumRowName].tolist()[0]
        sumColIndex = df.columns[df.columns.get_level_values(1) == sumColName].tolist()[0]

        df.loc[percOfDayRowIndex, colNotExcludedMask] = divisionResultAsPercentage( df.loc[sumRowIndex, colNotExcludedMask],
                                                                                    df.loc[sumRowIndex, sumColIndex] )
        
    '''elif keysAreNotNone   and   newVal is not None:
        df.loc[percKey, colKey] = newVal

    elif keysAreNotNone   and   firstValidIndex is not None   and   lastValidIndex is not None:
        df.loc[percKey, colKey] = df.loc[firstValidIndex:lastValidIndex, colKey].sum(skipna=True)
        
    elif keysAreNotNone   and   firstLvlRowMultiIndex is not None:
        chosenCol = df.loc[firstLvlRowMultiIndex, colKey]
        percOfDayRowIndex = chosenCol.index[chosenCol.index.get_level_values(1) == percOfDayRowName].tolist()[0]
        sumRowIndex = chosenCol.index[chosenCol.index.get_level_values(1) == sumRowName].tolist()[0]
        
        df.loc[percOfDayRowIndex, colKey] = divisionResultAsPercentage( chosenCol.loc[sumRowIndex, colNotExcludedMask],
                                                                        chosenCol.loc[sumRowIndex, sumColIndex] )'''
    
    return df



# Completely transform DataFrame into a vertical order where column names become the 1st level of the MultiIndex for the rows.
def completelyTransformDfToVerticalOrder(df, dfName, newDfLvlName):
    df = df.stack( level=0, dropna=False)
    
    # Correct the order of the levels in the hierarchy.
    df = reorderDfLvls(df, newOrder=[2,0,1], isRowIndexFirstLvlADay=True)
    
    # Add the parent value for the class columns.
    df.columns = createNewMultiIndexWithNewFirstLvl(df, dfName, newDfLvlName.capitalize())

    #df = removeDfEmptyRows(df)
    df = removeDuplicatedDfRows(df)

    return df



# Correct the order of the levels in the hierarchy.
def reorderDfLvls(df, newOrder, isIndex=True, isRowIndexFirstLvlADay=True):
    if isIndex:
        df.index = df.index.reorder_levels( newOrder )

    else:
        df.columns = df.columns.reorder_levels( newOrder )

    if isRowIndexFirstLvlADay:
        df = setDfLvlAsType(df, weekdaysCatDtype, 'values')

    return df



def combineTwoDfsWithDifferentIndices(df1, df2):
    # THE IMPORTANT WAY TO COMBINE TWO DATAFRAMES WHICH DIFFER IN INDICES.

    # Create a new column named 'idx_temp' containing the numeric index.
    df1['idx_temp'] = df1.groupby(df1.index).cumcount()
    df2['idx_temp'] = df2.groupby(df2.index).cumcount()

    # Set the column 'idx_temp' as an extra lvl of the current DataFrame index.
    df1 = df1.set_index(['idx_temp'], append=True)
    df2 = df2.set_index(['idx_temp'], append=True)

    # Combine two DataFrames along the columns axis
    # and then remove the 'idx_temp' level from the MultiIndex, completely removing it from the columns.
    merged = ( pd.concat([df1, df2], axis=1).reset_index(level=['idx_temp'], drop=True)
                                            .sort_index() )    
    return merged



def removeDfUnnamedCols(df):
    if not df.empty:
        unnamedCols = df.columns.get_level_values(0).str.contains('Unnamed', na=False)
        if unnamedCols.any():
            df = df.loc[:, ~unnamedCols]

    return df



def removeDfEmptyRows(df):
    df = df[~(df == '').all(axis=1)]

    return df



def removeDuplicatedDfRows(df, keepType='first', checkEmptiness=True):
    # The index level in this function is used due to errors with different lesson times for the same lesson number depending on the class on the scraped page.
    if checkEmptiness:
        # Check which rows are empty (contain only NaN or empty strings).
        isRowEmptyMask = df.isna().all(axis=1) | df.eq('').all(axis=1)
                
        # Filter the DataFrame using the mask that removes the rows that are both empty and duplicates (which means indices appear more than once).
        df = df[~(isRowEmptyMask   &   df.index.get_level_values(1).duplicated(keep=False))]#.fillna('-')

    elif keepType is not None:
        # Check which indices appear more than once, but by default, mark duplicated index rows except for the first occurrence.
        df = df[~df.index.get_level_values(1).duplicated(keep=keepType)]#.fillna('-')

    return df



def retainOnlyFirstCellsInDfGroups(df, axisNr=1, lvlNr=0):
    df = df.groupby(axis=axisNr, level=lvlNr, sort=False).first()

    return df



def countNonEmptyRowsInGroup(df, groupName):
    excludedIndices = [sumRowName, meanRowName, percOfDayRowName]
    indexNotExcludedMask = ~df.index.get_level_values(1).isin(excludedIndices)

    sumColTuple = (df.columns.get_level_values(0)[0], sumColName)

    return df[indexNotExcludedMask].loc[groupName, sumColTuple].gt(0).sum()



def convertDfValsToBinaryStates(df, useInt=True, useNan=True):
    emptyVal = np.nan   if useNan   else 0   if useInt   else 0.0
    filledVal = 1   if useInt   else 1.0

    excludedIndices = [sumRowName, meanRowName, percOfDayRowName]
    indexNotExcludedMask = ~df.index.get_level_values(1).isin(excludedIndices)

    df.loc[indexNotExcludedMask] = df.loc[indexNotExcludedMask].map(lambda val: filledVal   if pd.isna(val)   or   val in ['', 0, 0.0, None]
                                                                                            else emptyVal)

    return df



def convertDfValsToCounters(df, lvlList=[0], retainOnlyLastRows=True):
    df = ( df.map(lambda val: 1   if val   else np.nan)
             .groupby(level=lvlList, sort=False)
             .cumsum() )
    
    if retainOnlyLastRows:
        df = removeDuplicatedDfRows(df, keepType='last', checkEmptiness=False)
    
    return df