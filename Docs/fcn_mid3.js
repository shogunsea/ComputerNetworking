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

}

3.advantange and limitaions of bridged/switched network

4.Three way handshake, sequence number, acks number work.

5.RTO on TCP vs Wireless:{

}

6.TCP on high speed internet, problems of TCP:{

}

7.Remy

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