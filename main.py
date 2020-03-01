from src.parser import parse
from src.bot import bot
import time

if __name__ == '__main__':
    while True:
        time.sleep(3600)
        parse()
