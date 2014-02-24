1.BGP decision process, how operators use it to manage traffic.:{
	Border Gateway Protocol (BGP) is the most common Exterior Gateway Protocol in use 
	on the Internet. When a BGP router first comes up on the Internet, either for the
	 first time or after being turned off, it establishes connections with the other 
	 BGP routers with which it directly communicates to download the entire routing 
	 table of each neighboring router. After that it only exchanges much shorter update
	  messages with other routers.
 	BGP routers send and receive update messages to indicate a change in the preferred
 	 path to reach a computer with a given IP address. If the router decides to update 
 	 its own routing tables because this new path is better, then it will subsequently
 	  propagate this information to all of the other neighboring BGP routers to which
 	   it is connected, and they will in turn decide whether to update their own tables
 	    and propagate the information further. 
}

2.bandwidth/delay product:{
	1.TCP performs poorly when:{
		1.Bandwith is large.
		2.delay(RTT) is large.
		3.bandwidth*delay is large:{
			this product indicates maximum amount of in-flight data in the network.
		}
	}
	2.Why:{
		1.Slow start and AIMD are slow to converge.
		2.TCP is ack clocked, it will react only when ack received.
	}
}

4.Three way handshake, sequence number, acks number work:{
	1.client:{
		syn<seqC, 0>
	}
	2.server:{
		syn/ack<seqS, seqC+1>
	}
	3.client:{
		ack<seqC+1, seqS+1>
	}
	each side notifies the other of starting seq number.
	each side acks the other side's starting seq number.
}

5.RTO in wireless:{
	RTO definition in TCP:{
		RTO = 2*new_rtt
	}
	problem in wireless:{
		Interference in wireless is very common, the assumtion that long RTO
		indicates congestion is no longer true.
	}
	Solution:{
		1.Use delay based congestion detection like Vegas.
		2.explicit congestion notification.
	}
}

6.TCP on high speed internet, problems of TCP:{
	1.Bandwith*delay product is large.
	2.Goals of real world TCP:{
		1.Fast window growth.
		2.Converge quickly.
		3.Fairness between other protocols.
	}
	3.problems and solutions:{
		1.throughput depends on RTT:{
			Maintain a serperate delay window, one as delay window, one as 
			congestion window.
		}
		2.Short flows:most tcp flows never leave slow start:{
			1.increase initial cwnd to 10.
			2.TCP fast open.
		}
		
	}
}

7.Remy:{
	Remy is a computer program designed to generate effective congestion control
	solution, the algorithm is based on ack sent time, ack received time and RTT
	to decide Remy congestion control, but it does not take packet loss into
	consideration.
}

8.TCP congestion control pseudo code:{
	Start:
		cwnd = 1;
		ssthresh = adv_wnd;
	Ack_received:
		if (cwnd<ssthresh)
			//slow start, additive increase
			cwnd = cwnd+1
		else
			//congestion avoidance
			cwnd = cwnd + 1/cwnd
	Time out:
		// multiplicative decrease
		ssthresh = cwnd/2
		cwnd = 1
}

9.Tahoe features:{
	1.Slow start
	2.Congestion avoidance
	Reno:{
		3.Fast retransmitt:{
			retransmitt after receiving three duplicate acks.
		}
		4.Fast recovery:{
			after a fast retransmitt set cwnd to ssthresh/2:{
				avoid slow start, prevents timeout.
			}
		}
	}
	Newreno:{
		Inproved fast retransmitt: each duplicate ack trigger a 
		retransmission.
	}
	Vegas:{
		delay based congestion avoidance 
	}
}

10.Why running out of IP addresses:{
	IPv4: 32 bits, 2^32 possible addresses which is too small.
}

