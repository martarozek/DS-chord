from functools import wraps
from time import time


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        file_csv = open("measure.csv", "w")
        file_csv.write(f"measurement, {end-start}\n")
        file_csv.close()
        print ('Elapsed time: {}'.format(end-start))
        return result
    return wrapper