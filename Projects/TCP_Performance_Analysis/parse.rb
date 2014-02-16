require './parser'
require 'debugger'

parser = Parser.new

path = ARGV[0]

result = parser.read path

debugger 

p 's'



