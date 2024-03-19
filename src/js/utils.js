import fs from 'fs';
import {outputsPath, baseNameForLessonsJSON} from './constants.js';

function isObject(obj) {
    return typeof obj === 'object' && !!obj;
}

function getNowFormattedDate() {
    let today = new Date();
    let YYYY = today.getFullYear();
    let MM = correctNumNotation(today.getMonth()+1);
    let DD = correctNumNotation(today.getDate());
    let HH = correctNumNotation(today.getHours());
    let mm = correctNumNotation(today.getMinutes());
    let ss = correctNumNotation(today.getSeconds());

    return `${YYYY + MM + DD + '_' + HH + mm + ss}`;
}

function correctNumNotation(val) {
    return val<10 ? `0${val}` : val;
}

function compareFileChangeTime(a, b, folderPath = `${outputsPath}`) {
    const fileAInfo = fs.statSync(`${folderPath + a}`);
    const fileBInfo = fs.statSync(`${folderPath + b}`)

    return fileBInfo.ctime.getTime() - fileAInfo.ctime.getTime();
}

function findLatestFileWithBaseNameInFolder(fNameBase = baseNameForLessonsJSON, path = outputsPath) {
    let group = fs.readdirSync(path);
    let sortedGroup = group;
    if (group.length > 1) {
        let filteredFilesList = group.filter(   fName => fName.includes(fNameBase)  );
        sortedGroup = !filteredFilesList.length ? []
                                                : filteredFilesList.sort(  (a,b) => compareFileChangeTime(a,b) ); 
    }
    return sortedGroup[0] || '';
}

function doesFileExistInFolder(fileName='', path = outputsPath) {
    return !fileName ? false : fs.existsSync(path + fileName);
}

function writeLessonsToJSONFile(lessonsObj = {}) {
    const lessonsInJSON = JSON.stringify(lessonsObj);
    let fileName = findLatestFileWithBaseNameInFolder();
    const doesFileExist = !!fileName;
    let doAChange = !doesFileExist;

    if(doesFileExist) {
        const lastFileData = fs.readFileSync(`${outputsPath + fileName}`, 'utf8', (err, data) => {
                                if (err) throw err;
                            });
        doAChange = lessonsInJSON !== lastFileData;
    }
    if (doAChange)
        fileName = getNowFormattedDate() + '_' + baseNameForLessonsJSON;
    else {
        console.log('Nothing to update.');
    }
    if(!doesFileExist || doAChange) {
        fs.writeFileSync(`${outputsPath + fileName}`, lessonsInJSON, (err) => {
            if (err) throw err;
            else {
                console.log('File saved.');
            }
        });
    }
}

export {isObject, findLatestFileWithBaseNameInFolder, doesFileExistInFolder, writeLessonsToJSONFile};