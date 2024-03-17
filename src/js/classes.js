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