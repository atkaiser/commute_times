'''
Created on Dec 4, 2015

@author: akaiser
'''

import cherrypy

from browser_pool import BrowserPool
from commute_times import all_info
from commute_times import get_time


class DirTimeWeb(object):

    def __init__(self):
        cherrypy.engine.subscribe('start', self.start)
        cherrypy.engine.subscribe('stop', self.stop)

    def start(self):
        print("STARTING UP SERVER")

    def stop(self):
        print("STOPPING SERVER")
        browser_pool = BrowserPool()
        browser_pool.close_all()

    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def status(self):
        return "Server is up"

    @cherrypy.expose
    def pool(self):
        browser_pool = BrowserPool()
        return browser_pool.status()

    @cherrypy.expose
    def time(self, origin, destination):
        return str(get_time(origin.replace(' ', '+'), destination.replace(' ', '+')))

    @cherrypy.expose
    def all_info(self, origin, destination):
        return all_info(origin.replace(' ', '+'), destination.replace(' ', '+'))


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 10000})
    cherrypy.quickstart(DirTimeWeb())
