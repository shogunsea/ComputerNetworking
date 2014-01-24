require 'socket'
require 'debugger'
require 'uri'
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
debugger
matched = "<ul><li><a href=\"/fakebook/14105395/\">Rubere Zbaban</a></li><li><a href=\"/fakebook/19821562/\">Dopixaruno Sopunn</a></li><li><a href=\"/fakebook/55612647/\">Vepiga Bizell</a></li><li><a href=\"/fakebook/82787254/\">Carey Margaret</a></li><li><a href=\"/fakebook/90740453/\">Repolu Demaria</a></li><li><a href=\"/fakebook/152003634/\">Edmundo Balow</a></li><li><a href=\"/fakebook/205004985/\">Vadu Geputt</a></li><li><a href=\"/fakebook/206808854/\">Vogavu Kagesaki</a></li><li><a href=\"/fakebook/229922728/\">Genna Waddel</a></li><li><a href=\"/fakebook/265184668/\">Macie Fischang</a></li><li><a href=\"/fakebook/268584905/\">Alexandre Ridun</a></li><li><a href=\"/fakebook/305994363/\">Lenovuruca Renaud</a></li><li><a href=\"/fakebook/316680775/\">Tusecela Nedunn</a></li><li><a href=\"/fakebook/326186344/\">Tel Zbipinn</a></li><li><a href=\"/fakebook/351130560/\">Levatu Zusak</a></li><li><a href=\"/fakebook/353925234/\">Gabriele Neglio</a></li><li><a href=\"/fakebook/357923406/\">Walton Ariail</a></li><li><a href=\"/fakebook/411354445/\">Zefuhefa Nomil</a></li><li><a href=\"/fakebook/412385680/\">Rigefo Neroc</a></li><li><a href=\"/fakebook/414531792/\">Myrtie Cotheran</a></li></ul>"
a = URI.extract body
b =  URI.extract(body, ['http', 'https'])
# d =  URI.extract(c, ['http', 'https'])
# e =  URI.extract(c)

split_test = matched.scan(/"\/.{10,30}\/"/) 

debugger
p 'ss'
