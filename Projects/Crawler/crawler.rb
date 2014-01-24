require 'socket'
require 'uri'
# require 'debugger'
class Crawler
  attr_accessor :port
  attr_accessor :host
  attr_accessor :path
  attr_accessor :socket
  attr_accessor :query
  attr_accessor :login_query
  attr_accessor :cookie
  attr_accessor :login_session
  
  # @host = 'cs5700.ccs.neu.edu'     # The web server
  # @port = 80   
  # @path = '/'
  # @socket 
  #the login query
  @@post_query = "POST /accounts/login/?next=/fakebook HTTP/1.0\nHost: cs5700.ccs.neu.edu\nFrom: shogunx@ccs.neu.edu\nReferer: http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/\nUser-Agent: HTTPTool/1.0\nContent-Type: application/x-www-form-urlencoded\nContent-Length: 56\r\n"
  
  
 # @@post_query= "POST /accounts/login/ HTTP/1.1
# Host: cs5700.ccs.neu.edu
# Connection: keep-alive
# Content-Length: 109
# User-Agent: HTTPTool/1.0
# Content-Type: application/x-www-form-urlencoded
# Referer: http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/
# 
# username=001104765&password=ETLHFR62"
  
  #csrfmiddlewaretoken
  
  
  def initialize
    @host = "cs5700.ccs.neu.edu"     # The web server
    # @host = "google.com"     # The web server
    @port = 80   
    @path = "/"
    @socket = TCPSocket.open(host,port)
    # @socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_KEEPALIVE, true)
    @login_query = "GET /accounts/login/?next=/fakebook HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nConnection:keep-alive\nUser-Agent: HTTPTool/1.0\r\n\r\n"
    @query = "GET /fakebook HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nConnection: keep-alive\nUser-Agent: HTTPTool/1.0\r\n\r\n"
  end

  def path=(new_path)
    @path = new_path
    @query = "GET #{path} HTTP/1.0\nFrom: someuser@jmarshall.com\nUser-Agent: HTTPTool/1.0\r\n\r\n"
    nil
  end
  
  def update_query(cookie)
    @query = "GET /fakebook HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nCookie: csrftoken=#{cookie[:csrf]}; sessionid=#{self.login_session}\nConnection: keep-alive\nUser-Agent: HTTPTool/1.0\r\n\r\n"
  end
  
  def get_cookie
    response = self.get self.login_query
    # debugger
    csrf = response.scan(/csrftoken=\w*/).first.split("=")[1]
    session_id = response.scan(/sessionid=\w+/).first.split("=")[1]
    
    @cookie={:csrf=>csrf,:session_id=>session_id}
  end
  
  def flush
    @socket = TCPSocket.open(self.host,self.port) 
  end
  
  #method that handle login and session cookie.
  def login(username=nil,password=nil)
    cookie = get_cookie
    if username&&password
      input="username=#{username}&password=#{password}\r\n\r\n"
    else
      input="csrfmiddlewaretoken=#{cookie[:csrf]}&username=001104765&password=ETLHFR62&next=%2Ffakebook%2F"
    end
    self.get_post_query input.length,cookie[:csrf],cookie[:session_id]
    
    login_query = Crawler.post_query+input
    #call post here
    p 'post request looks like:'
    puts login_query
    response = self.get(login_query)
    if response
      @login_session = response.scan(/sessionid=\w+/).first.split("=")[1] 
      return @login_session
    else
      p 'response is nil, dont know why'
    end
    
  end
  
  
  def crawl
    #success, can login and get 302 found response so far, and can get the session id after logedin.
    self.login
    #use sever returned session id to update the get query, no problem.
    self.update_query(self.cookie)
    
    #try to get the index page, get 301 error right now.
    self.get self.query
    
    
    
    
    
  end
  
  #post method
  def post
  end
  
  #get method
  def get(request=nil)
    self.flush
    @socket.write request
    response= @socket.read#read method take soooooo long.
    #split("\r\n")[0]  
  end 
  
  def get_post_query(length,csrf,sessionid)
    @@post_query = "POST /accounts/login/?next=/fakebook HTTP/1.0\nHost: cs5700.ccs.neu.edu\nFrom: shogunx@ccs.neu.edu\nReferer: http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/\nUser-Agent: HTTPTool/1.0\nContent-Type: application/x-www-form-urlencoded\nContent-Length: #{length}\nCookie: csrftoken=#{csrf}; sessionid=#{sessionid}\r\n\r\n"
    # self.query = "GET #{path} HTTP/1.0\nFrom: someuser@jmarshall.com\nUser-Agent: HTTPTool/1.0\n"
  end
  
  def self.post_query
    @@post_query
  end

  # def test
    # @socket.print("GET / HTTP/1.0\nFrom: someuser@jmarshall.com\nUser-Agent: HTTPTool/1.0\r\n\r\n")
    # @socket.read
  # end
#   
    
  
end



# require 'net/http'
# #require 'debugger'
# 
# ARGV.each do |a|
  # p a
# end
# 
# 
# 
# uri = URI('http://example.com/index.html')
# # debugger
# params = { :limit => 10, :page => 3 }
# uri.query = URI.encode_www_form(params)
# # debugger
# 
# res = Net::HTTP.get_response(uri)
# # debugger
# puts res.body if res.is_a?(Net::HTTPSuccess)
# 
# 
# 
# require 'socket'
# 
# host = 'www.google.com'
# port = 80
# 
# s = TCPSocket.open host, port
# s.puts "GET / HTTP/1.1\r\n"
# s.puts "\r\n"
# 
# # while line = s.gets
  # # puts line.chop
# # end
# a = s.read
# p a
# 
# s.close
