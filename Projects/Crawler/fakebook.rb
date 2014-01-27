# Hello Xiaokang,
# 
# Your login credentials for Fakebook are:
# 
# username: Your NEU ID (with leading zeroes)
# password: ETLHFR62
# new password: 50UK7HD7
# 
# Good luck on the project!
# 
# Christo Wilson
require 'socket'
require 'debugger'
require 'uri'
require './crawler'
# include Socket::Constants
# 
# socket = Socket.new(AF_INET, SOCK_STREAM, 0)
# sockaddr = Socket.sockaddr_in(80, 'www.google.com')
# begin # emulate blocking connect
  # socket.connect_nonblock(sockaddr)
# rescue IO::WaitWritable
  # IO.select(nil, [socket]) # wait 3-way handshake completion
  # begin
    # socket.connect_nonblock(sockaddr) # check connection failure
  # rescue Errno::EISCONN
  # end
# end
# debugger
# socket.write("GET / HTTP/1.0\r\n\r\n")
# results = socket.read
# debugger


tt = "HTTP/1.1 200 OK\r\nDate: Mon, 27 Jan 2014 15:36:41 GMT\r\nServer: Apache/2.2.22 (Ubuntu)\r\nVary: Accept-Language,Co
okie,Accept-Encoding\r\nContent-Language: en-us\r\nSet-Cookie: sessionid=a5084ba028012ac96d7f35b311fa74cd; expires=Mo
n, 10-Feb-2014 15:36:41 GMT; Max-Age=1209600; Path=/\r\nContent-Length: 1192\r\nKeep-Alive: timeout=5, max=100\r\nCon
nection: Keep-Alive\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<html><head><title>Fakebook</title><style TYPE=\"text/css\"><!--\n#pagelist li { display: inline; padding-right: 10px; }\n--></style></head><body><h1>Fakebook</h1><p
><a href=\"/fakebook/\">Home</a></p><hr/><h1>Welcome to Fakebook</h1><p>Get started by browsing some random people's
profiles!</p><ul><li><a href=\"/fakebook/636281627/\">Gol Koll</a></li><li><a href=\"/fakebook/636472562/\">Quinton W
itaszek</a></li><li><a href=\"/fakebook/636531421/\">Patricia Alicer</a></li><li><a href=\"/fakebook/637560261/\">Del
oris Lamik</a></li><li><a href=\"/fakebook/638078584/\">Pazu Nadutt</a></li><li><a href=\"/fakebook/638188865/\">Jero
my Kilogan</a></li><li><a href=\"/fakebook/638480522/\">Zezerofibo Mishveladze</a></li><li><a href=\"/fakebook/639051
328/\">Daxi Fesid</a></li><li><a href=\"/fakebook/639491321/\">Xofelehi Mccouch</a></li><li><a href=\"/fakebook/63971
9376/\">Rat Starel</a></li></ul><h6>Fakebook is run by <a href=\"http://www.ccs.neu.edu/home/cbw/\">Christo Wilson</a
> at                        \n<a href=\"http://www.northeastern.edu\">NEU</a>. It is meant for educational purposes o
nly.                       \nFor questions, contact <a href=\"mailto:cbw@ccs.neu.edu\">Christo Wilson</a></h6></body>
</html>\n"



 # shogunsea/foxmail/aaaaaa
 a = Crawler.new
 debugger
 socket = Socket.new(:INET, :STREAM,0)
 sockaddr = Socket.pack_sockaddr_in( 80, 'cs5700.ccs.neu.edu' )
 socket.connect( sockaddr )
 debugger
 socket.write( "GET / HTTP/1.0\r\n\r\n")
 results = socket.read
 # sock.connect(('agentx.ccs.neu.edu', 27993))  
# sock.send('cs5700spring2013 HELLO 001105928\n')  
# print sock.recv(1024)  
 
 debugger
 p 's'
 
p 'ss'
 
 
 
 
 
 
#  
 # #http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/
# host = 'cs5700.ccs.neu.edu'     # The web server
# port = 80                           # Default HTTP port
# # path = "/fakebook/10953923"                 # The file we want 
# path = "/"
# login = "/accounts/login/?next=/fakebook"
# # This is the HTTP request we send to fetch a file
# request = "GET #{login} HTTP/1.0\r\n\r\n"
# debugger
# socket = TCPSocket.open(host,port)  # Connect to server
# debugger
# socket.print(request)               # Send request
# response = socket.read     
# 
# # response.split(/\r\n/)[0]     HTTP response header!!!
         # # Read complete response
# # Split response at first blank line into headers and body
# puts response
# 
# uri = URI("http://www.ccs.neu.edu/home/cbw/")
# debugger 
# p 's'

