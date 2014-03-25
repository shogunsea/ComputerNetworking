#!/usr/bin/python
import select
import socket
import sys
import	pdb
import re
from struct import *



# sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
# sudo python rawhttpget.py http://david.choffnes.com/classes/cs4700sp14/project4.php
# sudo python rawhttpget.py http://david.choffnes.com/classes/cs4700sp14/2MB.log 
# sudo python rawhttpget.py http://david.choffnes.com/classes/cs4700sp14/10MB.log
# sudo python rawhttpget.py http://david.choffnes.com/classes/cs4700sp14/50MB.log



#'''===Default constants==='''
# SOURCE_PORT = 55555 #55555 as default, will be generated
PORT = 80
# OK_MSG = '200'
# ACTION_START = 9
# ACTION_END = 12

sourceIP = ''
destIP = ''
# dupIDs = {}
ip_id_global = 0
false = 0
true = 1


'''===Raw Socket Functions==='''
# Checksum function needed for calculating checksum
# Note the bit operates

def checkSum(msg):
	s = 0
	for i in range(0, len(msg), 2):
		# differnt from tutorial
		if i+1 <= len(msg)-1:
			w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
		else:
			w = ord(msg[i])
		s = s + w
	
	s = (s>>16) + (s & 0xffff)
	s = s + (s >> 16)
	s = ~s & 0xffff
	return s

# Get available port
def getFreePort():

	sPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sPort.bind(("",0))
	sPort.listen(1)
	port = sPort.getsockname()[1]
	sPort.close()
	return port

# Get local IP
'''Note: Get Local IP in the environment like ubuntu is troubled, gethostname only 
returns 127.0.0.1 like address stored in the /etc/hosts file, this method is used for
this kind of situation'''
def getLocalIP(host):
  ipAddress = ''
  
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, 8000))
    ipAddress = s.getsockname()[0]
    s.close()
  except:
    pass

  return ipAddress 

# Generate IP header and add it to the packet
def generateIPPacket(msg, sourceIP, destIP):
	# IP header fields
	# print "Generating IP packet..."
	ip_version = 4 # Version ipv4
	ip_ihl = 5 #Length 4*5 = 20bytes
	ip_ver_ihl = (ip_version << 4) + ip_ihl
	ip_typeOfService = 0 #Normal
	ip_totalLength = 0
	global ip_id_global
	ip_id_global = ip_id_global + 1
	ip_id = ip_id_global #Pakcet id
	# ip_flags = 4 # 3bit, second 1 means no fragment
	ip_fragOffset = 0 # Shows the location in the segments
	ip_ttl = 255 # Living time 255 is max
	ip_protocol = socket.IPPROTO_TCP # TCP is 6
	ip_checksum = 0 
	ip_source = socket.inet_aton(sourceIP)
	ip_dest = socket.inet_aton(destIP)
	
	
	# Assemble ip packet
	ip_header = pack('!BBHHHBBH4s4s' , ip_ver_ihl, ip_typeOfService, ip_totalLength, ip_id, ip_fragOffset, ip_ttl, ip_protocol, ip_checksum, ip_source, ip_dest)
	
	packet = ip_header + msg
	
	return packet

# Generate the packet with TCP and IP header
def generateTCPPacket(msg, sourceIP, destIP, flag, seqNum, ackNum):
    # print "Generating TCP packet..."
    # TCP header fields
    tcp_sourcePort = SOURCE_PORT #Get the port generated
    tcp_destPort = PORT #dest Port
    tcp_seqNum = seqNum #Sequence number
    tcp_ackNum = ackNum #Ack number
    tcp_dataOffSet = 5 #5*4 = 20bytes
    #Functional bits
    tcp_dataOffSet_reserve = (tcp_dataOffSet<<4) + 0 #Reserved are 0s
    tcp_urg = 0 # 
    tcp_ack = 0 # 1 means ack packet
    tcp_psh = 0 #
    tcp_rst = 0 # reset packet
    tcp_syn = 0 # syn packet
    tcp_fin = 0 # finish
    tcp_window = 65535 # allow server to send packet as big as 65535
    tcp_checksum = 0 # originally 0
    tcp_urgPointer = 0 #
	
	# Set the flag as needed
    if flag == 'syn': tcp_syn = 1
    if flag == 'ack': tcp_ack = 1
    if flag == 'rst': tcp_rst = 1
    if flag == 'fin,ack':
    	tcp_fin = 1
        tcp_ack = 1
	
	# Assemble first header used for checksum
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
	
    tcp_header = pack('!HHLLBBHHH' , tcp_sourcePort, tcp_destPort, tcp_seqNum, tcp_ackNum, tcp_dataOffSet_reserve, tcp_flags, tcp_window, tcp_checksum, tcp_urgPointer)
    # 
	# Construct pseudo header
    sourceAddress = socket.inet_aton(sourceIP)
    destAddress = socket.inet_aton(destIP)
    placeHolder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header) + len(msg)
    
    pseudoHeader = pack('!4s4sBBH' , sourceAddress , destAddress , placeHolder , protocol , tcp_length);
    pseudoHeader = pseudoHeader + tcp_header + msg
    
    # Calculate checksum
    tcp_checksum = checkSum(pseudoHeader)
    
    # Assemble TCP header in order
    tcp_header = pack('!HHLLBBH' , tcp_sourcePort, tcp_destPort, tcp_seqNum, tcp_ackNum, tcp_dataOffSet_reserve, tcp_flags,  tcp_window) + pack('H', tcp_checksum) + pack('!H', tcp_urgPointer)
    
    packet = tcp_header + msg
	
	# Add IP header and return
    return generateIPPacket(packet, sourceIP, destIP)

# Decode IP header and store in a map
def decodeIPHeader(packet):
    
    ip_header = packet[0:20]
    # mapHeader = {}
    # mapHeader["version"] = (int(ord(packet[0])) & 0xF0)>>4
    # mapHeader["headerLen"] = (int(ord(packet[0])) & 0x0F)<<2
    # # mapHeader["serviceType"] = hex(int(ord(packet[1])))
    # mapHeader["totalLen"] = (int(ord(packet[2])<<8))+(int(ord(packet[3])))
    # # mapHeader["id"] = (int( ord(packet[4])<<8 )) + (int( ord(packet[5])))
    # # mapHeader["flag"] = int(ord(packet[6]) & 0xE0)>>5
    # # mapHeader["fragOff"] = int(ord(packet[6]) & 0x1F)<<8 + int(ord(packet[7]))
    # mapHeader["ttl"] = int(ord(packet[8]))
    # mapHeader["protocol"] = int(ord(packet[9]))
    # # mapHeader["checksum"] = int(ord(packet[10])<<8)+int(ord(packet[11]))
    # mapHeader["sourceIP"] = "%d.%d.%d.%d" % (int(ord(packet[12])),int(ord(packet[13])),int(ord(packet[14])), int(ord(packet[15])))
    # mapHeader["destIP"] = "%d.%d.%d.%d" % (int(ord(packet[16])),int(ord(packet[17])),int(ord(packet[18])), int(ord(packet[19])))
    # return mapHeader
    #now unpack them :)
    iph = unpack('!BBHHHBBH4s4s' , ip_header)
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    iph_length = ihl * 4
    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);

    mapHeader = {}
    mapHeader["version"] = version
    mapHeader["headerLen"] = ihl
    #mapHeader["serviceType"] = hex(int(ord(packet[1])))
    mapHeader["totalLen"] = iph_length
    #mapHeader["id"] = (int( ord(packet[4])<<8 )) + (int( ord(packet[5])))
    # mapHeader["flag"] = int(ord(packet[6]) & 0xE0)>>5
    #mapHeader["fragOff"] = int(ord(packet[6]) & 0x1F)<<8 + int(ord(packet[7]))
    mapHeader["ttl"] = ttl
    mapHeader["protocol"] = protocol
    # mapHeader["checksum"] = int(ord(packet[10])<<8)+int(ord(packet[11]))
    mapHeader["sourceIP"] = s_addr
    mapHeader["destIP"] = d_addr
    # 
    # print 'hhhhhhh'
    return mapHeader

# Decode TCP header and store in a map
############ERROR here
def decodeTCPHeader2(packet):
    tcp_header = packet[0:20]
    #now unpack them :)
    tcph = unpack('!HHLLBBHHH' , tcp_header)
    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]#96
    tcph_length = doff_reserved >> 4
    h_size = 20 + tcph_length * 4
    data_size = len(packet) - h_size
    data = packet[h_size:]
    mapHeader = {}
    mapHeader["sourcePort"] = source_port
    mapHeader["destPort"] = dest_port
    mapHeader["seqNum"] = sequence
    mapHeader["ackNum"] = acknowledgement
    mapHeader["doff_reserved"] = doff_reserved
    mapHeader["tcph_length"] = tcph_length
    mapHeader["h_size"] = h_size
    mapHeader["data_size"] = data_size
    mapHeader["data"] = data
    return mapHeader



def decodeTCPHeader(packet_long):
    packet = packet_long#[20:]
    mapHeader = {}
    mapHeader["sourcePort"] = (int(ord(packet[0])<<8))+(int(ord(packet[1])))
    mapHeader["destPort"] = (int(ord(packet[2])<<8))+(int(ord(packet[3])))
    mapHeader["seqNum"] =(int(ord(packet[4])<<24))+(int(ord(packet[5])<<16))+(int(ord(packet[6])<<8))+(int(ord(packet[7])))
    mapHeader["ackNum"] = (int(ord(packet[8])<<24))+(int(ord(packet[9])<<16))+(int(ord(packet[10])<<8))+(int(ord(packet[11])))
    mapHeader["dataOffSet"] = ((int(ord(packet[12])) & 0xF0)>>4)<<2
    mapHeader["urg"] = int(ord(packet[13]) & 0x20)>>5
    mapHeader["ack"] = int(ord(packet[13]) & 0x10)>	>4
    mapHeader["psh"] = int(ord(packet[13]) & 0x8)>>3
    mapHeader["rst"] = int(ord(packet[13]) & 0x4)>>2
    mapHeader["syn"] = int(ord(packet[13]) & 0x2)>>1
    mapHeader["fin"] = int(ord(packet[13]) & 0x1)
    mapHeader["window"] = int(ord(packet[14])<<8)+int(ord(packet[15]))
    mapHeader["checksum"] = int(ord(packet[16])<<8)+int(ord(packet[17]))
    mapHeader["urgPointer"] = int(ord(packet[18])<<8)+int(ord(packet[19]))
    mapHeader["data"] = packet[mapHeader["dataOffSet"]:]
    # 
    jj = decodeTCPHeader2(packet_long)
    if mapHeader['seqNum']!= jj['seqNum']:
    	print '!!!!!!!! seqNum not same.'
    if mapHeader['ackNum']!=jj['ackNum']:
    	print '!!!!!!!! ackNum not same.'
    
    return mapHeader
    
   
'''===Validation functions==='''
#Check IP Header
def checkIPHeader(packet, mapIP, destIP):
    # Check remote IP
	# if destIP != mapIP['sourceIP']:
	# 	print "ip dest"
	# 	return false
	# if checkSum(packet) != mapIP['checksum']:
	# 	print "ip checksum:", mapIP['checksum'],' ceh(p):',checkSum(packet)
	# 	print "ip check"
	# 	return false
    
    # Check protocol
	if 6 != mapIP['protocol']:
		print "ip proto"
		return false
    # Check duplicate packet
    ######WHY? Not necessary!
	# if dupIDs.has_key(mapIP['id']):
	# 	print "ip dup id", mapIP['id']
	# 	return false
	# else:
	# 	dupIDs[mapIP['id']] = mapIP['id']
	return true

##TCP checksum calculate
# def checkTCPChecksum(packet, checksum):
# 	global sourceIP
# 	global destIP
# 	# pseudo header fields
# 	sourceAddress = socket.inet_aton(sourceIP)
# 	destAddress = socket.inet_aton(destIP)
# 	placeHolder = 0
# 	protocol = socket.IPPROTO_TCP
# 	tcp_length = len(packet)
   
# 	pseudoHeader = pack('!4s4sBBH' , sourceAddress , destAddress , placeHolder , protocol , tcp_length);
# 	pseudoHeader = pseudoHeader + packet
# 	print "sudoheader:%r"%pseudoHeader
# 	tcp_checksum = checkSum(pseudoHeader)
# 	print "tcpch:",tcp_checksum, "chesum:", checksum , "tcplem:", tcp_length
# 	if tcp_checksum != checksum:
# 		return false
# 	return true

#Check TCP header
def checkTCPHeader(packet, mapTCP, seqNum, ackNum, msgLen):
	# if not checkTCPChecksum(packet, mapTCP['checksum']):
	# 	print "tcp check"
	# 	return false
    # Check packet in order
	
	print 'checking tcp header...'
	# 
	if mapTCP['destPort']!=SOURCE_PORT:
		print 'The destPort of this packet is not the source port of sending socket!!'
	if (seqNum + msgLen) != mapTCP['ackNum']:
		print "tcp seq mine:", seqNum+msgLen, " received:", mapTCP['ackNum'], "msglen", msgLen
		return false
	if ackNum != mapTCP['seqNum']:
		if mapTCP.get('syn') != 1 and mapTCP.get('ack') == 1:
			print "tcp ack"
			return false
	return true

def checkPacket(packet, mapIP, mapTCP, sentSeq, sentAck, sentMsgLen, sendsock):
	# global dupIDs
	print "Validating Packet..."
	
	headerIPlen = mapIP['headerLen']*4
	packetTCP = packet[headerIPlen:]
	packetIP = packet[0:headerIPlen]
	print 'sent ack: '+ str(sentAck)
	print 'sent seqNum: '+str(sentSeq)+' parsed seqNum: '+str(mapTCP['seqNum'])
	tcp_validation = checkTCPHeader(packetTCP, mapTCP, sentSeq, sentAck, sentMsgLen)
	ip_validation = checkIPHeader(packetIP, mapIP, destIP)
	if not tcp_validation or not ip_validation:
		'''This rst may fail because of the iptable blocking'''
		if not tcp_validation:
			print tcp_validation
			print 'TCP header fails.'
		if not ip_validation:
			print ip_validation
			print 'IP header fails.'

		print 'errrrrrr'
		return false
	return true
		
		# packetRST = generateTCPPacket('', sourceIP, destIP, 'rst', mapTCP['ackNum'], sentAck)
		# sendsock.sendto(packetRST, (destIP , 0 ))
		# handleError("Packet or header error")

#Handle ack time out
def timeOutRecv(recvsock, size):
	

	# Retransmit in 60 seconds
	timeout = 60
	
	ready = select.select([recvsock], [], [], timeout)
	# 
	# When timeout reached , select return three empty lists
	if ready[0]:
		
		response = recvsock.recvfrom(size)
		# ethernet_frame = response[0]
		# tcp_frame = ethernet_frame[14:]
	else:
		# handleError("Time out!")
		print "Time out! Retransmit"
		return false
	
	
	print 'timeOutRecv competed.'
	# return (tcp_frame, response[1])
	return response

#If retransmit do not work for 5 times(5 minutes), recognize as connection failure
def nonBlockTransmit(packet, recvsock, size, sendsock):
	

	response = timeOutRecv(recvsock, size)
	i = 0
	
	while not response:
		sendsock.sendto(packet, (destIP , 0 ))
		i = i + 1
		if i == 5:
			handleError("3 Transmission Connection failure")
			break;
		response = timeOutRecv(recvsock, size)
	
	return response


#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b


def three_way_handshake(host):
	global sourceIP
	global destIP

	sourceIP = socket.gethostbyname(socket.gethostname())#Get local IP
	# If falsed by hosts file use another method
	if sourceIP[0:3] == '127':
		sourceIP = getLocalIP(host)
	destIP= socket.gethostbyname(host)
	
	# Create two raw sockets, one for sending and one for receiving
	try:
		sendsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error , msg:
		handleError("Sending socket could not be created. " + str(msg[0]) + " " + msg[1])
	
	# Receiving socket is created in IPPROTO_TCP which could receive both IP and TCP headers
	try:
		# recvsock = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
		recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
	except socket.error , msg:
		handleError("Receiving socket could not be created. " + str(msg[0]) + " " + msg[1])
	
	'''Connection setup: three handshakes'''
	synMsg = ''
	seqNum = 4321 # Starting seq number
	ackNum = 0
	packet = generateTCPPacket(synMsg, sourceIP, destIP, 'syn', seqNum, ackNum)
	
	# First syn handshake
	sendsock.sendto(packet, (destIP , 0 ))
	response, addr =  nonBlockTransmit(packet, recvsock, 2048, sendsock)
	mapIP = decodeIPHeader(response)
	headerIPlen = mapIP['headerLen']*4
	# 
	mapTCP = decodeTCPHeader(response[headerIPlen:])#headerIPlen*4!?
	# mapTCP = decodeTCPHeader(response)
	#Validate packet
	
	while checkPacket(response, mapIP, mapTCP, seqNum, ackNum, 1, sendsock)==false:
		response, addr =  nonBlockTransmit(packet, recvsock, 2048, sendsock)
		mapIP = decodeIPHeader(response)
		headerIPlen = mapIP['headerLen']*4
		# 
		mapTCP = decodeTCPHeader(response[headerIPlen:])#headerIPlen*4!?




	print "Connection established?????????"
	
	if mapTCP.get('syn') == 1 and mapTCP.get('ack') == 1:
		seqNum = mapTCP['ackNum']
		ackNum = mapTCP['seqNum']+1
		packet = generateTCPPacket(synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
		sendsock.sendto(packet, (destIP , 0 ))
	
	#Handshake end, connection established
	return [sendsock, recvsock, seqNum, ackNum]

def connection_tear_down_by_server(sendsock, recvsock, seqNum, ackNum):
	'''Receivd fin, tear down connection'''
	synMsg = ''

	packet = generateTCPPacket(synMsg, sourceIP, destIP, 'fin,ack', seqNum, ackNum)
	sendsock.sendto(packet, (destIP , 0 ))
	response, addr = timeOutRecv(recvsock, 2048)
	mapIP = decodeIPHeader(response)
	headerIPlen = mapIP['headerLen']
	mapTCP = decodeTCPHeader(response[headerIPlen:])
	
	if mapTCP['ack'] == 1:
		print "receive succceed:", len(receivedMsg)
	
	# Close sockets
	sendsock.close()
	recvsock.close()
	return true


def connection_tear_down_by_client(sendsock, recvsock, seqNum, ackNum):
	synMsg = ''
	packet = generateTCPPacket(synMsg, sourceIP, destIP, 'fin,ack', seqNum, ackNum)
	sendsock.sendto(packet, (destIP , 0 ))
	response, addr = nonBlockTransmit(packet, recvsock, 65535, sendsock)
	mapIP = decodeIPHeader(response)
	headerIPlen = mapIP['headerLen']*4
	mapTCP = decodeTCPHeader(response[headerIPlen:])

	# print 'mapTCP fin:' + str(mapTCP['fin'])
	i = 0
	while mapTCP['fin']!=1:
		response, addr = nonBlockTransmit(packet, recvsock, 65535, sendsock)
		mapIP = decodeIPHeader(response)
		headerIPlen = mapIP['headerLen']*4
		mapTCP = decodeTCPHeader(response[headerIPlen:])
		print 'mapTCP fin:' + str(mapTCP['fin'])
		print mapTCP['fin']!=1
		if i>30:#receive at most 30 promiscuous packets, then force to close down
			break

	seqNum = mapTCP['ackNum']
	ackNum = mapTCP['seqNum']+1
	packet = generateTCPPacket(synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
	sendsock.sendto(packet, (destIP , 0 ))
	
	# Close sockets
	sendsock.close()
	recvsock.close()
	return true







'''===Raw socket connecting method==='''
# Used for constructing packets, send the message, then receive and assemble the response
def tcp_transmission(msg, host):
	
	global sourceIP
	global destIP

	# sourceIP = socket.gethostbyname(socket.gethostname())#Get local IP
	# # If falsed by hosts file use another method
	# if sourceIP[0:3] == '127':
	# 	sourceIP = getLocalIP(host)
	# destIP= socket.gethostbyname(host)
	
	# # Create two raw sockets, one for sending and one for receiving
	# try:
	# 	sendsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	# except socket.error , msg:
	# 	handleError("Sending socket could not be created. " + str(msg[0]) + " " + msg[1])
	
	# # Receiving socket is created in IPPROTO_TCP which could receive both IP and TCP headers
	# try:
	# 	recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
	# except socket.error , msg:
	# 	handleError("Receiving socket could not be created. " + str(msg[0]) + " " + msg[1])
	
	# '''Connection setup: three handshakes'''
	# synMsg = ''
	# seqNum = 4321 # Starting seq number
	# ackNum = 0
	# packet = generateTCPPacket(synMsg, sourceIP, destIP, 'syn', seqNum, ackNum)
	
	# # First syn handshake
	# sendsock.sendto(packet, (destIP , 0 ))
	# response, addr =  nonBlockTransmit(packet, recvsock, 2048, sendsock)
	# mapIP = decodeIPHeader(response)
	# headerIPlen = mapIP['headerLen']*4
	# # 
	# mapTCP = decodeTCPHeader(response[headerIPlen:])#headerIPlen*4!?
	# # mapTCP = decodeTCPHeader(response)
	# #Validate packet
	
	# while checkPacket(response, mapIP, mapTCP, seqNum, ackNum, 1, sendsock)==false:
	# 	response, addr =  nonBlockTransmit(packet, recvsock, 2048, sendsock)
	# 	mapIP = decodeIPHeader(response)
	# 	headerIPlen = mapIP['headerLen']*4
	# 	# 
	# 	mapTCP = decodeTCPHeader(response[headerIPlen:])#headerIPlen*4!?




	# print "Connection established?????????"
	
	# if mapTCP.get('syn') == 1 and mapTCP.get('ack') == 1:
	# 	seqNum = mapTCP['ackNum']
	# 	ackNum = mapTCP['seqNum']+1
	# 	packet = generateTCPPacket(synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
	# 	sendsock.sendto(packet, (destIP , 0 ))
	
	# #Handshake end, connection established

	connection = three_way_handshake(host)

	sendsock = connection[0]
	recvsock = connection[1]
	seqNum = connection[2]
	ackNum = connection[3]
	

	print 'Established! Starting to receive!!!!!!'
	
	'''Send the message and receive'''
	#Initiated receive string
	receivedMsg = ''
	synMsg = ''
    # Assemble the message packet
	packet = generateTCPPacket(msg, sourceIP, destIP, 'ack', seqNum, ackNum)
    # Send the packet 
	sendsock.sendto(packet, (destIP , 0 ))
    # Receive with the time out control method
	response, addr = nonBlockTransmit(packet, recvsock, 2048, sendsock)
    # Decode IP header
	
	mapIP = decodeIPHeader(response)
	headerIPlen = mapIP['headerLen']*4
    # Decode TCP header
	mapTCP = decodeTCPHeader(response[headerIPlen:])
	
    # Check the packet in various aspects
	while checkPacket(response, mapIP, mapTCP, seqNum, ackNum, len(msg), sendsock) == false:
		response, addr = nonBlockTransmit(packet, recvsock, 2048, sendsock)
	    # Decode IP header
		
		mapIP = decodeIPHeader(response)
		headerIPlen = mapIP['headerLen']*4
	    # Decode TCP header
		mapTCP = decodeTCPHeader(response[headerIPlen:])
    
	
    # Get the header total length
	headerLength = mapTCP['dataOffSet']+headerIPlen
	msg_dict = {}
	msg_arr = []
    # Assemble and receive the remain message in a loop
	while mapTCP['ack'] == 1 and mapTCP['fin'] == 0:
		# Get the data and assemble
		
		thisMsg = response[headerLength:]
		receivedMsg = receivedMsg + thisMsg
		
        # Get the next seq and ack
		seqNum = mapTCP['ackNum']
		ackNum = mapTCP['seqNum']+len(thisMsg)

		msg_dict[ackNum] = thisMsg
		msg_arr.append(ackNum)
		print 'seqNum: ' + str(mapTCP['seqNum'])
		print 'msg len: ' + str(len(thisMsg))
        # Only ack to ones with data
		if len(thisMsg) != 0:
			packet = generateTCPPacket(synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
			sendsock.sendto(packet, (destIP , 0 ))
		
		# Repeat the receiving process
		response, addr = nonBlockTransmit(packet, recvsock, 65535, sendsock)
		
		mapIP = decodeIPHeader(response)
		headerIPlen = mapIP['headerLen']*4
		mapTCP = decodeTCPHeader(response[headerIPlen:])
		

		while checkPacket(response, mapIP, mapTCP, seqNum, ackNum, len(synMsg), sendsock)==false:
			response, addr = nonBlockTransmit(packet, recvsock, 65535, sendsock)
			mapIP = decodeIPHeader(response)
			headerIPlen = mapIP['headerLen']*4
			mapTCP = decodeTCPHeader(response[headerIPlen:])
			


		headerLength = mapTCP['dataOffSet']+headerIPlen

	# for i in range(len(msg_arr)):
	# 	if i<len(msg_arr)-1:
	# 		if msg_arr[i]<msg_arr[i+1]:
	# 			print true
	# 		else:
	# 			print false
	seqNum = mapTCP['ackNum']
	ackNum = mapTCP['seqNum']+1
	print 'Tearing down connection...'
	if connection_tear_down_by_server(sendsock,recvsock, seqNum, ackNum):
		print 'Connection is disconnected.'
	# '''Receivd fin, tear down connection'''
	# seqNum = mapTCP['ackNum']
	# ackNum = mapTCP['seqNum']+1
	# packet = generateTCPPacket(synMsg, sourceIP, destIP, 'fin,ack', seqNum, ackNum)
	# sendsock.sendto(packet, (destIP , 0 ))
	# response, addr = timeOutRecv(recvsock, 2048)
	# mapIP = decodeIPHeader(response)
	# headerIPlen = mapIP['headerLen']
	# mapTCP = decodeTCPHeader(response[headerIPlen:])
	
	# if mapTCP['ack'] == 1:
	# 	print "receive succceed:", len(receivedMsg)
	
	# # Close sockets
	# sendsock.close()
	# recvsock.close()
	

	return receivedMsg


def ethernet_transmission(msg, host):
	global sourceIP
	global destIP

	mac_address = get_mac_address(host)


	connection = three_way_handshake(host)

	sendsock = connection[0]
	recvsock = connection[1]
	seqNum = connection[2]
	ackNum = connection[3]
	

	print 'Established! Starting to receive!!!!!!'
	'''Send the message and receive'''
	#Initiated receive string
	receivedMsg = ''
	synMsg = ''
    # Assemble the message packet
	packet = generateTCPPacket(msg, sourceIP, destIP, 'ack', seqNum, ackNum)
    # Send the packet 
	sendsock.sendto(packet, (destIP , 0 ))
    # Receive with the time out control method
	response, addr = nonBlockTransmit(packet, recvsock, 2048, sendsock)
    # Decode IP header
	
	mapIP = decodeIPHeader(response)
	headerIPlen = mapIP['headerLen']*4
    # Decode TCP header
	mapTCP = decodeTCPHeader(response[headerIPlen:])
	
    # Check the packet in various aspects
	while checkPacket(response, mapIP, mapTCP, seqNum, ackNum, len(msg), sendsock) == false:
		response, addr = nonBlockTransmit(packet, recvsock, 2048, sendsock)
	    # Decode IP header
		
		mapIP = decodeIPHeader(response)
		headerIPlen = mapIP['headerLen']*4
	    # Decode TCP header
		mapTCP = decodeTCPHeader(response[headerIPlen:])
    

    # Get the header total length
	headerLength = mapTCP['dataOffSet']+headerIPlen
	msg_dict = {}
	msg_arr = []
    # Assemble and receive the remain message in a loop
	while mapTCP['ack'] == 1 and mapTCP['fin'] == 0:
		# Get the data and assemble
		
		thisMsg = response[headerLength:]
		receivedMsg = receivedMsg + thisMsg
		
        # Get the next seq and ack
		seqNum = mapTCP['ackNum']
		ackNum = mapTCP['seqNum']+len(thisMsg)

		msg_dict[ackNum] = thisMsg
		msg_arr.append(ackNum)
		print 'seqNum: ' + str(mapTCP['seqNum'])
		print 'msg len: ' + str(len(thisMsg))
        # Only ack to ones with data
		if len(thisMsg) != 0:
			packet = generateTCPPacket(synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
			sendsock.sendto(packet, (destIP , 0 ))
		
		# Repeat the receiving process
		response, addr = nonBlockTransmit(packet, recvsock, 65535, sendsock)
		
		mapIP = decodeIPHeader(response)
		headerIPlen = mapIP['headerLen']*4
		mapTCP = decodeTCPHeader(response[headerIPlen:])
		while checkPacket(response, mapIP, mapTCP, seqNum, ackNum, len(synMsg), sendsock)==false:
			response, addr = nonBlockTransmit(packet, recvsock, 65535, sendsock)
			mapIP = decodeIPHeader(response)
			headerIPlen = mapIP['headerLen']*4
			mapTCP = decodeTCPHeader(response[headerIPlen:])


		headerLength = mapTCP['dataOffSet']+headerIPlen

	# for i in range(len(msg_arr)):
	# 	if i<len(msg_arr)-1:
	# 		if msg_arr[i]<msg_arr[i+1]:
	# 			print true
	# 		else:
	# 			print false
	seqNum = mapTCP['ackNum']
	ackNum = mapTCP['seqNum']+1
	print 'Tearing down connection...'
	if connection_tear_down_by_server(sendsock,recvsock, seqNum, ackNum):
		print 'Connection is disconnected.'
	# '''Receivd fin, tear down connection'''
	# seqNum = mapTCP['ackNum']
	# ackNum = mapTCP['seqNum']+1
	# packet = generateTCPPacket(synMsg, sourceIP, destIP, 'fin,ack', seqNum, ackNum)
	# sendsock.sendto(packet, (destIP , 0 ))
	# response, addr = timeOutRecv(recvsock, 2048)
	# mapIP = decodeIPHeader(response)
	# headerIPlen = mapIP['headerLen']
	# mapTCP = decodeTCPHeader(response[headerIPlen:])
	
	# if mapTCP['ack'] == 1:
	# 	print "receive succceed:", len(receivedMsg)
	
	# # Close sockets
	# sendsock.close()
	# recvsock.close()
	

	return receivedMsg



def get_mac_address(host):
	connection = three_way_handshake(host)

	sendsock = connection[0]
	recvsock = connection[1]
	seqNum = connection[2]
	ackNum = connection[3]

	print 'Tearing down connection...'
	if connection_tear_down_by_client(sendsock,recvsock, seqNum, ackNum):
		print 'Connection is disconnected.'






'''High level operate functions'''
# Handle error
def handleError(msg):
    print "ERROR: ", msg
    sys.exit(0)

# Get file name

################Need to modify!!
def getFileName(url):
	length = len(url)

	slash_index = length-1
	double_slash_index = url.find('//')+1

	for i in range(length-1, 0, -1):
		if url[i]=='/':
			slash_index = i
			break

	if slash_index == length-1 or slash_index==double_slash_index :
		return 'index.html'
	else:
		return url[slash_index+1:]
	# if url[length-1]=='/'
	# 	return 'index.html'
	# if url[length-3:length] == 'php':
	#     index = range(length - 3)
	#     for each in reversed(index):
	#         if url[each] == '/':
	#             return url[each+1:length]
	# else:
	#     return 'index.html'

# Write information into a file
def writeFile(info, fileName):
    output = open(fileName, 'wb')
    output.write(info)
    output.close()

# Get host domain name
def getHost(url):
	# \/\/[^\/]+
    index = 0
    count = 0
    start = 0
    
    for each in url:
        if each == '/':
            count = count + 1
            if count == 2:
                start = index+1
            if count == 3:
                return url[start:index]
        index = index + 1
    if count == 2:
        return url[start:len(url)]
    else:
        return '/'

# Get file path
def getPath(url):
    index = 0
    count = 0

    for each in url:
        if each == '/':
            count = count + 1
            if count == 3:
                return url[index:len(url)]
        index = index + 1
    return '/'

# Form get request
def generateGetRequest(path, host):
    get_request = 'GET '+path+' HTTP/1.1\r\n'\
+'Host: '+ host + '\r\n'\
+'Connection: keep-alive\r\n'\
+'\r\n\r\n'
    print "generated get:", get_request
    return get_request

# # Seperate head and page
# # Seperating using standard \r\n\r\n
# def getHTMLBody(msg):
#     htmlTag = msg.find("\r\n\r\n")
#     return msg[htmlTag:len(msg)]

# # Get response action number
# def getResponseAction(responseMsg):
#     return responseMsg[ACTION_START:ACTION_END]


def handleSendingMsg(msg, host):
    print "handle start"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, PORT))
    sock.send(msg)
#    rescMsg = sock.recv(65536)
    rescMsg = ''
    while 1:
        rescData = sock.recv(8192)
        if not rescData: break
        rescMsg += rescData
    sock.close()
    print "handle end"
    return rescMsg


def parse_result(file_name, content):
	
	extension = file_name[file_name.find('.'):]
	if extension=='.html' or extension=='.php' or extension=='.jsp':
		html_content = re.sub('\\n.{1,4}\\r', '\n\r', content)
		splitPoint = html_content.find('\r\n\r\n\r\n') + 6
		parsed = html_content[splitPoint:]
		return parsed
	# just split from \r\n\r\n
	file_content = content[content.find('\r\n\r\n')+4:]
	return file_content
	# web_page = find('html')!=-1 or find.('php')!=-1 or find.('jsp')!=-1
	# if file_name.find('html')!=-1 or 
	# final_txt = re.sub('\\n.{1,4}\\r', '\n\r', receivedMsg)
	# splitPoint = final_txt.find('\r\n\r\n') + 4
	# parsed = final_txt[splitPoint:]



# http://david.choffnes.com/classes/cs4700sp14/project4.php
# http://david.choffnes.com/classes/cs4700sp14/2MB.log 

'''===Main operation start==='''

SOURCE_PORT = getFreePort()
print "got source port:", SOURCE_PORT

host = ''
path = ''

if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    handleError("Wrong parameter number")



# File name from url
fileName = getFileName(url)
print "fileName", fileName


host = getHost(url)
path = getPath(url)


# get_mac_address(host)
# Construct get message
msg = generateGetRequest(path, host)

# Send and get response using raw socket
response = tcp_transmission(msg, host)
# response = ethernet_transmission(msg,host)

result = parse_result(fileName, response)

# if getResponseAction(response) == OK_MSG:
#     # Html info from the page
#     info = getHTMLBody(response)
# else:
#     handleError("Response action false")

# print "Page Info:", info
# \\n.{1,4}\\r
# Write the file with the info
writeFile(result, fileName)


    








