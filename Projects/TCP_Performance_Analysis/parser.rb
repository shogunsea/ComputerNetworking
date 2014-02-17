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
		records = []
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
				records<< record
			end
		}
		records
	end

	def loss
		pktdrops.to_f / numpkt.to_f 
	end

	def delay(records)
		max_pkt_id = 0
		start_time = {}
		end_time = {}
		records.each do |r|
			max_pkt_id = r[:pktid].to_i if r[:pktid].to_i > max_pkt_id
			start_time["#{r[:pktid]}"] ||= r[:time].to_f
			if r[:event]!="d" && r[:fid].to_i==2
				if r[:event]=="r"
					end_time["#{r[:pktid]}"] = r[:time].to_f 
				else
					end_time["#{r[:pktid]}"] = -1
				end
			end
		end
		delay = {}
		end_time.values.sort.each do |e|
			unless e==-1
				packet =0
				end_time.each do |pktid, time|
					packet = pktid if time==e
				end
				d =  end_time["#{packet}"] - start_time["#{packet}"]
				delay["#{e}"] = d>0? d: 0
			end
		end
		# for i in 0..max_pkt_id
		# 	d =  end_time["#{i}"].to_f - start_time["#{i}"].to_f
		# 	delay["#{i}"] = d>0? d: 0
		# end
		puts max_pkt_id
		{:start_time => start_time, :end_time => end_time, :delay => delay}
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