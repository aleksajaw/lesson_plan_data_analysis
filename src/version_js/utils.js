import fs from 'fs';
import {outputsPath, baseNameForLessonsJSON, baseNameForSimpleFormattedLessonsTxt, baseNameForFormattedLessonsTxt, baseNameForLessonsCSV, keysSpacesAmount} from './constants.js';

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

    return fileBInfo.birthtime.getTime() - fileAInfo.birthtime.getTime();
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

function createFolderIfDoesntExist(folderName='', path=outputsPath) {
    try {
        if (!fs.existsSync(path+folderName)) {
          fs.mkdirSync(path+folderName);
        }
      } catch (err) {
        console.error(err);
      }
}

function sortLessonsData(lessonsObj={}) {
    // ascending sort classes by class symbol
    // sort by e.g. [ '1A', {class data} ]
    return Object.fromEntries(
        Object.entries(lessonsObj).sort((a, b) => a[0].localeCompare(b[0]))
    );
}

function convertLessonsObjToFormattedStr(lessonsObj={}) {
    let fullLessonsStr = '';
    // uses classes
    // classesLessonData: { class name: {} }
    if (isObject(lessonsObj)) {
        // classes   loop
        for (const [className, classPlanData] of Object.entries(lessonsObj)) {

            let classTitle = className;
            if(!!classPlanData.classProfile) {
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
                                                        const placeAmount = keysSpacesAmount[lessonPropElName];
                                                        fullLessonsStr += lessonPropElVal.padStart(placeAmount) + ' ';
                                                    }
                                                    counter++;
                                                }
                                            }
                                        
                                        // lesson nr and hour for lesson row
                                        // #2   day name: [{ lessonNr: '', lessonHour: '' }]
                                        } else if (typeof lessonProp === 'string') {
                                            const placeAmount = keysSpacesAmount[lessonPropName];
                                            fullLessonsStr += lessonProp.padStart(placeAmount) + ' ';
                                            currSpaceBefore += placeAmount+1;
                                        }
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

function convertLessonsTableObjToFormattedStr(lessonsObj={}) {
    let fullLessonsStr = '';
    if(isObject(lessonsObj)) {
        for (let planOwner in lessonsObj) {
            
            let lessonsData = lessonsObj[planOwner];
            fullLessonsStr += "\n\n--------------------" + planOwner + "--------------------\n";

            for (let i = 2; i < lessonsData[0].length; i++) {
                fullLessonsStr += '\n' + lessonsData[0][i].toUpperCase() + '\n';

                for (let j = 1; j < lessonsData.length; j++) {
                    const lesson = lessonsData[j];
                    const lessonNr = lesson[0].padStart(keysSpacesAmount['lessonNr']);
                    const lessonHour= lesson[1].padStart(keysSpacesAmount['lessonHour']);
                    const subjects = lesson[i];
                    const basicRowText = lessonNr + ' ' + lessonHour + ' ';
                    fullLessonsStr += basicRowText;

                    if (!!subjects) {
                        const lessonsInOneCell = subjects.split('  |  ');
                        const formattedLessonsInOneCell = lessonsInOneCell.map(subjectInfo => {
                                                    const elements = subjectInfo.split(' ');
                                                    const subject = elements[0].padStart(keysSpacesAmount['subjectSymbol']);
                                                    const teacher = elements[1].padStart(keysSpacesAmount['teacherSymbol']);
                                                    const classroom = elements[2].padStart(keysSpacesAmount['classroomNr']);
                                                    return subject + ' ' + teacher + ' ' + classroom + ' ';
                                                });
                        fullLessonsStr += formattedLessonsInOneCell.join('\n' + ' '.repeat(basicRowText.length));
                    }
                    fullLessonsStr += '\n';
                }
            }
        }
    }
    return fullLessonsStr;
}

function convertLessonsToCSV(lessonsData) {
    let csvStr = "";

    for (const sheetName in lessonsData) {
        csvStr += `,,,"${sheetName}",,,\n`;

        const sheetData = lessonsData[sheetName];

        for (const row of sheetData) {
            csvStr += row.map(cell => `"${cell}"`).join(",") + "\n";
        }
        csvStr += "\n";
    }
    return csvStr;
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

function writeLessonsToJSON(lessonsData={}, formattedDate='', sorted=false) {
    const sortedLessonsData = sorted ? lessonsData
                                     : sortLessonsData(lessonsData);
    let fileName = baseNameForLessonsJSON;
    if(!lessonsData[Object.keys(lessonsData)[0]].classDaysData) {
        fileName = fileName.split('.');
        fileName[0] = fileName[0]+'2';
        fileName = fileName.join('.');
    }
    return writeLessonsToFile(sortedLessonsData, fileName, '', formattedDate, 'json')
}

function writeLessonsObjToFormattedTxt(lessonsData=null, formattedDate='', sorted=false) {
    let fullLessonsStr = lessonsData || '';
    if(isObject(lessonsData)) {
        const sortedLessonsData = sorted ? lessonsData
                                         : sortLessonsData(lessonsData);
        fullLessonsStr = convertLessonsObjToFormattedStr(sortedLessonsData);
    }
    return writeLessonsToFile(fullLessonsStr, baseNameForFormattedLessonsTxt, '', formattedDate, 'txt');
}

function writeLessonsTableObjToFormattedTxt(lessonsData=null, formattedDate='', sorted=false) {
    let fullLessonsStr = lessonsData || '';
    if(isObject(lessonsData)) {
        const sortedLessonsData = sorted ? lessonsData
                                         : sortLessonsData(lessonsData);
        fullLessonsStr = convertLessonsTableObjToFormattedStr(sortedLessonsData);
    }
    return writeLessonsToFile(fullLessonsStr, baseNameForSimpleFormattedLessonsTxt, '', formattedDate, 'txt');
}

function writeLessonsToCSV(lessonsData=null, formattedDate='', sorted=false) {
    let fullLessonsStr = lessonsData || '';
    if(isObject(lessonsData)) {
        const sortedLessonsData = sorted ? lessonsData
                                         : sortLessonsData(lessonsData);
        fullLessonsStr = convertLessonsToCSV(sortedLessonsData);
    }
    return writeLessonsToFile(fullLessonsStr, baseNameForLessonsCSV, '', formattedDate, 'csv');
}

export {firstLetterToLowerCase, firstLetterToUpperCase, isObject, isType, getNowFormattedDate, findLatestFileWithBaseNameInFolder, doesFileExistInFolder, createFolderIfDoesntExist, sortLessonsData, convertLessonsObjToFormattedStr, convertLessonsTableObjToFormattedStr, convertLessonsToCSV, writeLessonsToJSON, writeLessonsObjToFormattedTxt, writeLessonsTableObjToFormattedTxt, writeLessonsToCSV};