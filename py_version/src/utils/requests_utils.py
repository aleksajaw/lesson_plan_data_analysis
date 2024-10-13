import requests
from constants import planURL


def getResponse(url=''):
    #print('Get response from: ', url,'.')
    return requests.get(url)


def getWithoutLastPart(url=''):
    url = url or planURL
    urlParts = url.split('/')
    slicedURLParts = urlParts[slice(len(urlParts)-1)]
    return '/'.join(slicedURLParts)


def convertToFrameURL(url='', frameSrc=''):
    frameURL = getWithoutLastPart(url) + '/' + frameSrc
    return frameURL