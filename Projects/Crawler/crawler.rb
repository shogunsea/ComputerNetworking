require 'socket'
require 'uri'
class Crawler
  attr_accessor :port
  attr_accessor :host
  attr_accessor :path
  attr_accessor :socket
  attr_accessor :query
  
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
  
  
  
  
  def initialize
    @host = "cs5700.ccs.neu.edu"     # The web server
    # @host = "google.com"     # The web server
    @port = 80   
    @path = "/"
    @socket = TCPSocket.open(host,port) 
    @query = "GET /accounts/login/?next=/fakebook HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nUser-Agent: HTTPTool/1.0\r\n\r\n"
  end

  def path=(new_path)
    @path = new_path
    @query = "GET #{path} HTTP/1.0\nFrom: someuser@jmarshall.com\nUser-Agent: HTTPTool/1.0\r\n\r\n"
    nil
  end
  
  #method that handle login and session cookie.
  def login(username=nil,password=nil)
    if username&&password
      input="username=#{username}&password=#{password}\r\n\r\n"
    else
      input="
username=001104765&password=ETLHFR62"
    end
    
    login_query = Crawler.post_query+input
    #call post here
    p 'post request looks like:'
    puts login_query
    self.get(login_query)
  end
  
  #post method
  def post
  end
  
  #get method
  def get(request=nil)
    @socket.print(request)
    @socket.read
    #split("\r\n")[0]  
  end 
  
  def update_query
    self.query = "GET #{path} HTTP/1.0\nFrom: someuser@jmarshall.com\nUser-Agent: HTTPTool/1.0\n"
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
