from multiprocessing import shared_memory
import time
from datetime import datetime

import numpy as np


def estimate_time(result_array_name, point_counts_name, result_arrays_shape, point_counts_shape):
    '''
    Console output of statistics of the current segmentation
    :param result_array_name: Name of the shared memory result array
    :param point_counts_name: Name of the shared memory for the already completed points array
    :param result_arrays_shape: Shape of the shared memory result array
    :param point_counts_shape: Shape of the shared memory for the already completed points array
    :return: Nothing, just prints on console
    '''
    result_memory = shared_memory.SharedMemory(name=result_array_name)
    result_array = np.ndarray(result_arrays_shape, dtype=np.float16, buffer=result_memory.buf)
    point_counts_memory = shared_memory.SharedMemory(name=point_counts_name)
    point_counts = np.ndarray(point_counts_shape, dtype=np.int64, buffer=point_counts_memory.buf)
    sleep_seconds = 30
    start = datetime.now()
    print(datetime.now().strftime(
        "%H:%M:%S") + " => Time estimation started. The first estimation will be given in " + str(
        sleep_seconds) + " seconds")
    time.sleep(30)
    while True:
        try:
            print("")
            finished = sum(point_counts)
            not_finished = len(result_array) - finished
            current = datetime.now()
            progress = finished / len(result_array)
            performance = finished / (current - start).total_seconds()
            estimated_time = not_finished / performance
            print(datetime.now().strftime("%H:%M:%S") + " => Progress: " + str(progress * 100) + " %")
            print(datetime.now().strftime("%H:%M:%S") + " => Performance: " + str(performance) + " points per second")
            print(datetime.now().strftime("%H:%M:%S") + " => Estimated time: " + str(estimated_time / 60) + " minutes")
            time.sleep(sleep_seconds)
        except ZeroDivisionError:
            start = datetime.now()
            time.sleep(sleep_seconds)
