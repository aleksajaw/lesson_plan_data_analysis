import puppeteer from 'puppeteer';
import {isObject, writeLessonsToJSONFile} from './utils.js';
import fs from 'fs';
import {Profile, TechnicalProfile, MultitradeProfile, classProfiles} from './classes.js';
import { outputsPath, schoolPlanPage, linksFrameName, planFrameName, weekDays, shouldPrintPlanToConsole, shouldWritePlanToJSON, shouldWritePlanToTxt, keysSpacesAmount} from './constants.js';

(async () => {

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

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

    /*for(const link of links) {
        console.log(link);
    }*/

    // iterate over links in frame1
    for(const link of links) {
        //console.log(link);
            
        // switch to frame2
        const frame2 = await page.waitForSelector(`frame[name="${planFrameName}"]`);
        const frame2Content = await frame2.contentFrame();
        await frame2Content.goto(link.href);

        /*// wait for frame2 content to load
        await frame2Content.waitForSelector('.tabtytul');
        const classSymbol = await frame2Content.evaluate(() => {
                                const symbolTemp = document.querySelector('.tabtytul .tytulnapis').textContent.trim();
                                return { short: symbolTemp.split(' ')[0], fullClassSymbol: symbolTemp };
                            })*/
        const partOfClassProfile = link.text.split(' ')[1];
        const profilesForClass = (partOfClassProfile?.replace(/\d+/g,'') || '')
                                    .split('/')
                                        .map( profile => classProfiles[profile]?.getShort()
                                                        || `${'no "' + profile + '" profile'}` );
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
                        /*lessonSubjectInfoTemp.push({
                            subjectSymbol: spanP?.[i]?.textContent.trim() || '',
                            teacherSymbol: spanN?.[i]?.textContent.trim() || '',
                            classroomNr: spanS?.[i]?.textContent.trim() || ''
                        });*/
                        const subjectSymbol = spanP?.[i]?.textContent.trim() || '';
                        const teacherSymbol = spanN?.[i]?.textContent.trim() || '';
                        const classroomNr = spanS?.[i]?.textContent.trim() || '';

                        lessonSubjectInfoTemp.push({subjectSymbol, teacherSymbol, classroomNr});
                    }

                    /*lessons.push({
                        lessonNr: tdNr?.textContent.trim() || '',
                        lessonHour: tdG?.textContent.trim() || '',
                        lessonSubjectInfo: lessonSubjectInfoTemp || []
                    });*/
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


    // ascending sort classes by class symbol
    // sort by e.g. [ '1A', {class data} ]
    const sortedClassesLessonsData = Object.fromEntries(
        Object.entries(classesLessonsData).sort((a, b) => a[0].localeCompare(b[0]))
    );


    // uses classes
    // classesLessonData: { class name: {} }
    if (isObject(sortedClassesLessonsData)) {
        let fullLessonsStr = '';
        // classes   loop
        for (const [className, classPlanData] of Object.entries(sortedClassesLessonsData)) {

            //const fullSymbol = classesLessonsData[classStr].fullClassSymbol;
            let classTitle = className;
            if(classPlanData.classProfile.length>0)
                classTitle += '(' + (classPlanData.classProfile).join(', ') + ')';
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
        if(shouldWritePlanToTxt.class)
            fs.writeFileSync(`${outputsPath}output.txt`, fullLessonsStr, (err) => {
                if (err) throw err;
            })

        if(shouldWritePlanToJSON.class)
            writeLessonsToJSONFile(sortedClassesLessonsData);

        if(shouldPrintPlanToConsole.class)
            console.log(fullLessonsStr);
    }

    await browser.close();

})();