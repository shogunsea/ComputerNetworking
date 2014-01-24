require 'net/http'
#require 'debugger'

ARGV.each do |a|
  p a
end



uri = URI('http://example.com/index.html')
# debugger
params = { :limit => 10, :page => 3 }
uri.query = URI.encode_www_form(params)
# debugger

res = Net::HTTP.get_response(uri)
# debugger
puts res.body if res.is_a?(Net::HTTPSuccess)



require 'socket'

host = 'www.google.com'
port = 80

s = TCPSocket.open host, port
s.puts "GET / HTTP/1.1\r\n"
s.puts "\r\n"

# while line = s.gets
  # puts line.chop
# end
a = s.read
p a

s.close
