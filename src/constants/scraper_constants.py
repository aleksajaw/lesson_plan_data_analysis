
from selenium.webdriver.common.by import By


###   INITIAL VARIABLES   ###
schoolsWebInfo = [  {
                       'title'      : 'zamkowa15',
                       'schoolName' : {
                           'short'    : 'PZS nr 2',
                           'standard' : 'PZS nr 2 im. Marii Dąbrowskiej w Sieradzu'
                       },
                       'schoolURL'  : 'https://zamkowa15.edu.pl',
                       'planURL'    : {
                           'partial' : '/plan/plan.html',
                           'full'    : 'https://zamkowa15.edu.pl/plan/plan.html'
                       },
                       'useDOMFrames' : True,
                       'scheduleLinksInfo' : {
                           'selector'       : (By.CSS_SELECTOR, 'a[target="plan"]'),
                           'selectorParent' : (By.NAME, 'list')
                       },
                       'planInfo' : {
                           'selector'       : (By.NAME, 'plan'),
                           'selectorParent' : ''
                       }
                    },
                    {
                       'title'      : 'mechaniksieradz',
                       'schoolName' : {
                           'short'    : 'PZS nr 1',
                           'standard' : 'PZS nr 1 w Sieradzu'
                       },
                       'schoolURL'  : 'https://www.mechaniksieradz.edu.pl',
                       'planURL'    : {
                           'partial' : '/DANE/Plan/Uczen/biezacy/',
                           'full'    : 'https://www.mechaniksieradz.edu.pl/DANE/Plan/Uczen/biezacy/'
                       },
                       'useDOMFrames' : True,
                       'scheduleLinksInfo' : {
                           'selector'       : (By.CSS_SELECTOR, 'a[target="plan"]'),
                           'selectorParent' : (By.NAME, 'list')
                       },
                       'planInfo' : {
                           'selector'       : (By.NAME, 'plan'),
                           'selectorParent' : ''
                       }
                    },
                    {
                       'title'      : 'zeromski',
                       'schoolName' : {
                           'short'    : 'II LO',
                           'standard' : 'II LO im. Stefana Żeromskiego w Sieradzu'
                       },
                       'schoolURL'  : 'https://zeromski.edu.pl',
                       'planURL'    : {
                           'partial' : '/plany/',
                           'full'    : 'https://zeromski.edu.pl/plany/'
                       },
                       'useDOMFrames' : True,
                       'scheduleLinksInfo' : {
                           'selector'       : (By.CSS_SELECTOR, 'a[target="plan"]'),
                           'selectorParent' : (By.NAME, 'list')
                       },
                       'planInfo' : {
                           'selector' : (By.NAME, 'plan'),
                           'selectorParent' : ''
                       }
                    },
                    {
                       'title'      : 'lojagiellonczyk',
                       'schoolName' : {
                           'short'    : 'I LO',
                           'standard' : 'I LO im. Kazimierza Jagiellończyka w Sieradzu'
                       },
                       'schoolURL'  : 'https://lojagiellonczyk.pl',
                       'planURL'    : {
                           'partial' : '/dla-uczniow/plan-lekcji/',
                           'full'    : 'https://lojagiellonczyk.pl/dla-uczniow/plan-lekcji/'
                       },
                       'useDOMFrames' : False,
                       'scheduleLinksInfo' : {
                           'selector'       : (By.XPATH, "//a[contains(@href, '/dla-uczniow/plan-lekcji/')]"),
                           'selectorParent' : ''
                       },
                       'planInfo' : {
                           'selector'       :'',
                           'selectorParent' : ''
                       }
                    }
                 ]

#schoolURL, partPlanURL = schoolAndPlanURLs[0]
#planURL = schoolURL + partPlanURL

# The frame names (for attributes).
scheduleLinksFrameName = 'list'
planFrameName = 'plan'



scraperFindKeys = { 'table' : (By.CLASS_NAME, 'tabela'),
                    'rows'  : (By.TAG_NAME, 'tr'),
                    'cols'  : (By.XPATH, './/td | .//th'),
                    'spans' : (By.XPATH, './/span[ not(*) ]') }

#scraperPresenceLocators = { 'list': (By.NAME, linksFrameName),
#                            'plan': (By.NAME, planFrameName) }


# The WebDriver possible locations.
driverLocationStates = ['default', scheduleLinksFrameName, planFrameName]