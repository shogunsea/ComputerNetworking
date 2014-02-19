require './parser'
# require 'debugger'

parser = Parser.new

path = ARGV[0]

file_name = path.split('.tr').first.split('./').last

records = parser.read path

# delay = parser.delay records

throughput = parser.throughput records

# loss = parser.loss records

# debugger

# p 's'
 # File.open("./ruby_test/delay_#{file_name}.txt", 'w') do |file|
 # 	delay.each do |id, time|
 # 		file.write(id.to_s+","+ time.to_s+"\n")
 # 	end
 # end
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
 	File.open("./ruby_test/thpt_#{file_name}.txt", 'w') do |file|
 		flow_keys = []
 		throughput.keys.each do |k|
 			flow_keys<<k.to_f
 		end
 		flow_keys.sort.each do |time|
 			#denote in Mbps unit.
	  		value = (throughput["#{time.to_s}"].to_f)/1000000	
	  		file.write(time.to_s+" "+ value.to_s+"\n")
	  	end
 end

# debugger 

# p 's'



