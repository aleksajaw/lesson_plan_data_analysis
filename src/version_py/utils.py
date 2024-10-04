import requests
from bs4 import BeautifulSoup
from constants import *


def isType(obj, value):
    return obj.type == value


def getResponse(url=''):
    print('url: ', url)
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

def findInFrame(elTag='', elAttr={}, frameName='', url='', findAll=False):
    url = url or planStartUrl
    urlSoup = getSoup(url)
    if urlSoup:
        foundFrame = urlSoup.find('frame', {'name': frameName})
        frameSrc = foundFrame['src'] if foundFrame else None
        frameSoup = getSoup(convertToFrameUrl(url, frameSrc))
        return frameSoup.find_all(elTag, elAttr) if findAll else frameSoup.find(elTag, elAttr)
    return None