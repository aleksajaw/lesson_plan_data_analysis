from schedule_structures_constants import timeIndexNames
introColName = 'Wstęp'

basicTableTitleLvlName = 'Tytuł'

dataTypeColsLvlName = 'Typ danych'
dayOrderColName = 'Lp.'
dayColName = 'Dzień'

overviewColIndexLastLvlName = dataTypeColsLvlName

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

classroomTableName = ' sal'

occupancyTableName = 'Obłożenie'
classroomOccupancyTableName = occupancyTableName + classroomTableName

gapsTableName = '"Okienka" w planie'
classroomGapsTableName = gapsTableName + classroomTableName

availabilityTableName = 'Dostępność'
classroomAvailabilityTableName = availabilityTableName + classroomTableName

