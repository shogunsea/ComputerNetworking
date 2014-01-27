require 'socket'
require 'thread'

# 6cbc16569e9321908f6268692e567e8ebdb053aca633f0ded431c7860a2839b2
# f03e6e05c72b77f56bbf5d6df286e0776392bf7dd45b7331d800690a8f41d2b8
# 27c11a054ef0047161e1ab9c2914c42efee4cc3b4edc810477c12411a1441b82
# ec5f21341c52fcb91fc84b2c9eda6c1670cd7fa9d203ec4b1255ab4346bff9f0
# 777227fd95751358e447178ea11d0c588b9ef6d39a7e17a43679552b53068506



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

  def update_query(new_path)
    new_query = @query.gsub(/\/fakebook\//, new_path)
  end
  
  def update_session(cookie)
    @query = "GET /fakebook/ HTTP/1.0\nFrom: shogunx@ccs.neu.edu\nCookie: csrftoken=#{cookie[:csrf]}; sessionid=#{login_session}\nConnection: keep-alive\nUser-Agent: HTTPTool/1.0\r\n\r\n"
  end
  
  def get_cookie
    response = get login_query
    csrf = response.scan(/csrftoken=\w*/).first.split("=")[1]
    session_id = response.scan(/sessionid=\w+/).first.split("=")[1]
    @cookie={:csrf=>csrf,:session_id=>session_id}
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
    t1 = Time.new
    #success, can login and get 302 found response so far, and can get the session id after logedin.
    new_session_id = login 
    #get index page with new session id
    update_session(cookie)
    
    secreat_flags = bfs("/fakebook/")
    
    t2 = Time.new
    puts "Total time: #{t2-t1} secs."
    
    puts secreat_flags
    
  end
  
  
  def bfs(path)
    queue = Queue.new
    track = {}
    track[path] = 1#dummy value
    queue<<path # root node
    secreat_flags = []
    count = 1
    # five_err = 0
    re_try = 0
    # p 'into while loop'
    while !queue.empty?
      current_path = queue.pop
      # puts "url poped from the queue:\n#{current_path}"
      new_query = update_query current_path # update query explicitly
      # p new_query
      current_response = get(new_query)
      
      until current_response[0..15].scan(/HTTP\/1.1 500/).empty?
        re_try = re_try + 1
        puts "retrying at #{re_try} times"
        current_response = get(new_query)
      end
      
      
      # unless header.scan(/HTTP\/1.1 500/).empty?
        # five_err = five_err+1
      # end
      # p "current response:\n#{current_response}"
      
      flags = current_response.scan(/FLAG: .{0,64}/)
      if flags
        flags.each do |flag|
          secreat_flags<<flag[6..-1]
        end
      end
      
      
      adjacent_urls = parse_html(current_response)
      unless adjacent_urls.nil?
        # puts "url add to the queue:\n"
        adjacent_urls.each do |url|
          url = url[0..-2]
          if track[url].nil?
            count = count+1
            # if count==200
              # return count
            # end
            # puts url
            track[url] = 1
            queue<<url
          end
        end
      end
    end
    # puts "total 500 error: #{five_err}"
    puts "total 500 error retry: #{re_try}"
    puts "total #{count} urls"
    return secreat_flags
  end
  
    #method to parse html content, will return all valid url under 'cs5700.ccs.neu.edu' domain
  def parse_html(html)
    urls = html.scan(/\/fakebook\/.{0,20}"/)
  end
  
  
  #get method
  def get(request=nil)
    @socket = TCPSocket.open(host,port) 
    @socket.write request
    response= @socket.recv(1000000)#read method take soooooo long.
    ########## if use socket.recv(10000000), it takes 8~9 secs to count 600 urls
  end 
  
  def get_post_query(length,csrf,sessionid)
    @login_query = "POST /accounts/login/?next=/fakebook HTTP/1.0\nHost: cs5700.ccs.neu.edu\nFrom: shogunx@ccs.neu.edu\nReferer: http://cs5700.ccs.neu.edu/accounts/login/?next=/fakebook/\nUser-Agent: HTTPTool/1.0\nContent-Type: application/x-www-form-urlencoded\nContent-Length: #{length}\nCookie: csrftoken=#{csrf}; sessionid=#{sessionid}\r\n\r\n"
    # query = "GET #{path} HTTP/1.0\nFrom: someuser@jmarshall.com\nUser-Agent: HTTPTool/1.0\n"
  end
  
end


