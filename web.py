'''
Created on Dec 4, 2015

@author: akaiser
'''

import cherrypy

from commute_times import get_time

class DirTimeWeb(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

    @cherrypy.expose
    def status(self):
        return "Server is up"

    @cherrypy.expose
    def time(self, origin, destination):
        return str(get_time(origin.replace(' ', '+'), destination.replace(' ', '+')))

if __name__ == '__main__':
    cherrypy.config.update( {'server.socket_host': '0.0.0.0'} )
    cherrypy.config.update( {'server.socket_port': 10000} )
    cherrypy.quickstart(DirTimeWeb())
