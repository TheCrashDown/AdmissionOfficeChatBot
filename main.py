import time

from sys import path
path.append("./src")

from Parser import parser

if __name__ == '__main__':
    while True:
        time.sleep(3600)
        parser.parse()
