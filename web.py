'''
Created on Dec 4, 2015

@author: akaiser
'''
import random
import string

import cherrypy

from commute_times import get_time

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def generate(self, length=8):
        return ''.join(random.sample(string.hexdigits, int(length)))
    
    @cherrypy.expose
    def time(self, origin, destination):
        return str(get_time(origin.replace(' ', '+'), destination.replace(' ', '+')))

if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())