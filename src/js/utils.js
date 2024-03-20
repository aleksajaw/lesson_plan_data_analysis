import fs from 'fs';
import {outputsPath, baseNameForLessonsJSON,baseNameForFormattedLessonsTxt, keysSpacesAmount} from './constants.js';

function firstLetterToCase(str, caseType = 'Upper') {
    if (!!str && !!caseType) {
        const strToEval = 'str.charAt(0).to' + caseType + 'Case()';
        str = eval(strToEval) + str.slice(1);
    }
    return str;
}

function firstLetterToLowerCase(str) {
    return firstLetterToCase(str, 'Lower');
}

function firstLetterToUpperCase(str) {
    return firstLetterToCase(str, 'Upper');
}

function isObject(obj) {
    return typeof obj === 'object' && !!obj;
}

function isType(obj, value, name='') {
    let typeName = 'type';
    if (!name)
        name = obj.constructor.name || '';
    if (!!name) {
        name = firstLetterToLowerCase(name);
        typeName = name + 'Type';
    }
    return obj[typeName] == value
}

function correctNumNotation(val) {
    return val<10 ? `0${val}` : val;
}

function getNowFormattedDate() {
    const today = new Date();
    const YYYY = today.getFullYear();
    const MM = correctNumNotation(today.getMonth()+1);
    const DD = correctNumNotation(today.getDate());
    const HH = correctNumNotation(today.getHours());
    const mm = correctNumNotation(today.getMinutes());
    const ss = correctNumNotation(today.getSeconds());

    return `${YYYY + MM + DD + '_' + HH + mm + ss}`;
}

function compareFileChangeTime(a, b, folderPath=outputsPath) {
    const fileAInfo = fs.statSync(`${folderPath + a}`);
    const fileBInfo = fs.statSync(`${folderPath + b}`)

    return fileBInfo.ctime.getTime() - fileAInfo.ctime.getTime();
}

function findLatestFileWithBaseNameInFolder(fNameBase='', path='') {
    path = path || outputsPath;
    const groupInFolder = fs.readdirSync(path);
    let desiredFile = { name: '', content: '' };

    if (!!fNameBase && groupInFolder.length > 0) {
        const filteredFilesList = groupInFolder.filter( fName => fName.includes(fNameBase) );

        const sortedGroup = filteredFilesList?.sort( (a,b) => compareFileChangeTime(a,b) ) || [];

        if (sortedGroup.length > 0 ) {
            desiredFile = { name: sortedGroup[0],
                            content: fs.readFileSync(`${path + sortedGroup[0]}`, 'utf8', (err, data) => {
                                        if (err) throw err;
                                    }) }
        }
    }
    return desiredFile;
}

function doesFileExistInFolder(fileName='', path=outputsPath) {
    return !fileName ? false : fs.existsSync(path + fileName);
}

function sortLessonsData(lessonsObj={}) {
    // ascending sort classes by class symbol
    // sort by e.g. [ '1A', {class data} ]
    return Object.fromEntries(
        Object.entries(lessonsObj).sort((a, b) => a[0].localeCompare(b[0]))
    );
}

function convertLessonsToStr(lessonsObj={}) {
    let fullLessonsStr = '';
    // uses classes
    // classesLessonData: { class name: {} }
    if (isObject(lessonsObj)) {
        // classes   loop
        for (const [className, classPlanData] of Object.entries(lessonsObj)) {

            let classTitle = className;
            if(classPlanData.classProfile.length>0)
                classTitle += ' (' + (classPlanData.classProfile).join(', ') + ')';
            const maxTitleLength = Math.max(55, (classTitle.length + 2));
            const titleLine = '-'.repeat((maxTitleLength - classTitle.length)/2);
            fullLessonsStr += `\n\n\n${titleLine + classTitle + titleLine}`;

            const classDays = classPlanData.classDaysData;
            // uses class days
            // class name: { classDaysData: {} }
            // classDaysData: { day name: [] }
            if (isObject(classDays)) {
                // days in the class   loop
                for (const [classDay, classDayLessons] of Object.entries(classDays)) {

                    fullLessonsStr += `\n\n${classDay.toUpperCase()}:`;
                    
                    // uses day lessons
                    // day name: [ {} ]
                    if (Array.isArray(classDayLessons)) {
                        // lessons in day   loop
                        for (const lessonDataVal of classDayLessons) {
                            fullLessonsStr += '\n';

                            // uses lesson data
                            // lesson row of the class day as {}
                            if (isObject(lessonDataVal)) {
                                let currSpaceBefore = 0;
                                // lesson(s) in one row for the class   loop
                                for (const [lessonPropName, lessonProp] of Object.entries(lessonDataVal)) {
                                    
                                    // condition for lesson's object containing subject, teacher & classroom
                                    // in one time (cell) for the class
                                    // #1   day name: [{ lessonSubjectInfo: [{}] }]
                                    if (Array.isArray(lessonProp)) {
                                        let counter = 0;
                                        // subjects info in one cell   loop
                                        for (const lessonPropEl of lessonProp) {

                                            if(isObject(lessonPropEl)){
                                                if(counter>0) {
                                                    fullLessonsStr += '\n' + ' '.repeat(currSpaceBefore);
                                                }
                                                for (const [lessonPropElName, lessonPropElVal] of Object.entries(lessonPropEl)) {
                                                    const spacesAmount = keysSpacesAmount[lessonPropElName] - lessonPropElVal.length;
                                                    const spaces = ' '.repeat(spacesAmount);
                                                    fullLessonsStr += spaces + lessonPropElVal + ' ';
                                                }
                                                counter++;
                                            }
                                        }
                                    
                                    // lesson nr and hour for lesson row
                                    // #2   day name: [{ lessonNr: '', lessonHour: '' }]
                                    } else if (typeof lessonProp === 'string') {
                                        const spacesAmount = keysSpacesAmount[lessonPropName] - lessonProp.length;
                                        currSpaceBefore += keysSpacesAmount[lessonPropName]+1;
                                        const spaces = ' '.repeat(spacesAmount);
                                        fullLessonsStr += spaces + lessonProp + ' ';
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return fullLessonsStr;
}

function writeLessonsToFile(lessonsData=null, fileBaseName='', path='', formattedDate='', fileType='') {
    fileBaseName = fileBaseName || baseNameForLessonsJSON;
    path = path || outputsPath;
    const currLessonsData = fileType=='json' ? (JSON.stringify(lessonsData) || {})
                                             : (lessonsData || '');
    let fileName = findLatestFileWithBaseNameInFolder(fileBaseName, path).name;
    const doesFileExist = !!fileName;
    let doAChange = !doesFileExist;

    if(doesFileExist) {
        const lastFileData = fs.readFileSync(`${path + fileName}`, 'utf8', (err, data) => {
                                if (err) throw err;
                            });
        doAChange = currLessonsData !== lastFileData;
    }
    if (doAChange)
        fileName = (formattedDate || getNowFormattedDate()) + '_' + fileBaseName;
    else {
        console.log('Nothing to update in' + (!fileType ? '' : ' ' + fileType) + ' file.');
    }
    if(!doesFileExist || doAChange) {
        fs.writeFile(`${path + fileName}`, currLessonsData, (err) => {
            if (err) throw err;
            else {
                console.log('File' + (!fileType ? '' : ' .' + fileType) + ' saved.');
            }
        });
    }
}

function writeLessonsToJSONFile(lessonsData={}, formattedDate='', sorted=false) {
    const sortedLessonsData = sorted ? lessonsData
                                     : sortLessonsData(lessonsData);
    return writeLessonsToFile(sortedLessonsData, baseNameForLessonsJSON, '', formattedDate, 'json')
}

function writeFormattedLessonsToTxtFile(lessonsData=null, formattedDate='', sorted=false) {
    let fullLessonsStr = lessonsData || '';
    if(isObject(lessonsData)) {
        const sortedLessonsData = sorted ? lessonsData
                                         : sortLessonsData(lessonsData);
        fullLessonsStr = convertLessonsToStr(sortedLessonsData);
    }
    return writeLessonsToFile(fullLessonsStr, baseNameForFormattedLessonsTxt, '', formattedDate, 'txt');
}

export {firstLetterToLowerCase, firstLetterToUpperCase, isObject, isType, getNowFormattedDate,findLatestFileWithBaseNameInFolder, doesFileExistInFolder, sortLessonsData, convertLessonsToStr, writeLessonsToJSONFile, writeFormattedLessonsToTxtFile};