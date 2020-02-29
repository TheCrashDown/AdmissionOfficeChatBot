import time

from sys import path
path.append("./src")

from Parser import parse
from Corrector import correct

if __name__ == '__main__':
    while True:
        time.sleep(3600)
        parse()