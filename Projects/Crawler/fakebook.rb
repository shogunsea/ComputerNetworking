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
require './crawler'

 a = Crawler.new
 
 tt = ">FLAG: 6cbc16569e9321908f6268692e567e8ebdb053aca633f0ded431c7860a2839b2</h2><h2>Basic Information</h2><ul><li>Sex: Female</li><li>Hometown: Woburn</li></ul><h2>Personal Information</h2><ul></ul><h2>Friends</h2><p><a href=\"/fakebook/231843152/friends/1/\">View Jere Lestrange's friends</a></p><h2>Wall</h2>"
 ff = "HTTP/1.1 200 OK\r\nDate: Mon, 27 Jan 2014 20:48:10 GMT\r\nServer: Apache/2.2.22 (Ubuntu)\r\nVary: Accept-Language,Co
okie,Accept-Encoding\r\nContent-Language: en-us\r\nContent-Length: 861\r\nKeep-Alive: timeout=5, max=100\r\nConnectio
n: Keep-Alive\r\nContent-Type: text/html; charset=utf-8"
 
 debugger
 # a.crawl
 p 'ss'
 # debugger
 
 
 
 
 
 
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

