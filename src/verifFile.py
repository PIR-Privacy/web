import datetime
import os
import shutil


def verif(path, firstLine):
    if os.path.exists(path):
        shutil.copyfile(path,
                        path + datetime.datetime.now().strftime('_%m_%d_%Y_%H_%M_%S'))
    with open(path, "w") as file:
        file.write(firstLine)
