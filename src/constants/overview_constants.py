from schedule_structures_constants import timeIndexNames
introColName = 'Wstęp'
dataTypeColName = 'Typ danych'
dayOrderColName = 'Lp.'
dayColName = 'Dzień'

overviewColIndexLastLvlName = dataTypeColName

#overviewsByDaysColIndexNames = [dayOrderColName, dayColName, overviewColIndexLastLvlName]
overviewsByDaysColIndexNames = [dayColName, overviewColIndexLastLvlName]
overviewsByHoursColIndexNames = timeIndexNames + [overviewColIndexLastLvlName]

overviewsMainByDaysColIndexNames = [dayOrderColName, dayColName]#, overviewColIndexLastLvlName]

sumCellsInRowsColName = 'Razem'
sumCellsInColsRowName = 'Razem'

amountColName = 'Ilość'
percOfDayColName = 'Udział w dniu'
percOfWeekColName = 'Udział w tygodniu'

#notApplicableVal = 'nie dotyczy'
notApplicableVal = 'N/A'
noLessonsVal = 'brak zajęć'

nrOfOccurrColName = 'Ilość wystąpień'
meanColName = 'Średnia'