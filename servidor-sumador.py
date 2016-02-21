#!/usr/bin/python

"""
Simple HTTP Server version 2: reuses the port, so it can be
restarted right after it has been killed. Accepts connects from
the outside world, by binding to the primary interface of the host.

Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket
import random 

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind(('localhost', 1235))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)
entero = None;
suma = None;

try:
    while True:
        print 'Waiting for connections'
        (recvSocket, address) = mySocket.accept()
        print 'Request received:'

        peticion = recvSocket.recv(2048)

        if (entero == None):
            entero = int(peticion.split(' ')[1][1:])
        elif (entero != None):
            entero2 = int(peticion.split(' ')[1][1:])
            suma = entero + entero2

        print peticion
        print 'Answering back...'

        numero = random.randint(1, 10000000);

        html = "<html><body><h1>Hello World! <!/h1><p>And in particular hello to you, " + str(address[1])
        html += "<p>"
        #html += '<p><a href ="http://localhost:1235' + str(numero) + '">Dame otra</a></p>'

        if (suma != None):
            html += "<p>La suma de tus GET/ es: " + str(suma) + "</p>"
            entero = suma
            
        html += "</body></html>"
        
        recvSocket.send("HTTP/1.1 200 OK\r\n\r\n" + html + "\r\n")
        recvSocket.close()
except KeyboardInterrupt:
    print "Closing binded socket"
    mySocket.close()