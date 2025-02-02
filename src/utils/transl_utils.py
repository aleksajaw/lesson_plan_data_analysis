from src.constants.transl_constants import translations


def findSingular(word='', lang='en'):

    for key, forms in translations.get( lang, {} ).items():
        if forms['plural'] == word:
            
            return forms['singular']

    return f'There is no singular form found for "{word}".'



def findTranslParent(word='', lang='en'):
    for key, forms in translations.get( lang, {} ).items():
        if word in forms.values(): 
            return key
    
    return f'There is no parent found for "{word}"'


def getTranslation(word='', getPlural=False, toLang='pl', fromLang='en'):
    form = 'plural'   if getPlural   else 'singular'
    parentWord = findTranslParent(word, fromLang)

    return translations[toLang][parentWord][form]



def getTranslByPlural(word='', getPlural=False, toLang='pl', fromLang='en'):
    return getTranslation(word, getPlural, toLang, fromLang)