1.ISO OSI model layers, functionalities, example protocols/encodings:{
	1.Application layer:{
		function:{
			Offer communications services for applications.
		}
		example:{
			HTTP, FTP
		}
	}
	2.Presentation layer:{
		function:{
			Convert data between different representations.
		}
		example:{
			Big endian to little endian, ASCii to Unicode
		}
	}
	3.Session layer:{
		function:{
			Access/Session management, synchronization. 
		}
		example:{
			none.
		}
	}
	4.Transport layer:{
		function:{
			Demultiplexing of data streams, reliable packets delivery, flow and congestion control, error detection.
		}
		example:{
			TCP, UDP
		}
	}
	5.Network layer:{
		function:{
			Route packets end-to-end on a network, through multiple hops, sub-networks traffic control.
		}
		example:{
			IP, BGP, OSPF, Routers
		}
	}
	6.Datalink layer:{
		function:{
			Framing, error detection/correction, Media Access Control
		}
		example:{
			Ethernet, WiFi
		}
		Concepts:{
			MTU: maximum transmission unit, 1500 bytes.
			CSMA/CA:{
				two problems of CSMA/CD:{
					hidden terminal:Radios on the same network cannot always hear each other
					exposed terminal:Carrier sensing is problematic in wireless
				}
			}
		}
	}
	7.Physical layer:{
		function:{
			Move information between two systems connected by a physical link.
		}
		example:{
			Cable, NRZ, NRZI, Manchester
		}
	}

}

2.Physical layer encodings and schemes:{
	1.NRZ:{
		Non-Return to Zero: high signal represents 1 and low signal represents 0. Long
		string of 0 and 1 cause desynchronization.
	}
	2.NRZI:{
		Non-Return to Zero Inverted: if 1 appears then make trasition, if 0 appers then remain 
		the same, solves the problem for sequences of 1s, but not for 0s.
	}
	3.Manchester:{
		signal change from high to low represents 1, low to high represents 0. Benefit: solves 
		clock skew, but only half throughput.
	}
}

3.Datelink layer:{
	1.Framing, error detection/correction, Media access control:{
		1.Framing:{
			Datelink  layer encapsulate network layer datagram within a frame before transmission over
			the link, it adds a frame head sigh(SOH) and an end sigh(EOT) to a frame.
		}
		2.Error detection and correction:{
			Transmitting node includes error-detection bits in the frame, receving node perform 
			an error check based on this bit. Correction is similar to detection execpt that it 
			also determines where is the error and then correct it.
		}
		3.Media Access Control:{
			MAC protocal are the rules on how to share the medium, also provide strategies for detecting, 
			avoiding and recovering from collisions.
			Example:{
				Time Division Multi-Access(TDMA) cellular.
				Frequency Division Multi-Access(FDMA) cellular.
			}
		}
	}
	2.Advantages and limitations of bridged/switched newtorks:{
		1.Bridge:{
			Bridges have memoery buffer to queue packets, intelligent so that only foward packets to the correct 
			output, and high performance
			Goals of bridge and swith: reduce the collision domain.
			Function:{
				forwarding of frames, learning of addresses, spanning tree algorithm to handle loops.
			}
			Pros:{
				1.limits collision domains.
				2. Improve scalability.
			}
			Cons: More complex than hubs.
		}
		2.Switch:{
			Special case of bridge, each port is connected to a single host,
			links are full duplex, no need for collision detection.
		}
		3.Hub:{
			Hubs and repeaters are layer-1 devices, physical only.
			Pros: Hardware are cheap and fast
			Cons: No scalability.
		}
	}
}

4.Network layer:{
	1.Basic Internet service model, motivation behind the design decisions:{
		Internet offers three kind of services, non-promise deliver service, non-connection deliver,
		best-effor services. This design is diferent from how the telephone network works, since the
		designer of the Internet thought the reliability of the service should be provided by the end
		of the communication, but not the network itself, since computer have the ability of correct
		mistakes in transmitting.
	}
	2.Differences between class and prefix based addressing, Advantages of CIDR:{
		Class address: divides the address space for IPv4 into five address classes, 
		prefix based addressing organized IP address into sub-networks independent of 
		the value of the address themselves.
		Advantages of CIDR: it can be used to effectively manage 
		the available IP address space. Also can reduce the number of routing table 
		entries.
		prefix based or hierachical addressing is critical for scalability;
		CIDR improves scalability and granularity.		
		}Cons:{
		classes are still too coarse;
		routing tables are still too big.
	}
	}
	3.IP fragmentation algorithm:{
		Break large packets into smaller pieces and re-assembled at destination so that the original
		packet can pass through a linkwith small MTU limit.
	}
	4.Contrast IPv4 and IPv6:{
		Length:[32bit, 128bit]
		Representation:[binary numbers represented in decimals, binary numbers represented in hex number.]
		Fragmentation:[Done by sender and forwarding router, Done only be the sender.]
		Packet flow:[No identification, available by flow label field in the header]
		Configuration:[Manualy, auto configuration available]
	}
}



