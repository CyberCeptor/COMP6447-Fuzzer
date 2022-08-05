import threading
import _thread as thread

def handler(fn_name):
    print(f"{fn_name} exitted after timing out.")
    thread.interrupt_main()

def timeout(n:float, func, *args, **kwargs):
    """
    Exit if function takes longer than n seconds
    """
    timer = threading.Timer(n, handler, args=[func.__name__])
    timer.start()
    try:
        result = func(*args, **kwargs)
    finally:
        timer.cancel()
    return result
