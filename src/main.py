import uuid
from utils import *
import matplotlib.pyplot as plt


class Break:
    def __init__(self, id=None, name=None, breakNumber=None, startTime=None, endTime=None):
        self.id = id if id is not None else self._generateId()
        self.name = name
        self.breakNumber = breakNumber
        self.startTime = startTime
        self.endTime = endTime

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class LessonHour:
    def __init__(self, id=None, lessonNumber=None, startTime=None, endTime=None):
        self.id = id if id is not None else self._generateId()
        self.lessonNumber = lessonNumber
        self.startTime = startTime
        self.endTime = endTime

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class Lesson:
    def __init__(self, id=None, subject=None, teacher=None, classroom=None, lessonHour=None, schoolClassGroup=None, schoolClass=None):
        self.id = id if id is not None else self._generateId()
        self.subject = subject
        self.teacher = teacher
        self.classroom = classroom
        self.lessonHour = lessonHour
        self.schoolClassGroup = schoolClassGroup
        self.schoolClass = schoolClass

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class Schedule:
    def __init__(self, id=None):
        self.id = id if id is not None else self._generateId()
        self.timetable = []

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    def addEvent(self, lesson, lessonHourNumber):
        self.timetable.append((lesson, lessonHourNumber))



class School:
    def __init__(self, id=None, name=None, symbol=None, type=None, address=None, email=None, phone=None, numberOfStudents=None):
        self.id = id if id is not None else self._generateId()
        self.name = name
        self.symbol = symbol
        self.type = type
        self.address = address
        self.email = email
        self.phone = phone
        self.numberOfStudents = numberOfStudents
        self.classrooms = []

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    def addClassroom(self, classroom):
        self.classrooms.append(classroom)



class Teacher:
    def __init__(self, id=None, name=None, symbol=None, type=None, possibleClassrooms=None):
        self.id = id if id is not None else self._generateId()
        self.name = name
        self.symbol = symbol
        self.type = type
        self.possibleClassrooms = possibleClassrooms or []

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class Classroom:
    def __init__(self, id=None, name=None, symbol=None, type=None, capacity=None, substitute=None):
        self.id = id if id is not None else self._generateId()
        self.name = name
        self.symbol = symbol
        self.type = type
        self.capacity = capacity
        self.substitute = substitute

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class SchoolClass:
    def __init__(self, id=None, name=None, symbol=None, type=None, school=None, numberOfStudents=None):
        self.id = id if id is not None else self._generateId()
        self.name = name
        self.symbol = symbol
        self.type = type
        self.school = school
        self.numberOfStudents = numberOfStudents

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())



class SchoolClassGroup:
    def __init__(self, id=None, name=None, symbol=None, type=None, schoolClass=None, numberOfStudents=None):
        self.id = id if id is not None else self._generateId()
        self.name = name
        self.symbol = symbol
        self.type = type
        self.schoolClass = schoolClass
        self.numberOfStudents = numberOfStudents

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    def isLanguage(self):
        isType(self, "Language")

    def isPE(self):
        isType(self, "Physical Education")

    def isGirls(self):
        isType(self, "Girls")
    
    def isBoys(self):
        isType(self, "Boys")

    def isVocational(self):
        isType(self, "Vocational")



class Subject:
    def __init__(self, id=None, name=None, symbol=None, type=None, occurrenceMethods=None, possibleSchoolClass=None, possibleClassGroup=None, possibleTeachers=None, possibleClassrooms=None):
        self.id = id if id is not None else self._generateId()
        self.name = name
        self.symbol = symbol
        self.type = type
        self.occurrenceMethods = occurrenceMethods or {"single": 1, "double": 0, "triple": 0}
        self.possibleSchoolClass = possibleSchoolClass
        self.possibleClassGroup = possibleClassGroup
        self.possibleTeachers = possibleTeachers or []
        self.possibleClassrooms = possibleClassrooms or []

    @staticmethod
    def _generateId():
        return str(uuid.uuid4())

    def hasSingleOccurrence(self):
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
        isType(self, "Artistic")

