###   INITIAL VARIABLES   ###
schoolAndPlanURLs = [ ('https://zamkowa15.edu.pl', '/plan/plan.html'),
                      ('https://www.mechaniksieradz.edu.pl', '/DANE/Plan/Uczen/biezacy/') ]

schoolURL, partPlanURL = schoolAndPlanURLs[0]
planURL = schoolURL + partPlanURL

# The frame names (for attributes).
linksFrameName = 'list'
planFrameName = 'plan'


from selenium.webdriver.common.by import By

scraperFindKeys = { 'classList': (By.CSS_SELECTOR, 'a[target="plan"]'),
                    'table': (By.CLASS_NAME, 'tabela'),
                    'rows': (By.TAG_NAME, 'tr'),
                    'cols': (By.XPATH, './/td | .//th') }

scraperPresenceLocators = { 'list': (By.NAME, linksFrameName),
                            'plan': (By.NAME, planFrameName) }


# The WebDriver possible locations.
driverLocationStates = ['default', linksFrameName, planFrameName]