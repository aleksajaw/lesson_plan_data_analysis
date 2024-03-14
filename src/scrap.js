import puppeteer from 'puppeteer';
import {isObject} from './utils.js';

(async () => {

    const shouldPrintLessonPlan = true;
    const weekDays = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek'];
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto('https://zamkowa15.edu.pl/plan/plan.html');

    // wait for frame1 content to load
    const frame1 = await page.waitForSelector('frame[name="list"]');
    const frame1Content = await frame1.contentFrame();

    let classesLessonsData = {};
    
    // get links from frame1
    const links = await frame1Content.evaluate(() => {
        let linksList = document.querySelectorAll('body > ul > li > a');
        let linksArray = Array.from(linksList).map(link => link.href);
        return linksArray;
    });

    for(let link of links) {
        console.log(link);
    }

    // iterate over links in frame1
    for(let link of links) {
        await frame1Content.goto(link);
        console.log(link);
            
        // switch to frame2
        const frame2 = await page.waitForSelector('frame[name="plan"]');
        const frame2Content = await frame2.contentFrame();

        // wait for frame2 content to load
        await frame2Content.waitForSelector('.tabtytul');
        let classSymbol = await frame2Content.evaluate(() => {
                                return document.querySelector('.tabtytul .tytulnapis').textContent;
                            })

        // wait for frame2 content to change
        await frame2Content.waitForSelector('.tabela');

        // get data from frame2
        const daysInUse = await frame2Content.evaluate((weekDays) => {
            let headingCells = document.querySelectorAll('.tabela tr th');
            let headingsWithIndexes = {};
            headingCells.forEach((heading, i) => {
                let headingIndex = weekDays.indexOf(heading.textContent.toLowerCase());
                if (headingIndex != -1) {
                    headingsWithIndexes[i+1] = heading.textContent;
                }
            })
            return headingsWithIndexes;
        }, weekDays)


        let classLessonsData = {};        


        // create lessonsData by days
        for (const [key, value] of Object.entries(daysInUse)) {

            const day = daysInUse[key];
            const dayNr = key;
            const lessonData = await frame2Content.evaluate((dayNr) => {
                
                const lessonsInDay = document.querySelectorAll(`.tabela tr:not(:first-child) td:nth-child(${dayNr})`);
                const lessons = [];

                lessonsInDay.forEach(cell => {
                    let parentTr = cell.parentNode;
                    let tdNr = parentTr.querySelector('td.nr');
                    let tdG = parentTr.querySelector('td.g');
                    let spanP = cell.querySelector('span.p');
                    let spanN = cell.querySelector('span.n');
                    let spanS = cell.querySelector('span.s');
                    
                    lessons.push({
                        lessonNr: tdNr ? tdNr.textContent : '',
                        lessonG: tdG ? tdG.textContent : '',
                        lessonSymbol: spanP ? spanP.textContent : '',
                        teacherSymbol: spanN ? spanN.textContent : '',
                        classroomNumber: spanS ? spanS.textContent : ''
                    });
                });
                
                return lessons;
            
            }, dayNr);
            
            classLessonsData[day] = lessonData;
        }
        
        //console.log('Dane lekcji:', classLessonsData);
        classesLessonsData[classSymbol] = classLessonsData;

        // class loop
        if (isObject(classesLessonsData)) {
            for (const [key, value] of Object.entries(classesLessonsData)) {

                let classStr = key;
                if(shouldPrintLessonPlan) console.log(`\n\n--------------------${classStr}--------------------`)

                //day loop
                if (isObject(value)) {
                    for (const [key2, value2] of Object.entries(value)) {
                        let dayStr = key2;
                        if(shouldPrintLessonPlan) console.log(`\n${dayStr.toUpperCase()}:`);

                        //lesson loop
                        if (isObject(value2)) {
                            for (const [key3, value3] of Object.entries(value2)) {
                                let fullLessonStr = '';

                                //lesson elements loop
                                if (isObject(value3)) {
                                    let keysWhiteSpacesAmount = { lessonNr: 3, lessonG: 13, lessonSymbol: 13, teacherSymbol: 5, classroomNumber: 5};
                                    for (const [key4, value4] of Object.entries(value3)) {
                                        let whiteSpacesAmount = keysWhiteSpacesAmount[key4] - value4.length;
                                        let whiteSpaces = ' '.repeat(whiteSpacesAmount);
                                        fullLessonStr += ' ' + value4 + whiteSpaces + ' ';
                                    }
                                    if(shouldPrintLessonPlan) console.log(fullLessonStr);
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
