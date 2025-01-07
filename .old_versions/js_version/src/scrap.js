import puppeteer from 'puppeteer';
import {isObject, getNowFormattedDate, createFolderIfDoesntExist, sortLessonsData, convertLessonsObjToFormattedStr, writeLessonsToJSON, writeLessonsObjToFormattedTxt} from './utils.js';
import fs from 'fs';
import {Profile, TechnicalProfile, MultitradeProfile, classProfiles} from './classes.js';
import { outputsPath, schoolPlanPage, linksFrameName, planFrameName, weekDays, shouldPrintPlanToConsole, shouldWritePlanToJSON, shouldWritePlanToTxt, keysSpacesAmount} from './constants.js';

(async () => {

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    //await page.setViewport({ width: 1080, height: 720 });
    await page.goto(schoolPlanPage);

    // wait for frame1 content to load
    const frame1 = await page.waitForSelector(`frame[name="${linksFrameName}"]`);
    const frame1Content = await frame1.contentFrame();

    let classesLessonsData = {};

    // get links from frame1
    const links = await frame1Content.evaluate(() => {
        const linksList = document.querySelectorAll('body > ul > li > a');
        const linksArray = Array.from(linksList).map(link => ({href: link.href, text: link.textContent.trim()}));
        return linksArray;
    });


    // iterate over links in frame1
    for(const link of links) {
            
        // switch to frame2
        const frame2 = await page.waitForSelector(`frame[name="${planFrameName}"]`);
        const frame2Content = await frame2.contentFrame();
        await frame2Content.goto(link.href);

        const partOfClassProfile = link.text.split(' ')[1];
        const profilesForClass = (partOfClassProfile?.replace(/\d+/g,'') || '')
                                    .split('/')
                                        .map( profile => classProfiles[profile]?.getShort()
                                                        || (!profile ? 'no profile' : `no ${profile} profile`) );
        // ignore specific classes without profiles
        // that cannot be precisely identified
        // and properly used for future analysis
        if(profilesForClass[0] === 'no profile')
            continue;
 
        const shorterClassSymbol = link.text.split(' ')[0];
        const classSymbol = {
                                year: link.text[0],
                                letter: shorterClassSymbol.replace(/\d+/g,''),
                                short: shorterClassSymbol,
                                full: link.text,
                                profile: profilesForClass
                            };

        // wait for frame2 content to change
        await frame2Content.waitForSelector('.tabela');
        // create outputs folder if doesn't exist
        createFolderIfDoesntExist('');
        //createFolderIfDoesntExist('lessons_screenshots');
        //await frame2.screenshot({'path': outputsPath + 'lessons_screenshots/' + classSymbol.short + 'screenshot.png'});

        // get data from frame2
        const daysInUse = await frame2Content.evaluate((weekDays) => {

            const allHeadingCells = document.querySelectorAll('.tabela tr th');
            const headingsWithCorrectIndexes = {};

            allHeadingCells.forEach((heading, i) => {
                const headingText = heading.textContent.trim();
                const isWeekDay = weekDays.includes(headingText.toLowerCase());
                if (isWeekDay)
                    headingsWithCorrectIndexes[i+1] = headingText;
            })

            return headingsWithCorrectIndexes;
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
                    const parentTr = cell.parentNode;
                    const tdNr = parentTr.querySelector('td.nr');
                    const tdG = parentTr.querySelector('td.g');
                    const spanP = cell.querySelectorAll('span.p');
                    const spanN = cell.querySelectorAll('span.n');
                    const spanS = cell.querySelectorAll('span.s');
                    
                    let lessonSubjectInfoTemp = [];
                    
                    for(let i=0; i < Math.max(spanP.length, spanN.length, spanS.length); i++) {
                        const subjectSymbol = spanP?.[i]?.textContent.trim() || '';
                        const teacherSymbol = spanN?.[i]?.textContent.trim() || '';
                        const classroomNr = spanS?.[i]?.textContent.trim() || '';

                        lessonSubjectInfoTemp.push({subjectSymbol, teacherSymbol, classroomNr});
                    }

                    const lessonNr = tdNr?.textContent.trim() || '';
                    const lessonHour = tdG?.textContent.trim() || '';
                    const lessonSubjectInfo = lessonSubjectInfoTemp || [];
                    
                    lessons.push({lessonNr, lessonHour,lessonSubjectInfo});
                });
                
                return lessons;
            
            }, dayNr);
            
            classDaysData[day] = lessonDataRow;
        }
        
        classesLessonsData[classSymbol.short] = {   classYear: classSymbol.year,
                                                    classLetter: classSymbol.letter,
                                                    fullClassSymbol: classSymbol.full,
                                                    classProfile: classSymbol.profile,
                                                    classDaysData   };
    }


    const currFormattedDate = getNowFormattedDate();
    const sortedClassesLessonsData = sortLessonsData(classesLessonsData);
    const fullLessonsStr = convertLessonsObjToFormattedStr(sortedClassesLessonsData);

    if(shouldWritePlanToTxt.class)
        writeLessonsObjToFormattedTxt(fullLessonsStr, currFormattedDate, true)

    if(shouldWritePlanToJSON.class)
        writeLessonsToJSON(sortedClassesLessonsData, currFormattedDate, true);

    if(shouldPrintPlanToConsole.class)
        console.log(fullLessonsStr);

    await browser.close();

})();