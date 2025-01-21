from bs4 import BeautifulSoup
from src.constants import planURL
from requests_utils import getResponse, getWithoutLastPart


def getSoup(url=planURL):
    response = getResponse(url)
    return BeautifulSoup(response.content, 'html.parser') if response else None


def convertToFrameURL(url='', frameSrc=''):
    frameURL = getWithoutLastPart(url) + '/' + frameSrc
    return frameURL


def getFrameSoup(url, urlSoup, frameName=''):
    foundFrame = urlSoup.find('frame', {'name': frameName})
    frameSrc = foundFrame['src'] if foundFrame else None
    return getSoup(convertToFrameURL(url, frameSrc))


def findInFrame(elTag='', elAttr={}, frameName='', url='', findAll=False):
    url = url or planURL
    urlSoup = getSoup(url)
    if urlSoup:
        frameSoup = getFrameSoup(url, urlSoup, frameName)
        return findInSource(elTag, elAttr, '', findAll, frameSoup)
        
    return None


def findInSource(elTag='', elAttr={}, url='', findAll=True, urlSoup=None):
    url = url or planURL
    if not urlSoup: urlSoup = getSoup(url)
    if urlSoup:
      if findAll:
          return urlSoup.find_all(elTag, elAttr)
      else:
          return urlSoup.find(elTag, elAttr)
    return None


def getElDOMPath(el=None, elAttrName='', defaultSep="/"):
    parentTempName = ''
    currEl = el
    pathElements = []
    pathLimit = []

    if (el):
      counter = 0

      while len(parentTempName) or not counter:
          
          parentTemp = currEl.parent if len(pathElements) else currEl
          parentTempName = parentTemp.name if parentTemp else ''

          if len(parentTempName):
              pathEl = parentTempName

              if parentTempName not in pathLimit:

                  try:
                      pathEl += getElId(parentTemp, True)
                  except:
                      pathEl += getElClass(parentTemp, True)

              if not counter and len(elAttrName):
                  elAttr = getElAttr(currEl, elAttrName)
                  pathEl += f'[{elAttrName}="{elAttr}"]'

              pathElements.append(pathEl)

          currEl = parentTemp
          counter+=1

    # join reversed list to get el path
    return defaultSep.join(pathElements[::-1])


def getElId(el=None, getConverted=False):
    elId = getElAttr(el, 'id')
    return '#' + elId if len(elId) and getConverted else ''


def getElClass(el=None, getConverted=False):
    classList = getElAttr(el, 'class')
    return '.' + '.'.join(classList) if len(classList) and getConverted else ''


def getElAttr(el=None, attrName=''):
  if not el: return el
  return el.get(attrName) if el.has_attr(attrName) else ''