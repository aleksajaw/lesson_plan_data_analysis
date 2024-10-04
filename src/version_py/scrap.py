from constants import *
from utils import *


baseUrl = getWithoutLastPart(planStartUrl)

listFrameLinks = findInFrame('a', {'target': 'plan'}, 'list', planStartUrl, True) or []

data = []

for link in listFrameLinks:

    print(convertToFrameUrl(baseUrl, link.get('href')))
    
    table = findInFrame('table', {'class': 'tabela'}, 'plan', planStartUrl)

    for row in table.find_all('tr'):
        rowData = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if rowData:
            data.append(rowData)