require './parser'
# require 'debugger'

parser = Parser.new

path = ARGV[0]

records = parser.read path

delay = parser.delay records

# debugger

 File.open('./delay_start.txt', 'w') do |file|
 	delay[:start_time].each do |id, time|
 		file.write(id.to_s+","+ time.to_s+"\n")
 	end
 end
 File.open('./delay_end.txt', 'w') do |file|
 	delay[:end_time].each do |id, time|
 		file.write(id.to_s+","+ time.to_s+"\n")
 	end
 end
  File.open('./delay_final.txt', 'w') do |file|
 	delay[:delay].each do |id, time|
 		file.write(id.to_s+","+ time.to_s+"\n")
 	end
 end


# debugger 

p 's'



