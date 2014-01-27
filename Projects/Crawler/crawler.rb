require 'socket'
class Crawler
  attr_accessor :port,:host,:path,:socket,:query,:login_query,:cookie,:login_session, :login_query
  
  def initialize
    @host = "cs5700.ccs.neu.edu"     # The web server
    @port = 80   
    @path = "/"
    @socket = TCPSocket.open(host,port)
    @login_query = "GET /accounts/login/?next=/fakebook HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nConnection:keep-alive\nUser-Agent: HTTPTool/1.0\r\n\r\n"
    @query = "GET /fakebook HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nConnection: keep-alive\nUser-Agent: HTTPTool/1.0\r\n\r\n"
  end

  def path=(new_path)
    @path = new_path
    @query.gsub!(/\/fakebook/, new_path)
  end
  
  def update_session(cookie)
    @query = "GET /fakebook/ HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nCookie: csrftoken=#{cookie[:csrf]}; sessionid=#{login_session}\nReferer: http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/\nConnection: keep-alive\nUser-Agent: HTTPTool/1.0\r\n\r\n"
  end
  
  def get_cookie
    response = get login_query
    csrf = response.scan(/csrftoken=\w*/).first.split("=")[1]
    session_id = response.scan(/sessionid=\w+/).first.split("=")[1]
    @cookie={:csrf=>csrf,:session_id=>session_id}
  end
  
  def flush
    @socket = TCPSocket.open(host,port) 
  end
  
  #login method, through post request, will return new sessionid
  def login(username=nil,password=nil)
    cookie = get_cookie
    if username&&password
      input="csrfmiddlewaretoken=#{cookie[:csrf]}&username=#{username}&password=#{password}&next=%2Ffakebook%2F"
    else
      input="csrfmiddlewaretoken=#{cookie[:csrf]}&username=001104765&password=50UK7HD7&next=%2Ffakebook%2F"
    end
    post_query = get_post_query(input.length,cookie[:csrf],cookie[:session_id])
    login_query = post_query+input
    response = get(login_query)
    @login_session = response.scan(/sessionid=\w+/).first.split("=")[1] 
  end   
  
  def crawl
    #success, can login and get 302 found response so far, and can get the session id after logedin.
    new_session_id = login 
    #get index page with new session id
    update_session(cookie)
    
    secreat_flags = bfs(query)
    
    puts secreat_flags
    
  end
  
  
  def bfs(query)
    queue = Queue.new
    track = {}
    track[url] = 1#dummy value
    queue<<query # root node
    secreat_flags = []
    
    while !queue.empty?
      current_url = queue.pop
      path = current_url
      
      current_response = get(query)
      
      adjcent_urls = parse_html(current_response)
      
      unless adjcent_urls.nil?
        adjacent_urls.each do |url|
          if track[url].nil?
            track[url] = 1
            queue<<url
            
            
          end
          
        
        end
        
      end
      
      
      
      
      
      
    end
    
    
    
    
    
    
    
    return []
  end
  
  
  
  #get method
  def get(request=nil)
    flush
    @socket.write request
    response= @socket.recv(10000000)#read method take soooooo long.
    #split("\r\n")[0]  
  end 
  
  def get_post_query(length,csrf,sessionid)
    @login_query = "POST /accounts/login/?next=/fakebook HTTP/1.0\nHost: cs5700.ccs.neu.edu\nFrom: shogunx@ccs.neu.edu\nReferer: http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/\nUser-Agent: HTTPTool/1.0\nContent-Type: application/x-www-form-urlencoded\nContent-Length: #{length}\nCookie: csrftoken=#{csrf}; sessionid=#{sessionid}\r\n\r\n"
    # query = "GET #{path} HTTP/1.0\nFrom: someuser@jmarshall.com\nUser-Agent: HTTPTool/1.0\n"
  end
  
  
  #BFS crawler. return secret flag found.
  # def 
  
  
  #method to parse html content, will return all valid url under 'cs5700.ccs.neu.edu' domain
  def parse_html(html)
    urls = html.scan(/\/fakebook\/\d+/)
  end
  
end


