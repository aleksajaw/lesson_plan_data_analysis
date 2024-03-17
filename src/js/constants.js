const schoolPlanPage = 'https://zamkowa15.edu.pl/plan/plan.html';
const linksFrameName = 'list';
const planFrameName = 'plan';
const weekDays = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek'];

const shouldPrintPlanToConsole = {
    class: false,
    teacher: true,
    classroom: true
};
const shouldWritePlanToTxt = {
    class: true,
    teacher: true,
    classroom: true
};
const keysSpacesAmount = {
    lessonNr: 3,
    lessonHour: 13,
    subjectSymbol: 15,
    teacherSymbol: 5,
    classroomNr: 5
};

export {schoolPlanPage, linksFrameName, planFrameName, weekDays, shouldPrintPlanToConsole, shouldWritePlanToTxt, keysSpacesAmount};