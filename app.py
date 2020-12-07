from time import sleep
from datetime import datetime
import logging


def app():
    from aiogram import executor
    import loader as ld
    import handlers
    app()


if __name__ == '__main__':
    while True:
        try:
            app()
        except Exception as e:
            print(e)
            sleep(1)
            print(f'FULL Restarting \t[{datetime.now()}]')
