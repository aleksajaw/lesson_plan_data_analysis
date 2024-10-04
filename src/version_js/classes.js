import { uuid } from 'uuidv4';

class Break {
    constructor(id, name, breakNumber, startTime, endTime) {
        this.id = id || this._generateId();
        this.name = name;
        this.breakNumber = breakNumber;
        this.startTime = startTime;
        this.endTime = endTime;
    }

    static _generateId() {
        return uuid.v4();
    }
}

class LessonHour {
    constructor(id, lessonNr, startTime, endTime) {
        this.id = id || this._generateId();
        this.lessonNr = lessonNr;
        this.startTime = startTime;
        this.endTime = endTime;
    }

    static _generateId() {
        return uuid.v4();
    }
}

class Lesson {
    constructor(id, subjectId, teacherId, classroomId, lessonHourId, schoolClassGroupId, schoolClassId) {
        this.id = id || this._generateId();
        this.subjectId = subjectId;
        this.teacherId = teacherId;
        this.classroomId = classroomId;
        this.lessonHourId = lessonHourId;
        this.schoolClassGroupId = schoolClassGroupId;
        this.schoolClassId = schoolClassId;
    }

    static _generateId() {
        return uuid.v4();
    }
}

class Schedule {
    constructor(id) {
        this.id = id || this._generateId();
        this.timetable = [];
    }

    _generateId() {
        return uuid.v4();
    }

    addEvent(lesson) {
        this.timetable.push(lesson);
    }
}

class School {
    constructor(id, name, symbol) {
        this.id = id || this._generateId();
        this.name = name;
        this.symbol = symbol;
        //this.type = type;
        //this.nrOfStudents = nrOfStudents;
        this.classrooms = [];
        this.teachers = [];
        this.subjects = [];
    }

    _generateId() {
        return uuid.v4();
    }

    addClassroom(classroom) {
        this.classrooms.push(classroom);
    }
}

class Teacher {
    constructor(id, symbol, possibleClassrooms) {
        //this.type = type;
        this.id = id || this._generateId();
        this.symbol = symbol;
        this.possibleClassrooms = possibleClassrooms || [];
    }

    _generateId() {
        return uuid.v4();
    }
}

class Classroom {
    constructor(id, symbol) {
        //this.name = name;
        //this.type = type;
        //this.capacity = capacity;
        //this.substitutes = substitutes;
        this.id = id || this._generateId();
        this.symbol = symbol;
    }

    _generateId() {
        return uuid.v4();
    }
}

class SchoolClass {
    constructor(id, name, symbol) {
        //this.type = type;
        //this.schoolClassGroups = [];
        //this.nrOfStudents = nrOfStudents;
        this.id = id || this._generateId();
        this.symbol = symbol;
        this.name = name;
    }

    _generateId() {
        return uuid.v4();
    }
}

class SchoolClassGroup {
    constructor(id, symbol, schoolClassId) {
        //this.name = name;
        //this.type = type;
        //this.nrOfStudents = nrOfStudents;
        this.id = id || this._generateId();
        this.symbol = symbol;
        this.schoolClassId = schoolClassId;
    }

    _generateId() {
        return uuid.v4();
    }
    /*
    isLanguage() {
        isType(this, "Language");
    }

    isPE() {
        isType(this, "Physical Education");
    }

    isGirls() {
        isType(this, "Girls");
    }

    isBoys() {
        isType(this, "Boys");
    }

    isVocational() {
        isType(this, "Vocational");
    }
    */
}

class Subject {
    constructor(id, symbol) {
        //this.name = name;
        //this.type = type;
        //this.occurrenceMethods = occurrenceMethods || {"single": 1, "double": 0, "triple": 0};
        //this.possibleSchoolClasses = possibleSchoolClasses;
        //this.possibleClassGroups = possibleClassGroups;
        //this.possibleTeachers = possibleTeachers || [];
        //this.possibleClassrooms = possibleClassrooms || [];
        this.id = id || this._generateId();
        this.symbol = symbol;
    }

    _generateId() {
        return uuid.v4();
    }
    /*
    hasSingleOccurrence() {
        return this.occurrenceMethods.get("single", 0) > 0;
    }

    hasDoubleOccurrence() {
        return this.occurrenceMethods.get("double", 0) > 0;
    }

    hasTripleOccurrence() {
        return this.occurrenceMethods.get("triple", 0) > 0;
    }

    isHumanistic() {
        isType(this, "Humanistic");
    }

    isScientific() {
        isType(this, "Scientific");
    }

    isArtistic() {
        isType(this, "Artistic");
    }
    */
}

class Profile {
    constructor(type, long, short) {
        this.type = type;
        this.long = long;
        this.short = short;
    }
    getShort(){
        return this.short;
    }
}

class TechnicalProfile extends Profile {
    constructor(long, short) {
        super('t', long, short);
    }
}

class MultitradeProfile extends Profile {
    constructor(long, short) {
        super('z', long, short);
    }
}

class HighSchoolProfile extends Profile {
    constructor(long, short) {
        super('lo', long, short);
    }
}

const classProfiles = {
    ek: new TechnicalProfile('Technik ekonomista', 'ekonomik'),
    fry: new TechnicalProfile('Technik usług fryzjerskich', 'fryzjer'),
    gas: new TechnicalProfile('Technik żywienia i usług gastronomicznych', 'gastronom'),
    ha: new TechnicalProfile('Technik handlowiec', 'handlowiec'),
    hot: new TechnicalProfile('Technik hotelarstwa', 'hotelarz'),
    log: new TechnicalProfile('Technik logistyk', 'logistyk'),
    ra: new TechnicalProfile('Technik rachunkowości', 'rachunkowość'),
    sport: new HighSchoolProfile('Klasa sportowa', 'sportowa'),
    wz: new MultitradeProfile('Oddział wielozawodowy', 'wielozawodowa')
};

export {Profile, TechnicalProfile, MultitradeProfile, classProfiles};