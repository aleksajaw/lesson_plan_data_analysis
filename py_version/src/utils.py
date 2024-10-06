import requests
from bs4 import BeautifulSoup
from constants import *


def isType(obj, value):
    return obj.type == value


def getResponse(url=''):
    #print('Get response from: ', url,'.')
    return requests.get(url)


def getSoup(url=planStartUrl):
    response = getResponse(url)
    return BeautifulSoup(response.content, 'html.parser') if response else None


def getWithoutLastPart(url=''):
    url = url or planStartUrl
    urlParts = url.split('/')
    slicedUrlParts = urlParts[slice(len(urlParts)-1)]
    return '/'.join(slicedUrlParts)


def convertToFrameUrl(url='', frameSrc=''):
    frameUrl = getWithoutLastPart(url) + '/' + frameSrc
    return frameUrl


def getFrameSoup(url, urlSoup, frameName=''):
    foundFrame = urlSoup.find('frame', {'name': frameName})
    frameSrc = foundFrame['src'] if foundFrame else None
    return getSoup(convertToFrameUrl(url, frameSrc))


def findInFrame(elTag='', elAttr={}, frameName='', url='', findAll=False):
    url = url or planStartUrl
    urlSoup = getSoup(url)
    if urlSoup:
        frameSoup = getFrameSoup(url, urlSoup, frameName)
        return findInSource(elTag, elAttr, '', findAll, frameSoup)
        
    return None


def findInSource(elTag='', elAttr={}, url='', findAll=True, urlSoup=None):
    url = url or planStartUrl
    if not urlSoup: urlSoup = getSoup(url)
    if urlSoup:
      if findAll:
          return urlSoup.find_all(elTag, elAttr)
      else:
          return urlSoup.find(elTag, elAttr)
    return None


def getElPath(el=None, elAttrName='', defaultSep="/"):
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