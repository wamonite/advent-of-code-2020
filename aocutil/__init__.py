# -*- coding: utf-8 -*-

import time


# https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)

        else:
            print(f'{method.__name__} {(te - ts) * 1000:.2f}ms')

        return result

    return timed


def load_file(file_name):
    with open(file_name) as file_object:
        return list(map(str.strip, file_object.readlines()))
