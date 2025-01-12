# INITIAL VARIABLES
schoolAndPlanURLs = [ ('https://zamkowa15.edu.pl', '/plan/plan.html'),
                      ('https://www.mechaniksieradz.edu.pl', '/DANE/Plan/Uczen/biezacy/') ]

schoolURL, partPlanURL = schoolAndPlanURLs[0]
planURL = schoolURL + partPlanURL

# frame name attributes
linksFrameName = 'list'
planFrameName = 'plan'

# table week days
weekdays = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek']

# driver constant
driverLocationStates = ['default', 'list', 'plan']

# VARIABLES FOR EXCEL CREATOR
#excelEngineName = 'xlsxwriter'
excelEngineName = 'openpyxl'
draftSheetName = 'draft_sheet'