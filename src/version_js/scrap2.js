import puppeteer from 'puppeteer';
import {sortLessonsData, convertLessonsTableObjToFormattedStr, writeLessonsToJSON, writeLessonsTableObjToFormattedTxt, writeLessonsToCSV} from './utils.js';
import {classProfiles} from './classes.js';
import { schoolPlanPage, linksFrameName, planFrameName, shouldPrintPlanToConsole, shouldWritePlanToJSON, shouldWritePlanToCSV, shouldWritePlanToTxt} from './constants.js';

(async () => {

    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    //await page.setViewport({ width: 1080, height: 720 });
    await page.goto(schoolPlanPage);

    // wait for frame1 content to load
    const frame1 = await page.waitForSelector(`frame[name="${linksFrameName}"]`);
    const frame1Content = await frame1.contentFrame();

    // get links from frame1
    const links = await frame1Content.evaluate(() => {
        const linksList = document.querySelectorAll('body > ul > li > a');
        const linksArray = Array.from(linksList).map(link => ({href: link.href, text: link.textContent.trim()}));
        return linksArray;
    });

    let allOfResults = [];

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

        const result = await frame2Content.evaluate(() => {
                            const rows = document.querySelectorAll('.tabela tr');
                            return Array.from(rows, row => {
                                        let cols = row.querySelectorAll('td');
                                        if(!cols.length)
                                            cols = row.querySelectorAll('th');

                                        return Array.from(cols, (col) => {
                                            let colValue = '';
                                            const spans = col.querySelectorAll('span');
                                            const maxElLength = spans.length;

                                            // fixing used content of table cells; irregular amount of spans
                                            // it could be 0 (text outside any spans)
                                            if(!maxElLength) {
                                                colValue += col.textContent.trim();

                                            // or 4 (1 parent, 3 children)
                                            } else if(maxElLength%4===0) {
                                                for(let i=1; i<=maxElLength; i=i+4) {
                                                    if(i!=1)colValue += '  |  ';
                                                    colValue += spans[i-1].textContent;
                                                }

                                            // or 3 (0 parent, 3 children)
                                            } else if (maxElLength%3===0) {
                                                colValue = col.textContent
                                            }
                                            return colValue;
                                        });
                                    });
                        });

        allOfResults[classSymbol.full] = result;
    }
    allOfResults = sortLessonsData(allOfResults);
    if(shouldWritePlanToJSON.class)
        writeLessonsToJSON(allOfResults);
    if(shouldWritePlanToCSV.class)
        writeLessonsToCSV(allOfResults);
    if(shouldWritePlanToTxt.class)
        writeLessonsTableObjToFormattedTxt(allOfResults);
    if(shouldPrintPlanToConsole.class)
        console.log(convertLessonsTableObjToFormattedStr(allOfResults));
    await browser.close();

})();