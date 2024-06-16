from datetime import *
from time import time

def log(type: str, message: str):
    time = datetime.now()
    log_format = time.strftime(f'(%x - %X) [{type}] {message}\n')
    print(log_format)
    open('logs.txt','a').write(log_format)

def current_time_ms():
    return int(time() * 1000)