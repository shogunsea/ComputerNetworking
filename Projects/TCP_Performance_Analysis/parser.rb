# require 'debugger'
class Parser
	attr_accessor :numpkt, :pktdrops
	# numberOfPackets = 0
	# packetDrops = 0
	def initialize
		@numpkt = 0
		@pktdrops = 0
	end

	def read(path)
		record = {}
		File.open(path, "r"){ |f|
			count = 0
			f.each_line do |l|
				record = parse(l)
				if record[:fnode].to_f==1 && record[:tnode] && record[:event]=="+"
					@numpkt = @numpkt +1
				end

				if record[:fid]==2 && record[:event] =="d"
					@pktdrops = @pktdrops + 1
				end
				# debugger
				# puts l
				# count = count+1
				# if count == 20
				# 	break
				# end
			end
		}
		record
	end

	def loss
		pktdrops.to_f / numpkt.to_f 
	end
	
	# item index in the record filed:
	# 0 : event
	# 1: time
	# 2: from node
	# 3: to node
	# 4: packet type
	# 5: packte size
	# 6: flags ----
	# 7: flow id(fid)
	# 8: source address
	# 9: destination address
	# 10: sequence number
	# 11: packet id
	def parse(line)
		items = line.split(' ')
		record = {}
		record[:event] = items[0]
		record[:time] = items[1]
		record[:fnode] = items[2]
		record[:tnode] = items[3]
		record[:pktype] = items[4]
		record[:pktsize] = items[5]
		record[:fid] = items[7]
		record[:srcadd] = items[8]
		record[:desadd] = items[9]
		record[:seqnum] = items[10]
		record[:pktid] = items[11]
		record
	end
end