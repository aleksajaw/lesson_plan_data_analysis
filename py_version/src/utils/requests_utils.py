import requests
from constants import *


def getResponse(url=''):
    #print('Get response from: ', url,'.')
    return requests.get(url)


def getWithoutLastPart(url=''):
    url = url or planStartUrl
    urlParts = url.split('/')
    slicedUrlParts = urlParts[slice(len(urlParts)-1)]
    return '/'.join(slicedUrlParts)


def convertToFrameUrl(url='', frameSrc=''):
    frameUrl = getWithoutLastPart(url) + '/' + frameSrc
    return frameUrl