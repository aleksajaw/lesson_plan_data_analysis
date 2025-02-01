# variables for handling a pandas' Data Frame and an Excel content
timeIndexNames = ['Nr','Godz']
dayAndAttrNames = ['Dzień', 'Atrybuty']
weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
lessonAttrs3el = ['przedmiot', 'grupa', 'nauczyciel', 'sala']
lessonAttrs4el = ['przedmiot', 'nauczyciel', 'klasa', 'sala']
dfRowNrs = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12
]
lessonTimePeriods = [
    '8:00-8:45',
    '8:50-9:35',
    '9:40-10:25',
    '10:40-11:25',
    '11:30-12:15',
    '12:20-13:05',
    '13:10-13:55',
    '14:10-14:55',
    '15:00-15:45',
    '15:50-16:35',
    '16:40-17:25',
    '17:30-18:15'
]
dfRowNrAndTimeTuples = [
    (1, '8:00-8:45'),
    (2, '8:50-9:35'),
    (3, '9:40-10:25'),
    (4, '10:40-11:25'),
    (5, '11:30-12:15'),
    (6, '12:20-13:05'),
    (7, '13:10-13:55'),
    (8, '14:10-14:55'),
    (9, '15:00-15:45'),
    (10, '15:50-16:35'),
    (11, '16:40-17:25'),
    (12, '17:30-18:15')
]
dfRowIndexNamesTuples = [
    ('Nr', ''),
    ('Godz', '')
]
dfColWeekDayNamesTuples4el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'grupa'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'grupa'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'grupa'), ('Środa', 'nauczyciel'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'grupa'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'grupa'), ('Piątek', 'nauczyciel'), ('Piątek', 'sala')
]
dfColWeekDayNamesTuples5el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'grupa'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'klasa'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'grupa'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'klasa'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'grupa'), ('Środa', 'nauczyciel'), ('Środa', 'klasa'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'grupa'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'klasa'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'grupa'), ('Piątek', 'nauczyciel'), ('Piątek', 'klasa'), ('Piątek', 'sala')
]
dfColNamesTuples = dfRowIndexNamesTuples + dfColWeekDayNamesTuples4el
# dfColNamesTuples = [('Nr', ''), ('Godz', '')] + [(day, attr) for day in weekdays for attr in lessonAttrs]

import numpy as np
dfColWeekDayEmptyRow = {
    ('Poniedziałek', 'przedmiot'): np.nan, ('Poniedziałek', 'grupa'): np.nan, ('Poniedziałek', 'nauczyciel'): np.nan, ('Poniedziałek', 'klasa'): np.nan, ('Poniedziałek', 'sala'): np.nan,
    ('Wtorek', 'przedmiot'): np.nan, ('Wtorek', 'grupa'): np.nan, ('Wtorek', 'nauczyciel'): np.nan, ('Wtorek', 'klasa'): np.nan, ('Wtorek', 'sala'): np.nan,
    ('Środa', 'przedmiot'): np.nan, ('Środa', 'grupa'): np.nan, ('Środa', 'nauczyciel'): np.nan, ('Środa', 'klasa'): np.nan, ('Środa', 'sala'): np.nan,
    ('Czwartek', 'przedmiot'): np.nan, ('Czwartek', 'grupa'): np.nan, ('Czwartek', 'nauczyciel'): np.nan, ('Czwartek', 'klasa'): np.nan, ('Czwartek', 'sala'): np.nan,
    ('Piątek', 'przedmiot'): np.nan, ('Piątek', 'grupa'): np.nan, ('Piątek', 'nauczyciel'): np.nan, ('Piątek', 'klasa'): np.nan, ('Piątek', 'sala'): np.nan }

colWithNumbersNames = [ ('Poniedziałek', 'sala'),
                        ('Wtorek', 'sala'),
                        ('Środa', 'sala'),
                        ('Czwartek', 'sala'),
                        ('Piątek', 'sala') ]

noGroupMarker = '-'
wholeClassGroupName = 'cała klasa'
sumRowsCellName = 'Razem'
sumColsCellName = 'Razem'

excelFontSize = 11
excelMargin = { 'row' : 1,
                'col' : 1 }

excelDistance = { 'row' : 1,
                  'col' : 1 }

excelRangeStartCol = excelMargin['col'] + 1
excelRangeStartRow = excelMargin['row'] + 1