# variables for handling a pandas' Data Frame and an Excel content
timeIndexNames = ['Nr','Godz']
dayTimeIndexNames = ['Dzień', 'Nr', 'Godz']
dayAndAttrNames = ['Dzień', 'Atrybuty']
weekdays = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']
weekdaysLen = len(weekdays)
lessonAttrs4el = ['przedmiot', 'grupa', 'nauczyciel', 'sala']
lessonAttrs5el = ['przedmiot', 'grupa', 'nauczyciel', 'klasa', 'sala']
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
dfRowIndexNameTuples = [
    ('Nr', ''),
    ('Godz', '')
]
dfColWeekDayNameTuples3el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'grupa'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'grupa'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'grupa'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'grupa'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'grupa'), ('Piątek', 'sala')
]
dfColWeekDayNameTuples4el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'grupa'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'grupa'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'grupa'), ('Środa', 'nauczyciel'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'grupa'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'grupa'), ('Piątek', 'nauczyciel'), ('Piątek', 'sala')
]
dfColWeekDayNameTuples5el = [
    ('Poniedziałek', 'przedmiot'), ('Poniedziałek', 'grupa'), ('Poniedziałek', 'nauczyciel'), ('Poniedziałek', 'klasa'), ('Poniedziałek', 'sala'),
    ('Wtorek', 'przedmiot'), ('Wtorek', 'grupa'), ('Wtorek', 'nauczyciel'), ('Wtorek', 'klasa'), ('Wtorek', 'sala'),
    ('Środa', 'przedmiot'), ('Środa', 'grupa'), ('Środa', 'nauczyciel'), ('Środa', 'klasa'), ('Środa', 'sala'),
    ('Czwartek', 'przedmiot'), ('Czwartek', 'grupa'), ('Czwartek', 'nauczyciel'), ('Czwartek', 'klasa'), ('Czwartek', 'sala'),
    ('Piątek', 'przedmiot'), ('Piątek', 'grupa'), ('Piątek', 'nauczyciel'), ('Piątek', 'klasa'), ('Piątek', 'sala')
]
dfColName3elTuples = dfRowIndexNameTuples + dfColWeekDayNameTuples3el
dfColName4elTuples = dfRowIndexNameTuples + dfColWeekDayNameTuples4el
dfColName5elTuples = dfRowIndexNameTuples + dfColWeekDayNameTuples5el

dfRowIndexNameArrays = [
                          ['Nr', 'Godz'],
                          [''] * 2
                       ]
dfColWeekDayNameArrays4el = [
                               ['Poniedziałek'] * 4 + ['Wtorek'] * 4 + ['Środa'] * 4 + ['Czwartek'] * 4 + ['Piątek'] * 4,
                               ['przedmiot', 'grupa', 'nauczyciel', 'sala'] * 5
                             ]
dfColWeekDayNameArrays5el = [
                               ['Poniedziałek'] * 5 + ['Wtorek'] * 5 + ['Środa'] * 5 + ['Czwartek'] * 5 + ['Piątek'] * 5,
                               ['przedmiot', 'grupa', 'nauczyciel', 'klasa', 'sala'] * 5
                             ]
dfColNameArrays = [
                     dfRowIndexNameArrays[0] + dfColWeekDayNameArrays4el[0],
                     dfRowIndexNameArrays[1] + dfColWeekDayNameArrays4el[1]
                  ]

dfRowIndexNameProducts = [
                            ['Nr', 'Godz'],
                            ['']
                         ]
dfColWeekDayNameProducts4el = [
                                 ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'],
                                 ['przedmiot', 'grupa', 'nauczyciel', 'sala']
                              ]
dfColWeekDayNameProducts5el = [
                                 ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'],
                                 ['przedmiot', 'grupa', 'nauczyciel', 'klasa', 'sala']
                              ]

import numpy as np
dfColWeekDayEmptyRow = {
    ('Poniedziałek', 'przedmiot'): np.nan, ('Poniedziałek', 'grupa'): np.nan, ('Poniedziałek', 'nauczyciel'): np.nan, ('Poniedziałek', 'klasa'): np.nan, ('Poniedziałek', 'sala'): np.nan,
    ('Wtorek', 'przedmiot'): np.nan, ('Wtorek', 'grupa'): np.nan, ('Wtorek', 'nauczyciel'): np.nan, ('Wtorek', 'klasa'): np.nan, ('Wtorek', 'sala'): np.nan,
    ('Środa', 'przedmiot'): np.nan, ('Środa', 'grupa'): np.nan, ('Środa', 'nauczyciel'): np.nan, ('Środa', 'klasa'): np.nan, ('Środa', 'sala'): np.nan,
    ('Czwartek', 'przedmiot'): np.nan, ('Czwartek', 'grupa'): np.nan, ('Czwartek', 'nauczyciel'): np.nan, ('Czwartek', 'klasa'): np.nan, ('Czwartek', 'sala'): np.nan,
    ('Piątek', 'przedmiot'): np.nan, ('Piątek', 'grupa'): np.nan, ('Piątek', 'nauczyciel'): np.nan, ('Piątek', 'klasa'): np.nan, ('Piątek', 'sala'): np.nan }

colsWithNumbersNameTuples = [
                                ('Poniedziałek', 'sala'),
                                ('Wtorek', 'sala'),
                                ('Środa', 'sala'),
                                ('Czwartek', 'sala'),
                                ('Piątek', 'sala')
                             ]

colsWithNumbersNameArrays = [
                               ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek'],
                               ['sala'] * 5
                            ]

noGroupMarker = '-'
wholeClassGroupName = 'cała klasa'
classGroupsOwnerName = 'grupa'

defRowNamesLen = len(timeIndexNames)
defColNamesLen = len(dayAndAttrNames)

from pandas import CategoricalDtype
# REMINDER:
# If a CategoricalDType or a similar structure is used for the index or columns of a DataFrame,
# it is not recommended to use .levels[0] instead of .get_level_values(0).unique(), because
# the former returns all possible values of the CategoricalDType, not just the unique ones present in the data.
weekdaysCatDtype = CategoricalDtype(categories=weekdays, ordered=True)