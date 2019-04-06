import socket

#class of UDP sender
class UDP_Server:
    def __init__(self,myIp,port):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind((myIp,port))
    def recieve(self):
            data, addr = self.socket.recvfrom(1024)  # buffer size is 1024 bytes
            data=(data.decode(encoding="UTF-8"))
            return data



class UDP_Client:
    def __init__(self,targetIp,port):
        self._targetIp=targetIp
        self._port=port
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def send(self,msg):
            message=(msg.encode(encoding="UTF-8"))
            self.socket.sendto(message,(self._targetIp,self._port))

            