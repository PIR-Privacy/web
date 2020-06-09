import re


def resultFileName(URL):
    currentUrlWhitoutHTTP = re.sub('(http://)|(https://)', '', URL)
    currentUrlWhitoutHTTP = re.sub('(/)|(&)|(=)|(\?)', '_', currentUrlWhitoutHTTP)
    return currentUrlWhitoutHTTP
