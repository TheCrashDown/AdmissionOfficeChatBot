from src.bot import bot
import time
from src.parser import parse

if __name__ == '__main__':
    while True:
        time.sleep(3600)
        parse()
