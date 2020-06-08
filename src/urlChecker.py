import requests


def urlChecker(URL):
    try:
        page = requests.get(URL)
        if page.status_code in [404, 403]:
            print(URL + " error " + str(page.status_code))
            return False
    except requests.exceptions.ConnectionError as e:
        print(URL + " not resolved")
        return False
    print(URL + " ok")
    return True


if __name__ == '__main__':

    file = open("result/error.log", "r")
    print("---------------------------------------------------------------------")
    for url in file.read().split("\n"):
        if url == "":
            continue
        else:
            print("Working url : " + url)
            urlChecker(url)
            print("---------------------------------------------------------------------")
