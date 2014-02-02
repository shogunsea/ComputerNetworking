require 'socket'
# require 'debugger'
require './crawler'

#new instance of cralwer class
 crawler = Crawler.new

 username = ARGV[0]
 password = ARGV[1]

 secret_flags = crawler.go username, password

 puts secret_flags
 
