require './parser'
require 'debugger'

parser = Parser.new

path = ARGV[0]

file_name = path.split('.tr').first.split('./').last

records = parser.read path

delay = parser.delay records

throughput = parser.throughput records

loss = parser.loss records

debugger

p 's'
 # File.open('./delay_start.txt', 'w') do |file|
 # 	delay[:start_time].each do |id, time|
 # 		file.write(id.to_s+","+ time.to_s+"\n")
 # 	end
 # end
 # File.open('./delay_end.txt', 'w') do |file|
 # 	delay[:end_time].each do |id, time|
 # 		file.write(id.to_s+","+ time.to_s+"\n")
 # 	end
 # end
 #  File.open('./delay_final.txt', 'w') do |file|

 #  	# delay[:delay].keys.sort.each do |time|
 #  		# file.write(time.to_s+","+ delay[:"#{time}"].to_s+"\n")
 # 	delay[:delay].each do |id, time|
 # 		file.write(id.to_s+" "+ time.to_s+"\n")
 # 	end
 # end
  #  File.open("./throughput_#{file_name}.txt", 'w') do |file|

  # 	# delay[:delay].keys.sort.each do |time|
  # 		# file.write(time.to_s+","+ delay[:"#{time}"].to_s+"\n")
 	# throughput[:th].each do |id, time|
 	# 	file.write(id.to_s+" "+ time.to_s+"\n")
 	# end

 	File.open("./loss_#{file_name}.txt", 'w') do |file|

  	# delay[:delay].keys.sort.each do |time|
  		# file.write(time.to_s+","+ delay[:"#{time}"].to_s+"\n")
 	loss.each do |id, time|
 		file.write(id.to_s+" "+ time.to_s+"\n")
 	end
 end

# debugger 

p 's'



