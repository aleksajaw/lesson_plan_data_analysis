class Profile {
    constructor(type, long, short) {
        this.type = type;
        this.long = long;
        this.short = short;
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

const classProfiles = {
    ek: new TechnicalProfile('Technik ekonomista', 'ekonomik'),
    fry: new TechnicalProfile('Technik usług fryzjerskich', 'fryzjer'),
    gas: new TechnicalProfile('Technik żywienia i usług gastronomicznych', 'gastronom'),
    ha: new TechnicalProfile('Technik handlowiec', 'handlowiec'),
    hot: new TechnicalProfile('Technik hotelarstwa', 'hotelarz'),
    log: new TechnicalProfile('Technik logistyk', 'logistyk'),
    ra: new TechnicalProfile('Technik rachunkowości', 'rachunkowość'),
    wz: new MultitradeProfile('Oddział wielozawodowy', 'klasa wielozawodowa')
};

export {Profile, TechnicalProfile, MultitradeProfile, classProfiles};