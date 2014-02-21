
path = ARGV[0]

records = []
File.open(path, "r"){ |f|
	count = 0
	f.each_line do |line|
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
		records<< record
	end
}

	nodes = {"0"=>0,"1"=>0,"2"=>0,"3"=>0,"4"=>0,"5"=>0,"6"=>0}
#Count packets recevied or sent by node 4
	drop = {:tcp=>0, :cbr=>0}
	d = 0
  records.each do |r|
  	for i in 0..6
  		if r[:tnode].to_i==i || r[:fnode].to_i==i
  			nodes["#{i}"] =nodes["#{i}"]+1 
  		end
  	end
  	if r[:event]=="d"&&r[:pktype]=="cbr"
  		drop[:cbr] = drop[:cbr]+1
  	elsif r[:event]=="d"&&r[:pktype]=="tcp"
  		drop[:tcp] = drop[:tcp]+1
  	end
  end

  puts "#{records.size} records in total"
  t = 0
  for i in 0..6
  	count = nodes["#{i}"]
	puts "#{count} records related with node #{i}"
  end
  puts "drop: #{drop.inspect}"

  puts "tcp flow calc test:"

  from_tcp_source = 0
  to_tcp_source = 0
  from_tcp_sink = 0
  to_tcp_sink = 0


  	f_0_t_1 = 0
  	f_1_t_0 = 0
  	f_1_t_0_ack = 0
  	f_0_t_1_ack = 0
  	f_0_t_2 = 0
  	f_1_t_2 = 0
  	f_2_t_1 = 0
  	f_2_t_3 = 0
  	acks_to_source = []
  	# seq_num = []

  	sent_time = {}

  records.each do |r|

  	if r[:fnode].to_i==0 
  		sent_time[r[:seqnum].to_i] ||= r[:time].to_f
  	end
  	#Source node sent packets with duplicate seqnum, re_send process
  	# if r[:fnode].to_i==0 
  		#if seq_num.include?(r[:seqnum])
  			# puts "duplicate seqnum!"
  			# break
  		#else
  			# seq_num<<r[:seqnum]
  		#end
  	# end


  	if r[:fnode].to_i==0 && r[:tnode].to_i==1 && r[:fid].to_i ==1 
  		f_0_t_1 = f_0_t_1 +1
  	end
  	if r[:fnode].to_i==0 && r[:tnode].to_i==1 && r[:fid].to_i ==1 && r[:pktype]=="ack"
  		f_0_t_1_ack = f_0_t_1_ack +1
  	end
	if r[:fnode].to_i==1 && r[:tnode].to_i==0 
  		f_1_t_0 = f_1_t_0 +1
  	end
  	if r[:fnode].to_i==1 && r[:tnode].to_i==0 && r[:pktype]=="ack"
  		f_1_t_0_ack = f_1_t_0_ack +1
  		acks_to_source<<r
  	end
  	if r[:fnode].to_i==0 && r[:tnode].to_i==2 && r[:fid].to_i ==1 
  		f_0_t_2 = f_0_t_2 +1
  	end
  	if r[:fnode].to_i==1 && r[:tnode].to_i==2 && r[:fid].to_i ==1 
  		f_1_t_2 = f_1_t_2 +1
  	end
  	if r[:fnode].to_i==2 && r[:tnode].to_i==3 && r[:fid].to_i ==1 
  		f_2_t_3 = f_2_t_3+1
  	end
  	if r[:fnode].to_i==2 && r[:tnode].to_i==1 && r[:fid].to_i ==1 
  		f_2_t_1 = f_2_t_1 +1
  		
  	end

  	if r[:fnode].to_i==0
  		from_tcp_source = from_tcp_source+1
  	elsif r[:fnode].to_i==3
  		from_tcp_sink = from_tcp_sink+1
  	elsif r[:tnode].to_i == 0
  		to_tcp_source = to_tcp_source +1
  	elsif r[:tnode].to_i == 3
  		to_tcp_sink = to_tcp_sink+1
  	end

  	#if r[:tnode].to_i==1 && f[]

  end
  # puts "seq count: #{seq_num.size}"
  puts "from_tcp_source:#{from_tcp_source}"
  puts "to_tcp_sink:#{to_tcp_sink}"
  puts "from_tcp_sink:#{from_tcp_sink}"
  puts "to_tcp_source:#{to_tcp_source}"
  puts
  puts "from node 0 to node 1 in tcp flow: #{f_0_t_1}"
  puts "from node 0 to node 1 in tcp flow ack: #{f_0_t_1_ack}"
  puts "from node 1 to node 0 in tcp flow: #{f_1_t_0}"
  puts "from node 1 to node 0 in tcp flow ack: #{f_1_t_0_ack}"
  puts "from node 0 to node 2 in tcp flow: #{f_0_t_2}"
  puts "from node 1 to node 2 in tcp flow: #{f_1_t_2}"
  puts "from node 2 to node 1 in tcp flow: #{f_2_t_1}"
  puts "from node 2 to node 3 in tcp flow: #{f_2_t_3}"
  puts "there is some loss...right.."

  puts "sent size: #{sent_time.size}"
  puts "acks size: #{acks_to_source.size}"
  acks_unique_seqnum = {}
  acks_to_source.each do |ack|
	acks_unique_seqnum[ack[:seqnum].to_i] ||= ack[:time].to_f
  end
  puts "ack unique seq num size: #{acks_unique_seqnum.size}"
  
  puts "<<<<<<<<<\n<<<<<<<<<\nRTT calculation comparison...."

  # Method 1, sum all the time of ack packets recevied at source, 
  # then divide by number of acks.
  rtt1 = 0.0
  rtt1_count = 0
  records.each do |r|
  	if r[:event]=="r" && r[:tnode].to_i==0
  		rtt1 = rtt1 + r[:time].to_f
  		rtt1_count = rtt1_count + 1
  	end
  end
  puts "Method 1: total_rtt/count = #{rtt1/rtt1_count}"
  # Method 2, only count unique sequence number ack. iterate all unique
  # acks, search corresponding sequence number, sum all time difference.
  rtt2 = 0.0
  rtt2_count = 0
  acks_unique_seqnum.each do |ack|

  end


#   puts "acks are:"
#   sent_found = []
#   p acks_to_source
#   puts "searching packets:"
#   acks_to_source.each do |ack|
#   	seq_num = ack[:seqnum].to_i
#   	records.each do |r|
#   		if r[:seqnum].to_i ==seq_num && r[:fnode].to_i==1&&r[:tnode].to_i==2
#   			sent_found<<"found #{seq_num} sent"
#   			break
#   		end
#     end
#   end

  


# File.open("./sent_found.txt", 'w') do |file|
# 	sent_found.each do |found|
#  		file.write(found.to_s+"\n")
#  	end
#  end


  


		