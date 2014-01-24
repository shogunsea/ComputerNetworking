require 'socket'
#require 'debugger'
 
 # shogunsea/foxmail/aaaaaa
 
 #http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/
host = 'www.google.com'     # The web server
port = 80                           # Default HTTP port
path = "/"                 # The file we want 

# This is the HTTP request we send to fetch a file
request = "GET #{path} HTTP/1.0\r\n\r\n"

socket = TCPSocket.open(host,port)  # Connect to server
socket.print(request)               # Send request
response = socket.read              # Read complete response
# Split response at first blank line into headers and body
p response
#debugger
headers,body = response.split("\r\n\r\n", 2) 

p body    