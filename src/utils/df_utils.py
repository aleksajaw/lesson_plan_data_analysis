from converters_utils import convertDigitInStrToInt
from constants.overview_constants import sumCellsInRowsColName, sumCellsInColsRowName
from src.constants.schedule_structures_constants import weekdaysCatDtype
import pandas as pd
from pandas import MultiIndex
import numpy as np



def createNewMultiIndexWithNewFirstLvl(df, newFirstLvlVal, newLvlName='', isColumns=True, convertIndex=True):
    indexBase = df.columns   if isColumns   else df.index

    colsData = [convertDigitInStrToInt(col)   for col in indexBase]   if convertIndex   else indexBase

    return MultiIndex.from_product([[newFirstLvlVal], colsData], names=[newLvlName]+indexBase.names)



def createNewMultiIndexForSumRow(indexNames, firstLvlVal, secondLvlVal='', thirdLvlVal=sumCellsInColsRowName):
    return MultiIndex.from_tuples(tuples=[firstLvlVal + (secondLvlVal, thirdLvlVal)], names=indexNames)



def setNewDfColsFirstLvl(df, newFirstLvlVal):
    df.columns = df.columns.set_levels([newFirstLvlVal], level=0)

    return df



def addNewSumColToDf(df, sumColName=sumCellsInRowsColName):
    df[(df.columns.get_level_values(0)[0], sumColName)] = df.sum(axis=1)

    return df



def addNewSumRowsToDf(df, isRowIndexFirstLvlADay=True, sumRowName=sumCellsInColsRowName):
    newMultiIndexRows = MultiIndex.from_tuples([(day, '', sumRowName)   for day in df.index.get_level_values(0).unique()], names=df.index.names)
    sumRows = pd.DataFrame(data=[[np.nan] * len(df.columns)], index=newMultiIndexRows, columns=df.columns)
    df = pd.concat([df, sumRows])

    if isRowIndexFirstLvlADay:
        df = setDfLvlAsType(df, weekdaysCatDtype, sortingType='index', lvlNr=0)

    return df



def writeDfColSumToCell(df, keySum, col, newVal=None, firstValidIndex=None, lastValidIndex=None, firstLvlRowMultiIndex=None):
    if newVal is not None:
        df.loc[keySum, col] = newVal

    elif firstValidIndex is not None   and   lastValidIndex is not None:
        df.loc[keySum, col] = df.loc[firstValidIndex:lastValidIndex, col].sum(skipna=True)
        
    elif firstLvlRowMultiIndex is not None:
        df.loc[keySum, col] = df.loc[firstLvlRowMultiIndex, col][:-1].sum(skipna=True)
    
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
    merged = pd.concat([df1, df2], axis=1).reset_index(level=['idx_temp'], drop=True)

    return merged.sort_index()



def removeDfEmptyRows(df):
    df = df[~(df == '').all(axis=1)]

    return df



def removeDuplicatedDfRows(df, keepType='first', checkEmptiness=True):
    if checkEmptiness:
        isRowEmptyMask = df.isna().all(axis=1) | (df == '').all(axis=1)
        df = df[~(isRowEmptyMask   &   df.index.duplicated(keep=keepType))]#.fillna('-')

    else:
        df = df[~df.index.duplicated(keep=keepType)]#.fillna('-')

    return df



def convertDfValsToCounters(df, lvlList=[0], retainOnlyLastRows=True):
    df = ( df.map(lambda val: 1   if val   else np.nan)
             .groupby(level=lvlList, sort=False)
             .cumsum() )
    
    if retainOnlyLastRows:
        df = removeDuplicatedDfRows(df, keepType='last', checkEmptiness=False)
    
    return df



def convertDfValsToBinaryStates(df, useInt=True, useNan=True):
    emptyVal = np.nan   if useNan   else 0   if useInt   else 0.0
    filledVal = 1   if useInt   else 1.0

    df = df.map(lambda val: filledVal   if pd.isna(val)   or   val in ['', 0, 0.0, None]   else emptyVal)

    return df



def retainOnlyFirstCellsInDfGroups(df, axisNr=1, lvlNr=0):
    df = df.groupby(axis=axisNr, level=lvlNr, sort=False).first()

    return df



def getDfValidIndices(df):
    return (df.first_valid_index(), df.last_valid_index())



# Correct the order of the levels in the hierarchy.
def reorderDfLvls(df, newOrder, isIndex=True, isRowIndexFirstLvlADay=True):
    if isIndex:
        df.index = df.index.reorder_levels( newOrder )

    else:
        df.columns = df.columns.reorder_levels( newOrder )

    if isRowIndexFirstLvlADay:
        df = setDfLvlAsType(df, weekdaysCatDtype, 'values')

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