
from selenium.webdriver.common.by import By


###   INITIAL VARIABLES   ###
schoolsWebInfo = { 'zamkowa15': {
                        'schoolURL': 'https://zamkowa15.edu.pl',
                        'planURL': {
                            'partial': '/plan/plan.html',
                            'full': 'https://zamkowa15.edu.pl/plan/plan.html'
                        },
                        'useDOMFrames': True,
                        'scheduleLinksInfo': {
                            'selector': (By.CSS_SELECTOR, 'a[target="plan"]'),
                            'selectorParent': (By.NAME, 'list')
                        },
                        'planInfo': {
                            'selector': (By.NAME, 'plan'),
                            'selectorParent': ''
                        }
                    },
                    'mechaniksieradz': {
                        'schoolURL': 'https://www.mechaniksieradz.edu.pl',
                        'planURL': {
                            'partial': '/DANE/Plan/Uczen/biezacy/',
                            'full': 'https://www.mechaniksieradz.edu.pl/DANE/Plan/Uczen/biezacy/'
                        },
                        'useDOMFrames': True,
                        'scheduleLinksInfo': {
                            'selector': (By.CSS_SELECTOR, 'a[target="plan"]'),
                            'selectorParent': (By.NAME, 'list')
                        },
                        'planInfo': {
                            'selector': (By.NAME, 'plan'),
                            'selectorParent': ''
                        }
                    },
                    'zeromski': {
                        'schoolURL': 'https://zeromski.edu.pl',
                        'planURL': {
                            'partial': '/plany/',
                            'full': 'https://zeromski.edu.pl/plany/'
                        },
                        'useDOMFrames': True,
                        'scheduleLinksInfo': {
                            'selector': (By.CSS_SELECTOR, 'a[target="plan"]'),
                            'selectorParent': (By.NAME, 'list')
                        },
                        'planInfo': {
                            'selector': (By.NAME, 'plan'),
                            'selectorParent': ''
                        }
                    },
                    'lojagiellonczyk': {
                        'schoolURL': 'https://lojagiellonczyk.pl',
                        'planURL': {
                            'partial': '/dla-uczniow/plan-lekcji/',
                            'full': 'https://lojagiellonczyk.pl/dla-uczniow/plan-lekcji/'
                        },
                        'useDOMFrames': False,
                        'scheduleLinksInfo': {
                            'selector': (By.XPATH, "//a[contains(@href, '/dla-uczniow/plan-lekcji/')]"),
                            'selectorParent': ''
                        },
                        'planInfo': {
                            'selector':'',
                            'selectorParent': ''
                        }
                    } }

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