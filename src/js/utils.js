import fs from 'fs';
import {outputsPath, baseNameForLessonsJSON} from './constants.js';

function isObject(obj) {
    return typeof obj === 'object' && !!obj;
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

function correctNumNotation(val) {
    return val<10 ? `0${val}` : val;
}

function compareFileChangeTime(a, b, folderPath = `${outputsPath}`) {
    const fileAInfo = fs.statSync(`${folderPath + a}`);
    const fileBInfo = fs.statSync(`${folderPath + b}`)

    return fileBInfo.ctime.getTime() - fileAInfo.ctime.getTime();
}

function findLatestFileWithBaseNameInFolder(fNameBase = baseNameForLessonsJSON, path = outputsPath) {
    const groupInFolder = fs.readdirSync(path);
    let desiredFile = { name: '', content: '' };

    if (groupInFolder.length > 0) {
        const filteredFilesList = groupInFolder.filter( fName => fName.includes(fNameBase) );

        const sortedGroup = !filteredFilesList.length ? []
                                                    : filteredFilesList.sort( (a,b) => compareFileChangeTime(a,b) );

        if (sortedGroup.length == 1 ) {
            desiredFile = { name: sortedGroup[0],
                            content: fs.readFileSync(`${path + sortedGroup[0]}`, 'utf8', (err, data) => {
                                        if (err) throw err;
                                    }) }
        }
    }
    return desiredFile;
}

function doesFileExistInFolder(fileName='', path = outputsPath) {
    return !fileName ? false : fs.existsSync(path + fileName);
}

function writeLessonsToJSONFile(lessonsObj = {}) {
    const lessonsInJSON = JSON.stringify(lessonsObj);
    let fileName = findLatestFileWithBaseNameInFolder().name;
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