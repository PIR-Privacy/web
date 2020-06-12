import re


def resultFileName(URL):
    currentUrlWhitoutHTTP = re.sub('(http://)|(https://)', '', URL)
    currentUrlWhitoutHTTP = re.sub(r'(/)|(&)|(=)|(\?)', '_', currentUrlWhitoutHTTP)
    return currentUrlWhitoutHTTP
