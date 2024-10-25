import os
import pathlib
import threading
import time
from threading import Thread
import multiprocessing

t0 = time.time()

i = 0

def concurrent_access():
    global i
    for a in range(100):
        tmp = i
        i = tmp + 1

# concurrent_access()

threads = []

for thread in range(3):
    threads.append(threading.Thread(target=concurrent_access))
    threads[-1].start()



print(i)
#
# def explore(path: str):
#     folders = []
#     threads = []
#     for f in os.listdir(path):
#         print(threading.current_thread().name, f"{path}/{f}")
#         if pathlib.Path(f"{path}/{f}").is_dir():
#             folders.append(f"{path}/{f}")
#     for folder in folders:
#         # explore(folder)
#         threads.append(Thread(target=lambda: explore(folder)))
#         threads[-1].start()
#     for thread in threads:
#         thread.join()
#
# explore("./")
#
# print("Total time", time.time() - t0)