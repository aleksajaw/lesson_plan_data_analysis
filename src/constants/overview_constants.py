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

sumColName = 'Razem'
sumRowName = 'Razem'

amountColName = 'Ilość'
percOfDayColName = 'Udział w dniu'
percOfWeekColName = 'Udział w tygodniu'

#notApplicableVal = 'nie dotyczy'
notApplicableVal = 'N/A'
noLessonsVal = 'brak zajęć'

nrOfOccurrColName = 'Ilość wystąpień'
meanColName = 'Średnia'
meanRowName = 'Średnia'

nrOfClassesPerHourName = 'ilość zajęć na godz.'

calcRowAndColNames = ['Średnia', 'Suma']

classroomTableName = ' sal'

occupancyTableName = 'Obłożenie'
classroomOccupancyTableName = occupancyTableName + classroomTableName

gapsTableName = '"Okienka" w planie'
classroomGapsTableName = gapsTableName + classroomTableName

availabilityTableName = 'Dostępność'
classroomAvailabilityTableName = availabilityTableName + classroomTableName

