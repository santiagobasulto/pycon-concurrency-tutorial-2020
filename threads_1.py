# Run in REPL
import time
from threading import Thread


def simple_worker():
    print('hello')
    time.sleep(2)
    print('world')


print('Starting....')
t1 = Thread(target=simple_worker)
t1.start()

