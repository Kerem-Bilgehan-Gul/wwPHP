#!/usr/bin/python
from twisted.web import http;
from twisted.internet import reactor, protocol;
from twisted.python import log;
import re;
import sys;
import time;
from getmac import get_mac_address;
import datetime;
import subprocess;

log.startLogging(open('C:/Users/wwPHP/Desktop/log.log', 'w'))

class ProxyClient(http.HTTPClient):
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        self.contentLength = None

    def sendRequest(self):
        self.sendCommand(self.method, self.uri)

    def sendHeaders(self):
        for key, values in self.headers:
            if key.lower() == 'connection':
                values = ['close']
            elif key.lower() == 'keep-alive':
                next

            for value in values:
                self.sendHeader(key, value)
        self.endHeaders()

    def sendPostData(self):
        self.transport.write(self.postData)

    def connectionMade(self):
        self.sendRequest()
        self.sendHeaders()
        if self.method == 'POST':
            self.sendPostData()

    def handleStatus(self, version, code, message):
        self.originalRequest.setResponseCode(int(code), message)

    def handleHeader(self, key, value):
        if key.lower() == 'content-length':
            self.contentLength = value
        else:
            self.originalRequest.responseHeaders.addRawHeader(key, value)

    def handleResponse(self, data):
        data = self.originalRequest.processResponse(data)

        if self.contentLength != None:
            self.originalRequest.setHeader('Content-Length', len(data))

        self.originalRequest.write(data)

        self.originalRequest.finish()
        self.transport.loseConnection()

class ProxyClientFactory(protocol.ClientFactory):
    def __init__(self, method, uri, postData, headers, originalRequest):
        self.protocol = ProxyClient
        self.method = method
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest

    def buildProtocol(self, addr):
        return self.protocol(self.method, self.uri, self.postData,
                             self.headers, self.originalRequest)

    def clientConnectionFailed(self, connector, reason):
        log.err("Server connection failed: %s" % reason)
        self.originalRequest.setResponseCode(504)
        self.originalRequest.finish()

class ProxyRequest(http.Request):
    def __init__(self, channel, queued, reactor=reactor):
        http.Request.__init__(self, channel, queued)
        self.reactor = reactor

    def process(self):
        host = self.getHeader('host')
        if not host:
            log.err("No host header given")
            self.setResponseCode(400)
            self.finish()
            return
        port = 80
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        ClientsIp = self.getClientIP();
        remote_MAC = get_mac_address(ip=ClientsIp);
        Dates = datetime.datetime.now();
        f = open('C:/Users/wwPHP/Desktop/proxy_'+str(Dates.strftime("%d-%m-%Y"))+'.log', 'a');
        f.write(''+str(int(time.time()))+'----'+ClientsIp+'----'+remote_MAC+'----'+str(host)+':'+str(self.uri)+'\n');
        f.close();
        self.setHost(host, port)
        self.content.seek(0, 0)
        postData = self.content.read();
        factory = ProxyClientFactory(self.method, self.uri, postData,
                                     self.requestHeaders.getAllRawHeaders(),
                                     self)
        self.reactor.connectTCP(host, port, factory)
    def processResponse(self, data):
        return data

class TransparentProxy(http.HTTPChannel):
    requestFactory = ProxyRequest
 
class ProxyFactory(http.HTTPFactory):
    protocol = TransparentProxy
 
reactor.listenTCP(9091, ProxyFactory())
reactor.run()
