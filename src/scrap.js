import puppeteer from 'puppeteer';
import {isObject} from './utils.js';
import fs from 'fs';


(async () => {

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
    const keysSpacesAmount = { lessonNr: 3, lessonHour: 13, subjectSymbol: 15, teacherSymbol: 5, classroomNumber: 5};

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto(schoolPlanPage);

    // wait for frame1 content to load
    const frame1 = await page.waitForSelector(`frame[name="${linksFrameName}"]`);
    const frame1Content = await frame1.contentFrame();

    let classesLessonsData = {};

    // get links from frame1
    const links = await frame1Content.evaluate(() => {
        let linksList = document.querySelectorAll('body > ul > li > a');
        let linksArray = Array.from(linksList).map(link => ({href: link.href, text: link.textContent.trim()}));
        return linksArray;
    });

    /*for(let link of links) {
        console.log(link);
    }*/

    // iterate over links in frame1
    for(let link of links) {
        //console.log(link);
            
        // switch to frame2
        const frame2 = await page.waitForSelector(`frame[name="${planFrameName}"]`);
        const frame2Content = await frame2.contentFrame();
        await frame2Content.goto(link.href);

        /*// wait for frame2 content to load
        await frame2Content.waitForSelector('.tabtytul');
        let classSymbol = await frame2Content.evaluate(() => {
                                let symbolTemp = document.querySelector('.tabtytul .tytulnapis').textContent.trim();
                                return { short: symbolTemp.split(' ')[0], fullClassSymbol: symbolTemp };
                            })*/
        let classSymbol = {
            year: link.text[0],
            letter: link.text.slice(1),
            short: link.text.split(' ')[0],
            full: link.text
        };

        // wait for frame2 content to change
        await frame2Content.waitForSelector('.tabela');

        // get data from frame2
        const daysInUse = await frame2Content.evaluate((weekDays) => {
            let headingCells = document.querySelectorAll('.tabela tr th');
            let headingsWithIndexes = {};
            headingCells.forEach((heading, i) => {
                let headingIndex = weekDays.indexOf(heading.textContent.trim().toLowerCase());
                if (headingIndex != -1) {
                    // i is the nr of the col in a row of using headingCells
                    headingsWithIndexes[i+1] = heading.textContent.trim();
                }
            })
            return headingsWithIndexes;
        }, weekDays)


        let classDaysData = {};        


        // create lessonsData by days
        for (const [key, value] of Object.entries(daysInUse)) {

            const day = daysInUse[key];
            const dayNr = key;
            const lessonDataRow = await frame2Content.evaluate((dayNr) => {
                
                const lessonsInDay = document.querySelectorAll(`.tabela tr:not(:first-child) td:nth-child(${dayNr})`);
                const lessons = [];

                lessonsInDay.forEach(cell => {
                    let parentTr = cell.parentNode;
                    let tdNr = parentTr.querySelector('td.nr');
                    let tdG = parentTr.querySelector('td.g');
                    let spanP = cell.querySelectorAll('span.p');
                    let spanN = cell.querySelectorAll('span.n');
                    let spanS = cell.querySelectorAll('span.s');
                    
                    lessonSubjectInfoTemp = [];

                    
                    for(let i=0; i < Math.max(spanP.length, spanN.length, spanS.length); i++) {
                        lessonSubjectInfoTemp.push({
                            subjectSymbol: !!spanP && spanP[i] ? spanP[i].textContent.trim() : '',
                            teacherSymbol: !!spanN && spanN[i] ? spanN[i].textContent.trim() : '',
                            classroomNumber: !!spanS && spanS[i] ? spanS[i].textContent.trim() : ''
                        });
                    }

                    lessons.push({
                        lessonNr: !!tdNr ? tdNr.textContent.trim() : '',
                        lessonHour: !!tdG ? tdG.textContent.trim() : '',
                        lessonSubjectInfo: !!lessonSubjectInfoTemp ? lessonSubjectInfoTemp : []
                    });
                });
                
                return lessons;
            
            }, dayNr);
            
            classDaysData[day] = lessonDataRow;
        }
        
        classesLessonsData[classSymbol.short] = {   classYear: classSymbol.year,
                                                    classLetter: classSymbol.letter,
                                                    fullClassSymbol: classSymbol.full,
                                                    classDaysData   };
    }

    // uses classes
    // classesLessonData: { class name: {} }
    if (isObject(classesLessonsData)) {
        let fullLessonsStr = '';
        // classes   loop
        for (const [className, classPlanData] of Object.entries(classesLessonsData)) {

            //const fullSymbol = classesLessonsData[classStr].fullClassSymbol;
            const titleLine = '-'.repeat((55 - className.length)/2);
            fullLessonsStr += `\n\n\n${titleLine + className + titleLine}`;

            let classDays = classPlanData.classDaysData;
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
                                                    let spacesAmount = keysSpacesAmount[lessonPropElName] - lessonPropElVal.length;
                                                    let spaces = ' '.repeat(spacesAmount);
                                                    fullLessonsStr += spaces + lessonPropElVal + ' ';
                                                }
                                                counter++;
                                            }
                                        }
                                       
                                    // lesson nr and hour for lesson row
                                    // #2   day name: [{ lessonNr: '', lessonHour: '' }]
                                    } else if (typeof lessonProp === 'string') {
                                        let spacesAmount = keysSpacesAmount[lessonPropName] - lessonProp.length;
                                        currSpaceBefore += keysSpacesAmount[lessonPropName]+1;
                                        let spaces = ' '.repeat(spacesAmount);
                                        fullLessonsStr += spaces + lessonProp + ' ';
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        if(shouldWritePlanToTxt.class) {
            fs.writeFile('output.txt', fullLessonsStr, (err) => {
                if (err) throw err;
            })
        }
        if(shouldPrintPlanToConsole.class) console.log(fullLessonsStr);
    }

    await browser.close();

})();
