import sys
import socket
import re
import random
import hashlib
import threading
import logging
import signal
import os
import time
import datetime
import musqldeneme
class SIPSession:
    def sip_listener(self):
        while True:
            try:
                self.sipsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sipsocket.bind(('192.168.1.22', 5060))
                self.bind_port = self.sipsocket.getsockname()[1]
                # Setting the threshold of logger to DEBUG
                data = self.sipsocket.recvfrom(1500)
                #if not data: # after getting the first data
                print("sip listener geldim \r\n")
                self.sipsocket.setblocking(False)
                rcvdatabyte = data[0]                
                rcvdata = (data[0].decode("ascii"))
                rcvdataascii= str(rcvdatabyte[0])
                addr = data[1]
                addrport = addr[1]
                addrip = addr[0]
                if rcvdata.startswith(b'OPTIONS'):
                    cseq = re.findall(r'CSeq: (.*?)\r\n', rcvdata)[0]
                    cseq_type = cseq.split(" ")[1]
                    if cseq_type == "OPTIONS":
                        cseq_number = cseq.split(" ")[0]
                        contact_header = re.findall(r'Contact: <(.*?)>\r\n', rcvdata)[0]
                        #record_route = re.findall(r'Record-Route: (.*?)\r\n', rcvdata)[0]
                        call_from = re.findall(r'From: (.*?)\r\n', rcvdata)[0]
                        call_to = re.findall(r'To: (.*?)\r\n', rcvdata)[0]
                        call_id = re.findall(r'Call-ID: (.*?)\r\n', rcvdata)[0]
                        contact_to = re.split('>', call_to)[0]
                    totags = ''.join([random.choice('0123456789abcdef') for x in range(8)])
                    reply200opt = ""
                    reply200opt += "SIP/2.0 200 OK\r\n"
                    for (via_heading) in re.findall(r'Via: (.*?)\r\n', rcvdata):
                        reply200opt += "Via: " + str(via_heading) + "\r\n"
                        #record_route = re.findall(r'Record-Route: (.*?)\r\n', rcvdata)
                        #reply200bye += "Record-Route: " + str(record_route) + "\r\n"
                        reply200opt += "Contact: " + str(contact_to) + ":" + str(self.bind_port) + ">" "\r\n"
                        reply200opt += "To: " + str(call_to) + ";tag=" + str(totags) + "\r\n"
                        reply200opt += "From: " + str(call_from) + "\r\n"
                        reply200opt += "Call-ID: " + str(call_id) + "\r\n"
                        reply200opt += "CSeq: " + str(cseq_number) + " " + "OPTIONS" + "\r\n"
                        reply200opt += "Allow: SUBSCRIBE, NOTIFY, INVITE, ACK, CANCEL, BYE, REFER, INFO, OPTIONS, MESSAGE\r\n"
                        reply200opt += "Content-Type: application/sdp\r\n"
                        reply200opt += "Supported: replaces\r\n"
                        reply200opt += "User-Agent: " + str(self.USER_AGENT) + "\r\n"
                        reply200opt += "Content-Length: " + str("0") + "\r\n"
                        reply200opt += "\r\n"
                    print("OPTION DONULEN -->200 OK--->     " + "\r\n" + reply200opt + "\r\n")
                    self.sipsocket.sendto(bytes(reply200opt, 'ascii'),addr)
                    self.sip_listener(self)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
