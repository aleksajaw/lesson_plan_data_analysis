import puppeteer from 'puppeteer';

(async () => {

    const weekDays = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek'];
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    await page.goto('https://zamkowa15.edu.pl/plan/plan.html');

    const title = await page.title();
    console.log('Tytuł strony:', title);

    
    // frame1 contains the list of classes
    const frame1 = await page.waitForFrame(async frame => {
                        return frame.name() === 'list';
                    });

    let links = await frame1.evaluate((xxx) => {
        let linksList = document.querySelectorAll('body > ul > li > a');
        let linksArray = [];
        for(let link of linksList) {
            linksArray.push(link.textContent);
        }
        return linksArray;
    })


    //const linkElement = await frame1.click('body > ul > li > a');
    
    // frame2 contains the class lesson plan
    const frame2 = await page.waitForFrame(async frame => {
                        return frame.name() === 'plan';
                    });
        
    // check, which of them are in use
    let days2 = await frame2.evaluate((weekDays) => {
            
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


    // extract lesson data from the class lesson plan by day (column)
    const classLessonsData = {};

    for (const [key, value] of Object.entries(days2)) {

        const day = days2[key];
        const dayNr = key;
        const lessonData = await frame2.evaluate((dayNr) => {

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

    console.log('Dane lekcji:', classLessonsData);

    await browser.close();

})();
