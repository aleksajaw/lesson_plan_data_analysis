import uuid
from utils import *


class Break:
    def __init__(self, id, name, breakNumber, startTime, endTime):
        self.id = id or self._generateId()
        self.name = name
        self.breakNumber = breakNumber
        self.startTime = startTime
        self.endTime = endTime

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class LessonHour:
    def __init__(self, id, lessonNr, startTime, endTime):
        self.id = id or self._generateId()
        self.lessonNr = lessonNr
        self.startTime = startTime
        self.endTime = endTime

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

class Lesson:
    def __init__(self, id, subjectId, teacherId, classroomId, lessonHourId, schoolClassGroupId, schoolClassId):
        self.id = id or self._generateId()
        self.subjectId = subjectId
        self.teacherId = teacherId
        self.classroomId = classroomId
        self.lessonHourId = lessonHourId
        self.schoolClassGroupId = schoolClassGroupId
        self.schoolClassId = schoolClassId

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class Schedule:
    def __init__(self, id):
        self.id = id or self._generateId()
        self.timetable = []

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    def addEvent(self, lesson):
        self.timetable.append(lesson)



class School:
    def __init__(self, id, name, symbol):
        #, type, nrOfStudents
        self.id = id or self._generateId()
        self.name = name
        self.symbol = symbol
        '''self.type = type
        self.nrOfStudents = nrOfStudents'''
        self.classrooms = []
        self.teachers = []
        self.subjects = []

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    def addClassroom(self, classroom):
        self.classrooms.append(classroom)



class Teacher:
    def __init__(self, id, symbol, possibleClassrooms):
        #, type
        self.id = id or self._generateId()
        self.symbol = symbol
        '''self.type = type'''
        self.possibleClassrooms = possibleClassrooms or []

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class Classroom:
    def __init__(self, id, symbol):
        #, name, type, capacity, substitute
        self.id = id or self._generateId()
        self.symbol = symbol
        '''self.name = name
        self.type = type
        self.capacity = capacity
        self.substitutes = substitutes'''

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class SchoolClass:
    def __init__(self, id, name, symbol):
        #, type, schoolClassGroups, nrOfStudents
        self.id = id or self._generateId()
        self.symbol = symbol
        self.name = name
        '''self.type = type
        self.schoolClassGroups = []
        self.nrOfStudents = nrOfStudents'''

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class SchoolClassGroup:
    def __init__(self, id, symbol, schoolClassId):
        #, name, type, nrOfStudents
        self.id = id if id else self._generateId()
        self.symbol = symbol
        self.schoolClassId = schoolClassId
        '''self.name = name
        self.type = type
        self.nrOfStudents = nrOfStudents'''

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    '''def isLanguage(self):
        isType(self, "Language")

    def isPE(self):
        isType(self, "Physical Education")

    def isGirls(self):
        isType(self, "Girls")
    
    def isBoys(self):
        isType(self, "Boys")

    def isVocational(self):
        isType(self, "Vocational")'''



class Subject:
    def __init__(self, id, symbol):
        #, name, type, occurrenceMethods, possibleSchoolClasses, possibleClassGroups, possibleTeachers, possibleClassrooms
        self.id = id if id else self._generateId()
        self.symbol = symbol
        '''self.name = name
        self.type = type
        self.occurrenceMethods = occurrenceMethods or {"single": 1, "double": 0, "triple": 0}
        self.possibleSchoolClasses = possibleSchoolClasses
        self.possibleClassGroups = possibleClassGroups
        self.possibleTeachers = possibleTeachers or []
        self.possibleClassrooms = possibleClassrooms or []'''

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    '''def hasSingleOccurrence(self):
        return self.occurrenceMethods.get("single", 0) > 0

    def hasDoubleOccurrence(self):
        return self.occurrenceMethods.get("double", 0) > 0

    def hasTripleOccurrence(self):
        return self.occurrenceMethods.get("triple", 0) > 0

    def isHumanistic(self):
        isType(self, "Humanistic")

    def isScientific(self):
        isType(self, "Scientific")

    def isArtistic(self):
        isType(self, "Artistic")'''



class Profile:
    def __init__(self, type, long, short):
        self.type = type
        self.long = long
        self.short = short

    def getShort(self):
        return self.short

class TechnicalProfile(Profile):
    def __init__(self, long, short):
        super().__init__('t', long, short)

class MultitradeProfile(Profile):
    def __init__(self, long, short):
        super().__init__('z', long, short)

class HighSchoolProfile(Profile):
    def __init__(self, long, short):
        super().__init__('lo', long, short)


classProfiles = {
    'ek': TechnicalProfile('Technik ekonomista', 'ekonomik'),
    'fry': TechnicalProfile('Technik usług fryzjerskich', 'fryzjer'),
    'gas': TechnicalProfile('Technik żywienia i usług gastronomicznych', 'gastronom'),
    'ha': TechnicalProfile('Technik handlowiec', 'handlowiec'),
    'hot': TechnicalProfile('Technik hotelarstwa', 'hotelarz'),
    'log': TechnicalProfile('Technik logistyk', 'logistyk'),
    'ra': TechnicalProfile('Technik rachunkowości', 'rachunkowość'),
    'sport': HighSchoolProfile('Klasa sportowa', 'sportowa'),
    'wz': MultitradeProfile('Oddział wielozawodowy', 'wielozawodowa')
}