import asyncio
from pyppeteer import launch
import os
from classes import Profile, TechnicalProfile, MultitradeProfile, classProfiles
from constants import outputsPath, schoolPlanPage, linksFrameName, planFrameName, weekdays, shouldPrintPlanToConsole, shouldWritePlanToJSON, shouldWritePlanToTxt, keysSpacesAmount

async def main():
    browser = await launch()
    page = await browser.newPage()

    await page.goto(schoolPlanPage)

    # Wait for frame1 content to load
    frame1 = await page.waitForSelector(f'frame[name="{linksFrameName}"]')
    frame1Content = await frame1.contentFrame()

    classesLessonsData = {}

    # Get links from frame1
    links = await frame1Content.evaluate('''() => {
        const linksList = document.querySelectorAll('body > ul > li > a');
        const linksArray = Array.from(linksList).map(link => ({href: link.href, text: link.textContent.trim()}));
        return linksArray;
    }''')

    # Iterate over links in frame1
    for link in links:
        # Switch to frame2
        frame2 = await page.waitForSelector(f'frame[name="{planFrameName}"]')
        frame2Content = await frame2.contentFrame()
        await frame2Content.goto(link['href'])

        partOfClassProfile = link['text'].split(' ')[1]
        profilesForClass = [classProfiles[profile].getShort() if profile in classProfiles else f'no "{profile}" profile' for profile in partOfClassProfile.replace('\d+', '').split('/')]
        shorterClassSymbol = link['text'].split(' ')[0]
        classSymbol = {
            'year': link['text'][0],
            'letter': shorterClassSymbol.replace('\d+', ''),
            'short': shorterClassSymbol,
            'full': link['text'],
            'profile': profilesForClass
        }

        # Wait for frame2 content to change
        await frame2Content.waitForSelector('.tabela')

        # Get data from frame2
        daysInUse = await frame2Content.evaluate('''(weekdays) => {
            const allHeadingCells = document.querySelectorAll('.tabela tr th');
            const headingsWithCorrectIndexes = {};

            allHeadingCells.forEach((heading, i) => {
                const headingText = heading.textContent.trim();
                const isWeekDay = weekdays.includes(headingText.toLowerCase());
                if (isWeekDay)
                    headingsWithCorrectIndexes[i+1] = headingText;
            });

            return headingsWithCorrectIndexes;
        }''', weekdays)

        classDaysData = {}

        # Create lessonsData by days
        for key, value in daysInUse.items():
            day = daysInUse[key]
            dayNr = key
            lessonDataRow = await frame2Content.evaluate(f'''(dayNr) => {{
                const lessonsInDay = document.querySelectorAll('.tabela tr:not(:first-child) td:nth-child({dayNr})');
                const lessons = [];

                lessonsInDay.forEach(cell => {{
                    const parentTr = cell.parentNode;
                    const tdNr = parentTr.querySelector('td.nr');
                    const tdG = parentTr.querySelector('td.g');
                    const spanP = cell.querySelectorAll('span.p');
                    const spanN = cell.querySelectorAll('span.n');
                    const spanS = cell.querySelectorAll('span.s');

                    let lessonSubjectInfoTemp = [];

                    for (let i=0; i < Math.max(spanP.length, spanN.length, spanS.length); i++) {{
                        const subjectSymbol = spanP?.[i]?.textContent.trim() || '';
                        const teacherSymbol = spanN?.[i]?.textContent.trim() || '';
                        const classroomNr = spanS?.[i]?.textContent.trim() || '';

                        lessonSubjectInfoTemp.push({{subjectSymbol, teacherSymbol, classroomNr}});
                    }}

                    const lessonNr = tdNr?.textContent.trim() || '';
                    const lessonHour = tdG?.textContent.trim() || '';
                    const lessonSubjectInfo = lessonSubjectInfoTemp || [];

                    lessons.push({{lessonNr, lessonHour, lessonSubjectInfo}});
                }});

                return lessons;
            }}''', dayNr)

            classDaysData[day] = lessonDataRow

        classesLessonsData[classSymbol['short']] = {
            'classYear': classSymbol['year'],
            'classLetter': classSymbol['letter'],
            'fullClassSymbol': classSymbol['full'],
            'classProfile': classSymbol['profile'],
            'classDaysData': classDaysData
        }

    # Ascending sort classes by class symbol
    sortedClassesLessonsData = dict(sorted(classesLessonsData.items()))

    await browser.close()

    return sortedClassesLessonsData

asyncio.get_event_loop().run_until_complete(main())