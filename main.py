import time

from sys import path
path.append("./src")

from src.parser import parse

if __name__ == '__main__':
    while True:
        time.sleep(3600)
        parse()
