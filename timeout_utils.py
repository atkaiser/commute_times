'''
Created on Dec 2, 2017

Utils related to handling timeouts

@author: akaiser
'''


class TimeoutException(Exception):
    pass


def handler(signum, frame):
    raise TimeoutException("")
