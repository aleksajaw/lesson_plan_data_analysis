from constants.overview_constants import sumColName, sumRowName, meanRowName, meanColName, notApplicableVal, notAvailableVal
from src.constants.schedule_structures_constants import weekdaysCatDtype
import pandas as pd
from pandas import MultiIndex
import numpy as np



def createNewMultiIndexWithNewFirstLvl(df, newFirstLvlVal, newLvlName='', isColumns=True, convertIndex=True):
    from src.utils.converters_utils import convertDigitInStrToInt
    
    indexBase = df.columns   if isColumns   else df.index

    colsData = [convertDigitInStrToInt(col)   for col in indexBase]   if convertIndex   else indexBase
    newFirstLvlVal = convertDigitInStrToInt(newFirstLvlVal)   if convertIndex   else newFirstLvlVal

    return MultiIndex.from_product([[newFirstLvlVal], colsData], names=[newLvlName]+indexBase.names)



def createNewMultiIndexForSumRow(indexNames, firstLvlVal, secondLvlVal=sumRowName, thirdLvlVal=''):
    return MultiIndex.from_tuples(tuples=[firstLvlVal + (secondLvlVal, thirdLvlVal)], names=indexNames)



def addNewCalcRowsToDf(df, calcRowName, lastIndexLvl='', isRowIndexFirstLvlADay=True):
    newMultiIndexRows = MultiIndex.from_tuples([(day, calcRowName, lastIndexLvl)   for day in df.index.get_level_values(0).unique()], names=df.index.names)
    calcRows = pd.DataFrame(data=[[np.nan] * len(df.columns)], index=newMultiIndexRows, columns=df.columns)
    df = pd.concat([df, calcRows])

    if isRowIndexFirstLvlADay:
        df = setDfLvlAsType(df, weekdaysCatDtype, sortingType='index', lvlNr=0)

    return df



def addNewSumColToDf(df, sumColName=sumColName):
    #excludedIndices = [meanRowName]
    sumColTuple = (df.columns.get_level_values(0)[0], sumColName)
    meanColTuple = (df.index.get_level_values(0)[0], meanColName)

    df[sumColTuple] = df.sum(axis=1)

    df.loc[meanColTuple, sumColTuple] = notApplicableVal

    return df



def addNewMeanColToDf(df, meanColName=meanColName):
    #excludedIndices = [sumRowName, meanRowName]
    excludedCols = [sumColName]
    meanColTuple = (df.columns.get_level_values(0)[0], meanColName)

    df[meanColTuple] = ( df.drop(columns=excludedCols, level=1, axis=1).fillna(0.0)
                           .mean(axis=1).round(2) )

    return df



def setNewDfColsTitle(df, newFirstLvlVal):
    df.columns = df.columns.set_levels([newFirstLvlVal], level=0)

    return df



# Making the 1st lvl a concrete data type (for example CategoricalDType) to simplify the sorting proccess.
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



def writeDfColMeanToCell(df, meanKey, col, newVal=None, firstValidIndex=None, lastValidIndex=None, firstLvlRowMultiIndex=None):
    excludedIndices = [sumRowName, meanRowName]
    
    if newVal is not None:
        df.loc[meanKey, col] = newVal

    elif firstValidIndex is not None   and   lastValidIndex is not None:
        df.loc[meanKey, col] = df.loc[firstValidIndex:lastValidIndex, col].fillna(0.0).mean().round(2)
        
    elif firstLvlRowMultiIndex is not None:
        df.loc[meanKey, col] = df.loc[firstLvlRowMultiIndex, col].drop(index=excludedIndices).fillna(0.0).mean().round(2)
    
    return df



def writeDfColSumToCell(df, sumKey, col, newVal=None, firstValidIndex=None, lastValidIndex=None, firstLvlRowMultiIndex=None):
    excludedIndices = [sumRowName, meanRowName]

    if newVal is not None:
        df.loc[sumKey, col] = newVal

    elif firstValidIndex is not None   and   lastValidIndex is not None:
        df.loc[sumKey, col] = df.loc[firstValidIndex:lastValidIndex, col].sum(skipna=True)
        
    elif firstLvlRowMultiIndex is not None:
        
        df.loc[sumKey, col] = df.loc[firstLvlRowMultiIndex, col].drop(index=excludedIndices).fillna(0.0).sum(skipna=True)
    
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
    unnamedCols = df.columns.get_level_values(0).str.contains('Unnamed', na=False)
    if unnamedCols.any():
        df = df.loc[:, ~unnamedCols]

    return df



def removeDfEmptyRows(df):
    df = df[~(df == '').all(axis=1)]

    return df



def removeDuplicatedDfRows(df, keepType='first', checkEmptiness=True):
    if checkEmptiness:
        # Check which rows are empty (contain only NaN or empty strings).
        isRowEmptyMask = df.isna().all(axis=1) | df.eq('').all(axis=1)

        # Check which indices appear more than once.
        duplicatedRows = df.index.duplicated(keep=False)
        
        # Create a mask that will be used to remove the rows that are both empty and duplicates.
        isRowEmptyAndDuplicatedMask = (isRowEmptyMask   &   duplicatedRows)
        
        # Filter the DataFrame using the mask.
        df = df.loc[~isRowEmptyAndDuplicatedMask]#.fillna('-')

    elif keepType is not None:
        # Check which indices appear more than once, but by default, mark duplicated index rows except for the first occurrence.
        duplicatedRows = df.index.duplicated(keep=keepType)
        df = df[~duplicatedRows]#.fillna('-')

    return df



def retainOnlyFirstCellsInDfGroups(df, axisNr=1, lvlNr=0):
    df = df.groupby(axis=axisNr, level=lvlNr, sort=False).first()

    return df



def countNonEmptyRowsInGroup(df, groupName):
    isRowEmptyMask = df.isna().all(axis=1) | (df == '').all(axis=1)
    excludedIndices = [sumRowName, meanRowName]

    return df[~(isRowEmptyMask)].loc[groupName].drop(index=excludedIndices).sum(axis=1).gt(0).sum()



def convertDfValsToBinaryStates(df, useInt=True, useNan=True):
    emptyVal = np.nan   if useNan   else 0   if useInt   else 0.0
    filledVal = 1   if useInt   else 1.0

    df = df.map(lambda val: filledVal   if pd.isna(val)   or   val in ['', 0, 0.0, None]   else emptyVal)

    return df



def convertDfValsToCounters(df, lvlList=[0], retainOnlyLastRows=True):
    df = ( df.map(lambda val: 1   if val   else np.nan)
             .groupby(level=lvlList, sort=False)
             .cumsum() )
    
    if retainOnlyLastRows:
        df = removeDuplicatedDfRows(df, keepType='last', checkEmptiness=False)
    
    return df