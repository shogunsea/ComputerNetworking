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
# sudo python rawhttpget.py http://www.ccs.neu.edu

PORT = 80
sourceIP = ''
destIP = ''
ip_id_global = 0
false = 0
true = 1


def check_sum(msg):
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
def get_port():
	sPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sPort.bind(("",0))
	sPort.listen(1)
	port = sPort.getsockname()[1]
	sPort.close()
	return port

def get_local_up(host):
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
def generate_ip_packet(msg, sourceIP, destIP):
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
	# return generate
	return packet

# Generate the packet with TCP and IP header
def generate_tcp_packet(send_sock_type, msg, sourceIP, destIP, flag, seqNum, ackNum):
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
	# Construct pseudo header
    sourceAddress = socket.inet_aton(sourceIP)
    destAddress = socket.inet_aton(destIP)
    placeHolder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header) + len(msg)
    
    pseudoHeader = pack('!4s4sBBH' , sourceAddress , destAddress , placeHolder , protocol , tcp_length);
    pseudoHeader = pseudoHeader + tcp_header + msg
    
    # Calculate checksum
    tcp_checksum = check_sum(pseudoHeader)
    
    # Assemble TCP header in order
    tcp_header = pack('!HHLLBBH' , tcp_sourcePort, tcp_destPort, tcp_seqNum, tcp_ackNum, tcp_dataOffSet_reserve, tcp_flags,  tcp_window) + pack('H', tcp_checksum) + pack('!H', tcp_urgPointer)
    
    packet = tcp_header + msg
	
	# Add IP header and return
    return generate_ip_packet(packet, sourceIP, destIP)

def validate_ethernet_header(ethernet_dict):
	global LocalMac
	global RemoteMac
	if ethernet_dict['local_mac']!=LocalMac:
		return false
	elif ethernet_dict['remote_mac']!=RemoteMac:
		return false
	return true


def decode_ethernet_packet(packet):
	eth_length = 14
	eth_header = packet[:eth_length]
	eth = unpack('!6s6sH' , eth_header)
	eth_protocol = socket.ntohs(eth[2])
	print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)



# Decode IP header and store in a map
def decode_ip_packet(packet):
    ip_header = packet[0:20]
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

    packet_dict = {}
    packet_dict["version"] = version
    packet_dict["headerLen"] = ihl
    packet_dict["totalLen"] = iph_length
    packet_dict["ttl"] = ttl
    packet_dict["protocol"] = protocol
    packet_dict["sourceIP"] = s_addr
    packet_dict["destIP"] = d_addr
    return packet_dict

def decode_tcp_packet(packet_long):
    packet = packet_long#[20:]
    packet_dict = {}
    packet_dict["sourcePort"] = (int(ord(packet[0])<<8))+(int(ord(packet[1])))
    packet_dict["destPort"] = (int(ord(packet[2])<<8))+(int(ord(packet[3])))
    packet_dict["seqNum"] =(int(ord(packet[4])<<24))+(int(ord(packet[5])<<16))+(int(ord(packet[6])<<8))+(int(ord(packet[7])))
    packet_dict["ackNum"] = (int(ord(packet[8])<<24))+(int(ord(packet[9])<<16))+(int(ord(packet[10])<<8))+(int(ord(packet[11])))
    packet_dict["dataOffSet"] = ((int(ord(packet[12])) & 0xF0)>>4)<<2
    packet_dict["urg"] = int(ord(packet[13]) & 0x20)>>5
    packet_dict["ack"] = int(ord(packet[13]) & 0x10)>>4
    packet_dict["psh"] = int(ord(packet[13]) & 0x8)>>3
    packet_dict["rst"] = int(ord(packet[13]) & 0x4)>>2
    packet_dict["syn"] = int(ord(packet[13]) & 0x2)>>1
    packet_dict["fin"] = int(ord(packet[13]) & 0x1)
    packet_dict["window"] = int(ord(packet[14])<<8)+int(ord(packet[15]))
    packet_dict["checksum"] = int(ord(packet[16])<<8)+int(ord(packet[17]))
    packet_dict["urgPointer"] = int(ord(packet[18])<<8)+int(ord(packet[19]))
    packet_dict["data"] = packet[packet_dict["dataOffSet"]:]
    # 
    return packet_dict
    
#Check IP Header
def check_ip_packet(packet, ip_dict, destIP):
	if destIP != ip_dict['sourceIP']:
		print "Ip mismatch."
		return false
	if 6 != ip_dict['protocol']:
		print "Protocol type mismatch."
		return false
	return true

#Check TCP header
def check_tcp_packet(packet, tcp_dict, seqNum, ackNum, msgLen):
	# print 'checking tcp header...'
	if tcp_dict['destPort']!=SOURCE_PORT:
		print 'Port number mismatch.'
	if (seqNum + msgLen) != tcp_dict['ackNum']:
		print 'SeqNum mismatch.'
		return false
	if ackNum != tcp_dict['seqNum']:
		if tcp_dict.get('syn') != 1 and tcp_dict.get('ack') == 1:
			print "AckNum mismatch."
			return false
	return true

def check_packet(packet, ip_dict, tcp_dict, sentSeq, sentAck, sentMsgLen, send_sock):
	# print "Validating Packet..."
	headerIPlen = ip_dict['headerLen']*4
	packetTCP = packet[headerIPlen:]
	packetIP = packet[0:headerIPlen]
	# print 'sent ack: '+ str(sentAck)
	# print 'sent seqNum: '+str(sentSeq)+' parsed seqNum: '+str(tcp_dict['seqNum'])
	tcp_validation = check_tcp_packet(packetTCP, tcp_dict, sentSeq, sentAck, sentMsgLen)
	ip_validation = check_ip_packet(packetIP, ip_dict, destIP)
	if not tcp_validation or not ip_validation:
		# if not tcp_validation:
		# 	print tcp_validation
		# 	print 'TCP header fails.'
		# if not ip_validation:
		# 	print ip_validation
		# 	print 'IP header fails.'

		# print 'errrrrrr'
		return false
	return true

#Handle ack time out
def time_out_recev(recv_sock_type,recv_sock, size):

	print recv_sock_type
	timeout = 60
	ready = select.select([recv_sock], [], [], timeout)
	if ready[0]:
		# don't need to validate tcp packet here
		if recv_sock_type=='ip':
			response = recv_sock.recvfrom(size)
			return response
		elif recv_sock_type=='ethernet':
			response = recv_sock.recvfrom(size)
			return response

	else:
		print "Time out! Retransmit"
		return false
	# return (tcp_frame, response[1])
	# return response

def transmit(recv_sock_type, packet, recv_sock, size, send_sock):
	response = time_out_recev(recv_sock_type, recv_sock, size)

	i = 0
	while not response:
		send_sock.sendto(packet, (destIP , 0 ))
		i = i + 1
		if i == 5:
			handleError("3 Transmission Connection failure")
			break;
		response = time_out_recev(recv_sock_type,recv_sock, size)
	
	return response

#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
  return b

def three_way_handshake(host, send_sock_type, recv_sock_type):
	global sourceIP
	global destIP
	sourceIP = socket.gethostbyname(socket.gethostname())#Get local IP
	# If falsed by hosts file use another method
	if sourceIP[0:3] == '127':
		sourceIP = get_local_up(host)
	destIP= socket.gethostbyname(host)
	# Create two raw sockets, one for sending and one for receiving
	try:
		if send_sock_type=='ip':
			send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
		elif send_sock_type=='ethernet':
			send_sock = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
	except socket.error , msg:
		handleError("Sending socket could not be created. " + str(msg[0]) + " " + msg[1])
	# Receiving socket is created in IPPROTO_TCP which could receive both IP and TCP headers
	try:
		if recv_sock_type=='ip':
			recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
		elif recv_sock_type=='ethernet':
			recv_sock = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
	except socket.error , msg:
		handleError("Receiving socket could not be created. " + str(msg[0]) + " " + msg[1])
	


	# 
	synMsg = ''
	seqNum = 4321 # Starting seq number
	ackNum = 0
	packet = generate_tcp_packet(send_sock_type, synMsg, sourceIP, destIP, 'syn', seqNum, ackNum)
	# First syn handshake
	send_sock.sendto(packet, (destIP , 0 ))
	response, addr =  transmit(recv_sock_type, packet, recv_sock, 2048, send_sock)
	# 
	ip_dict = decode_ip_packet(response)
	headerIPlen = ip_dict['headerLen']*4
	tcp_dict = decode_tcp_packet(response[headerIPlen:])#headerIPlen*4!?
	# tcp_dict = decode_tcp_packet(response)
	#Validate packet
	while check_packet(response, ip_dict, tcp_dict, seqNum, ackNum, 1, send_sock)==false:
		response, addr =  transmit(recv_sock_type, packet, recv_sock, 2048, send_sock)
		ip_dict = decode_ip_packet(response)
		headerIPlen = ip_dict['headerLen']*4
		# 
		tcp_dict = decode_tcp_packet(response[headerIPlen:])#headerIPlen*4!?

	# print "Connection established?????????"
	if tcp_dict.get('syn') == 1 and tcp_dict.get('ack') == 1:
		seqNum = tcp_dict['ackNum']
		ackNum = tcp_dict['seqNum']+1
		packet = generate_tcp_packet(send_sock_type, synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
		send_sock.sendto(packet, (destIP , 0 ))
	#Handshake end, connection established
	return [send_sock, recv_sock, seqNum, ackNum]

def connection_tear_down_by_server(send_sock_type, recv_sock_type,send_sock, recv_sock, seqNum, ackNum):
	'''Receivd fin, tear down connection'''
	synMsg = ''
	packet = generate_tcp_packet(send_sock_type, synMsg, sourceIP, destIP, 'fin,ack', seqNum, ackNum)
	send_sock.sendto(packet, (destIP , 0 ))
	response, addr = time_out_recev(recv_sock_type,recv_sock, 2048)
	ip_dict = decode_ip_packet(response)
	headerIPlen = ip_dict['headerLen']
	tcp_dict = decode_tcp_packet(response[headerIPlen:])
	if tcp_dict['ack'] == 1:
		print "receive succceed:", len(receivedMsg)
	# Close sockets
	send_sock.close()
	recv_sock.close()
	return true

def connection_tear_down_by_client(send_sock, recv_sock, seqNum, ackNum):
	synMsg = ''
	packet = generate_tcp_packet(send_sock_type, synMsg, sourceIP, destIP, 'fin,ack', seqNum, ackNum)
	send_sock.sendto(packet, (destIP , 0 ))
	response, addr = transmit(recv_sock_type, packet, recv_sock, 65535, send_sock)
	ip_dict = decode_ip_packet(response)
	headerIPlen = ip_dict['headerLen']*4
	tcp_dict = decode_tcp_packet(response[headerIPlen:])
	# print 'tcp_dict fin:' + str(tcp_dict['fin'])
	i = 0
	while tcp_dict['fin']!=1:
		response, addr = transmit(recv_sock_type, packet, recv_sock, 65535, send_sock)
		ip_dict = decode_ip_packet(response)
		headerIPlen = ip_dict['headerLen']*4
		tcp_dict = decode_tcp_packet(response[headerIPlen:])
		print 'tcp_dict fin:' + str(tcp_dict['fin'])
		print tcp_dict['fin']!=1
		if i>30:#receive at most 30 promiscuous packets, then force to close down
			break

	seqNum = tcp_dict['ackNum']
	ackNum = tcp_dict['seqNum']+1
	packet = generate_tcp_packet(send_sock_type, synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
	send_sock.sendto(packet, (destIP , 0 ))
	# Close sockets
	send_sock.close()
	recv_sock.close()
	return true

def tcp_transmission(msg, host):
	global sourceIP
	global destIP

	send_sock_type = 'ip'
	recv_sock_type = 'ip'
	# recv_sock_type = 'ethernet'
	
	connection = three_way_handshake(host, send_sock_type, recv_sock_type)

	send_sock = connection[0]
	recv_sock = connection[1]
	seqNum = connection[2]
	ackNum = connection[3]

	print 'Connection established, starting to recevie...'
	
	receivedMsg = ''
	synMsg = ''
    # Assemble the message packet
	packet = generate_tcp_packet(send_sock_type, msg, sourceIP, destIP, 'ack', seqNum, ackNum)
    # Send the packet 
	send_sock.sendto(packet, (destIP , 0 ))
    # Receive with the time out control method
	response, addr = transmit(recv_sock_type, packet, recv_sock, 2048, send_sock)

    # Decode IP header
	ip_dict = decode_ip_packet(response)
	headerIPlen = ip_dict['headerLen']*4
    # Decode TCP header
	tcp_dict = decode_tcp_packet(response[headerIPlen:])
	
    # Check the packet in various aspects
	while check_packet(response, ip_dict, tcp_dict, seqNum, ackNum, len(msg), send_sock) == false:
		response, addr = transmit(recv_sock_type, packet, recv_sock, 2048, send_sock)
	    # Decode IP header
		ip_dict = decode_ip_packet(response)
		headerIPlen = ip_dict['headerLen']*4
	    # Decode TCP header
		tcp_dict = decode_tcp_packet(response[headerIPlen:])
    # Get the header total length
	headerLength = tcp_dict['dataOffSet']+headerIPlen
	msg_dict = {}
	msg_arr = []

	

    # Assemble and receive the remain message in a loop
	while tcp_dict['ack'] == 1 and tcp_dict['fin'] == 0:
		# Get the data and assemble
		thisMsg = response[headerLength:]
		receivedMsg = receivedMsg + thisMsg
        # Get the next seq and ack
		seqNum = tcp_dict['ackNum']
		ackNum = tcp_dict['seqNum']+len(thisMsg)

		msg_dict[ackNum] = thisMsg
		msg_arr.append(ackNum)
		# print 'seqNum: ' + str(tcp_dict['seqNum'])
		# print 'msg len: ' + str(len(thisMsg))
        # Only ack to ones with data
		if len(thisMsg) != 0:
			packet = generate_tcp_packet(send_sock_type, synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
			send_sock.sendto(packet, (destIP , 0 ))
		
		# Repeat the receiving process
		response, addr = transmit(recv_sock_type, packet, recv_sock, 65535, send_sock)
		
		ip_dict = decode_ip_packet(response)
		headerIPlen = ip_dict['headerLen']*4
		tcp_dict = decode_tcp_packet(response[headerIPlen:])
		

		while check_packet(response, ip_dict, tcp_dict, seqNum, ackNum, len(synMsg), send_sock)==false:
			response, addr = transmit(recv_sock_type, packet, recv_sock, 65535, send_sock)
			ip_dict = decode_ip_packet(response)
			headerIPlen = ip_dict['headerLen']*4
			tcp_dict = decode_tcp_packet(response[headerIPlen:])

		headerLength = tcp_dict['dataOffSet']+headerIPlen

	

	seqNum = tcp_dict['ackNum']
	ackNum = tcp_dict['seqNum']+1
	print 'Transmission finished.'
	print 'Tearing down connection...'
	if connection_tear_down_by_server(send_sock_type, recv_sock_type,send_sock,recv_sock, seqNum, ackNum):
		print 'Connection is disconnected.'
	print 'Receivd '+ str(len(receivedMsg)) + 'bytes data.'
	return receivedMsg


def ethernet_transmission(msg, host):
	global sourceIP
	global destIP
	mac_address = get_mac_address(host)
	connection = three_way_handshake(host, 'ethernet', 'ethernet')
	send_sock = connection[0]
	recv_sock = connection[1]
	seqNum = connection[2]
	ackNum = connection[3]

	print 'Established! Starting to receive!!!!!!'
	'''Send the message and receive'''
	#Initiated receive string
	receivedMsg = ''
	synMsg = ''
    # Assemble the message packet
	packet = generate_tcp_packet(send_sock_type, msg, sourceIP, destIP, 'ack', seqNum, ackNum)
    # Send the packet 
	send_sock.sendto(packet, (destIP , 0 ))
    # Receive with the time out control method
	response, addr = transmit(recv_sock_type, packet, recv_sock, 2048, send_sock)
    # Decode IP header
	ip_dict = decode_ip_packet(response)
	headerIPlen = ip_dict['headerLen']*4
    # Decode TCP header
	tcp_dict = decode_tcp_packet(response[headerIPlen:])
    # Check the packet in various aspects
	while check_packet(response, ip_dict, tcp_dict, seqNum, ackNum, len(msg), send_sock) == false:
		response, addr = transmit(recv_sock_type, packet, recv_sock, 2048, send_sock)
	    # Decode IP header
		
		ip_dict = decode_ip_packet(response)
		headerIPlen = ip_dict['headerLen']*4
	    # Decode TCP header
		tcp_dict = decode_tcp_packet(response[headerIPlen:])
    # Get the header total length
	headerLength = tcp_dict['dataOffSet']+headerIPlen
	msg_dict = {}
	msg_arr = []
    # Assemble and receive the remain message in a loop
	while tcp_dict['ack'] == 1 and tcp_dict['fin'] == 0:
		# Get the data and assemble
		thisMsg = response[headerLength:]
		receivedMsg = receivedMsg + thisMsg
        # Get the next seq and ack
		seqNum = tcp_dict['ackNum']
		ackNum = tcp_dict['seqNum']+len(thisMsg)
		msg_dict[ackNum] = thisMsg
		msg_arr.append(ackNum)
		print 'seqNum: ' + str(tcp_dict['seqNum'])
		print 'msg len: ' + str(len(thisMsg))
        # Only ack to ones with data
		if len(thisMsg) != 0:
			packet = generate_tcp_packet(send_sock_type, synMsg, sourceIP, destIP, 'ack', seqNum, ackNum)
			send_sock.sendto(packet, (destIP , 0 ))
		
		# Repeat the receiving process
		response, addr = transmit(recv_sock_type, packet, recv_sock, 65535, send_sock)
		
		ip_dict = decode_ip_packet(response)
		headerIPlen = ip_dict['headerLen']*4
		tcp_dict = decode_tcp_packet(response[headerIPlen:])
		while check_packet(response, ip_dict, tcp_dict, seqNum, ackNum, len(synMsg), send_sock)==false:
			response, addr = transmit(recv_sock_type, packet, recv_sock, 65535, send_sock)
			ip_dict = decode_ip_packet(response)
			headerIPlen = ip_dict['headerLen']*4
			tcp_dict = decode_tcp_packet(response[headerIPlen:])


		headerLength = tcp_dict['dataOffSet']+headerIPlen
	seqNum = tcp_dict['ackNum']
	ackNum = tcp_dict['seqNum']+1
	print 'Tearing down connection...'
	if connection_tear_down_by_server(send_sock_type,send_sock,recv_sock, seqNum, ackNum):
		print 'Connection is disconnected.'
	return receivedMsg



def get_mac_address(host):
	global LocalMac
	global RemoteMac

	sourceIP = socket.gethostbyname(socket.gethostname())#Get local IP
	# If falsed by hosts file use another method
	if sourceIP[0:3] == '127':
		sourceIP = get_local_up(host)
	destIP= socket.gethostbyname(host)
	# Create two raw sockets, one for sending and one for receiving
	try:
		send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error , msg:
		handleError("Sending socket could not be created. " + str(msg[0]) + " " + msg[1])
	# Receiving socket is created in IPPROTO_TCP which could receive both IP and TCP headers
	try:
		recv_sock = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
	except socket.error , msg:
		handleError("Receiving socket could not be created. " + str(msg[0]) + " " + msg[1])

	synMsg = ''
	seqNum = 4321 # Starting seq number
	ackNum = 0
	packet = generate_tcp_packet('ip', synMsg, sourceIP, destIP, 'syn', seqNum, ackNum)
	# First syn handshake
	send_sock.sendto(packet, (destIP , 0 ))

	response, addr = time_out_recev('ethernet', recv_sock, 2048)

	ip_packet = response[14:]
	ip_dict = decode_ip_packet(ip_packet)
	tcp_packet = response[34:]
	tcp_dict = decode_tcp_packet(tcp_packet)
	# while check_packet(ip_packet, ip_dict, tcp_dict, seqNum, ackNum, 1, send_sock)
# (packet, ip_dict, tcp_dict, sentSeq, sentAck, sentMsgLen, send_sock):
	pdb.set_trace()


	connection = three_way_handshake(host, 'ip', 'ethernet')
	send_sock = connection[0]
	recv_sock = connection[1]
	seqNum = connection[2]
	ackNum = connection[3]


	LocalMac = connection[4]
	RemoteMac = connection[5]


	print 'Tearing down connection...'
	if connection_tear_down_by_client(send_sock,recv_sock, seqNum, ackNum):
		print 'Connection is disconnected.'
	return [local_mac, remote_mac]


# Handle error
def handleError(msg):
    print "ERROR: ", msg
    sys.exit(0)


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
def get_request(path, host):
	get_request = 'GET '+path+' HTTP/1.1\r\n'\
	+'Host: '+ host + '\r\n'\
	+'Connection: keep-alive\r\n'\
	+'\r\n\r\n'
	# +'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0'\
	# +'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'\
	# +'Accept-Language: en-US,en;q=0.5'\
	# +'Accept-Encoding: gzip, deflate'\
	# +'Cookie: __utma=135809699.960683796.1395449745.1395613813.1395781399.8; __utmz=135809699.1395449745.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmb=135809699.1.10.1395781399; __utmc=135809699'\
	return get_request

def parse_result(file_name, content):
	
	extension = file_name[file_name.find('.'):]
	if extension=='.html' or extension=='.php' or extension=='.jsp':
		html_content = re.sub('\\n.{1,4}\\r', '\n\r', content)
		splitPoint = html_content.find('\r\n\r\n\r\n') + 6
		parsed = html_content[splitPoint:]
		ending = parsed.find('</html>')
		return parsed[0:ending+7]
	# just split from \r\n\r\n
	file_content = content[content.find('\r\n\r\n')+4:]

	return file_content


SOURCE_PORT = get_port()
print "Source port:", SOURCE_PORT


if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    handleError("Wrong parameter number")

fileName = getFileName(url)
print "fileName", fileName

host = getHost(url)
path = getPath(url)

LocalMac = ''
RemoteMac = ''

get_mac_address(host)



# # Construct get message
# msg = get_request(path, host)

# # Send and get response using raw socket
# response = tcp_transmission(msg, host)
# # response = ethernet_transmission(msg,host)
# result = parse_result(fileName, response)

# # print 'Receivd '+ str(len(result)) + 'bytes data.'

# writeFile(result, fileName)