import puppeteer from 'puppeteer';
import {isObject} from './utils.js';

(async () => {

    const schoolPlanPage = 'https://zamkowa15.edu.pl/plan/plan.html';
    const linksFrameName = 'list';
    const planFrameName = 'plan';
    const weekDays = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek'];
    const shouldPrintLessonPlan = true;
    const keysSpacesAmount = { lessonNr: 3, lessonG: 13, lessonSymbol: 15, teacherSymbol: 5, classroomNumber: 5};

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
        let linksArray = Array.from(linksList).map(link => link.href);
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
        await frame2Content.goto(link);

        // wait for frame2 content to load
        await frame2Content.waitForSelector('.tabtytul');
        let classSymbol = await frame2Content.evaluate(() => {
                                let symbolTemp = document.querySelector('.tabtytul .tytulnapis').textContent.trim();
                                return { short: symbolTemp.split(' ')[0], fullClassSymbol: symbolTemp };
                            })

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


        let classLessonsData = {};        


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
                    
                    lessonDataTemp = [];

                    
                    for(let i=0; i < Math.max(spanP.length, spanN.length, spanS.length); i++) {
                        lessonDataTemp.push({
                            lessonSymbol: !!spanP && spanP[i] ? spanP[i].textContent.trim() : '',
                            teacherSymbol: !!spanN && spanN[i] ? spanN[i].textContent.trim() : '',
                            classroomNumber: !!spanS && spanS[i] ? spanS[i].textContent.trim() : ''
                        });
                    }

                    lessons.push({
                        lessonNr: !!tdNr ? tdNr.textContent.trim() : '',
                        lessonG: !!tdG ? tdG.textContent.trim() : '',
                        lessonData: !!lessonDataTemp ? lessonDataTemp : []
                    });
                });
                
                return lessons;
            
            }, dayNr);
            
            classLessonsData[day] = lessonDataRow;
        }
        
        //console.log('Dane lekcji:', classLessonsData);
        classesLessonsData[classSymbol['short']] = {    fullClassSymbol: classSymbol.fullClassSymbol,
                                                        classLessonsData    };

        // class in classesLessonsData loop
        // give class: {}
        if (isObject(classesLessonsData)) {
            for (const [key, value] of Object.entries(classesLessonsData)) {

                let classStr = key;
                if(shouldPrintLessonPlan) {
                    const fullSymbol = classesLessonsData[classStr].fullClassSymbol;
                    const titleLine = '-'.repeat((55 - fullSymbol.length)/2);
                    console.log(`\n\n${titleLine + fullSymbol + titleLine}`)
                }

                // day in class loop
                // give day: {}
                if (isObject(value['classLessonsData'])) {
                    for (const [key2, value2] of Object.entries(value['classLessonsData'])) {

                        let dayStr = key2;
                        if(shouldPrintLessonPlan)
                            console.log(`\n${dayStr.toUpperCase()}:`);

                        // lesson in day loop
                        // give lesson: {}
                        if (isObject(value2)) {
                            for (const [key3, value3] of Object.entries(value2)) {
                                let fullLessonStr = '';

                                // elements in lesson loop
                                // give desired cells (string or array type)
                                if (isObject(value3)) {
                                    let currSpaceBefore = 0;

                                    for (const [key4, value4] of Object.entries(value3)) {
                                            
                                        // condition for lesson(s): symbol, teacher & classroom
                                        // in one time for class
                                        // #1 (array of objects)
                                        if (Array.isArray(value4)) {
                                            let counter = 0;
                                            for (const lessonProp of value4) {
                                                    
                                                if(isObject(lessonProp)){

                                                    if(counter>0) {
                                                        fullLessonStr += '\n' + ' '.repeat(currSpaceBefore);
                                                    }
                                                    for (const [key5, value5] of Object.entries(lessonProp)) {
                                                        let spacesAmount = keysSpacesAmount[key5] - value5.length;
                                                        let spaces = ' '.repeat(spacesAmount);
                                                        fullLessonStr += spaces + value5 + ' ';
                                                    }
                                                    counter++;
                                                }
                                            }
                                            
                                        // #2 (string type) lesson(s) nr & hour
                                        } else {
                                            let spacesAmount = keysSpacesAmount[key4] - value4.length;
                                            currSpaceBefore += keysSpacesAmount[key4]+1;
                                            let spaces = ' '.repeat(spacesAmount);
                                            fullLessonStr += spaces + value4 + ' ';
                                        }
                                    }
                                    if(shouldPrintLessonPlan)
                                        console.log(fullLessonStr);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    await browser.close();

})();
