1.BGP, iBGP, eBGP comparison:{
	1.BGP:{
		1. Set up routes between networks.
		2.Is a path vector protocal.
		3.Use bellman-ford path vector protocal.
		4.Simple but complex, need manual configuration, policies based , driven by 
		economics.
	}
	2.How paths are selected, and how BGP can be formalized(stable paths):{
		1.Paths are selected based on the BGP attributes:{
			LocalPref:{
				Local preference to choose  most prefered route.
			}
			MED(multi-exit discriminator):{
				specifies path for from internal network to external traffic.
			}
			import rules:{
				What route advertisements to accept.
			} 
			export rules:{
				Forward which routes to whom.
			}
		2.Selection summary:{
			Highest local preference, shortest AS path, lowest MED, lowest IGP 
			cost to BGP egress, lowest router ID.
		}
		3.How BGP can be formalised(Stable paths problem):{
			Instance of Stable paths problem:{
				1.graph of nodes and edges, node 0 is the origin.
				2.Each node has a set of permitted paths to origin, and 
				each path is ranked.
			}
			Solution:{
				1.An assignment such that node U''s path is either null or 
				uwP, where path uw is assigned to w and u->w exits.
				2.All nodes assigned with highest rank and consistent with neighbours. 
			}
		}
	}
	3.BGP relationships:{
		1.Customer pays provider.   Customer and provider.
		2.Peer do not pay each other.   Provider peers.
		3.GR model:{
			AS prefers to use customer path, then peer, then provider, path that
			can generate most profit should be of highest preference.
		}
		4.Valley free routing:{
			peer to peer routing should not occur after provider to customer
			routing.
		}

	}
	4.iBGP, eBGP comparison:{
		1.Definition:{
			relationships between two exterior routers of different newtork is eBGP neighbours,
			between two exterior of same network is iBGP neighbours.
		}
		2.Comparison:{
			1.OSPF does not include BGP policy info.
			2.iBGP Prevents routing loops within the AS.
			3.iBGP updates do not trigger annoucements. 
		}
	}
}

2.Distance vector vs link state:{
	Drawback of distance vector:{
		1.count to infinity problem: If there is loop in the network, cost in DV table
		might be count to infinity, how to solve:{
			Posioned Reverse: one route tell intermediate one of other path that has 
			huge cost, so that it would not route back using that path. Not compeletly
			solve the problem, multipath loops still trigger the issue.
		}
		2.Nodes may advertise incorrect path cost.
	}
	Link state:{
		1.Definition:{
			Each network periodically floods immediate reachability information to all 
		other routers.  each node learns complete network topology.
		}
		2.Two implementations:{
			OSPF:{
				Favored by companies, data centers. Built on top of ipv4. Ovrelapping 
				architecture.
			}
			IS-IS:{
				Favored by ISPs, less chatty, work with both ipv4 or v6. two level hierarchy.
			}
		}
		3.Drawbacks:{
			Nodes may advertise incorrect link costs.
		}
	}
}Comparison:{
	Link state has less message comlexity, quick to converge, operate better in large, 
	enterprise-level networks, but require more memory and processor power.
}

3.Poinsioning:{
	Lifeguard paper:{
		Lifeguard''s posioning repairs outages by instructing others to avoid paricular 
		routes, without disrupting working routes.
	}
}

4.Lifeguard:{
	1.Main idea:{
		Let edge networks reroute around failures.
	}
	2.Location challenge:{
		Use unidirecitonal information to locate error:{
			use reverse traceroute, isolate directions, use historical view.
		}
	}
	3.Avoid chanllenge:{
		reroute without participation of transit networks.
	}
}

9.UDP, TCP high level features:{
	1.UDP:{
		 provide best effortservice, transport connectionless datagram, do not
		 care about loss. 
	}
	2.TCP:{
		Provide reliable packet delivery, need to set up connection before transmission.
	}
}

13.Primary and ancillary considerations that motivated the original internet architecture:{
	1.Primary goal:{
		To develop an effective technique for multiplexed utilization of existing
		interconnected networks.
	}
	2.Ancillary considerations are:{
		1.Internet communication must continue despite loss of networks or gateways.
		2.Support multiple types of services.
		3.Should work well with a variety of networks.
		4.Cost effective.
	}
}

14.Spanning tree algorithm, performance bounds:{
	1.Principle of STP:{
		creates a tree allows only one active path at a time between any two network 
		devices (this prevents the loops) but establishes the redundant links as a
		backup if the initial link should fail. 
	}
	2.performance bounds:{
		if STP costs change, or if one network segment in the STP becomes unreachable, 
		the spanning tree algorithm reconfigures the spanning tree topology and 
		reestablishes the link by activating the standby path.
	}
}


16.Problems that may lead to delayed routing convergence:{
	The size of the network can effect the convergence time, the larger network will 
	converge slower than a smaller one. Also the different protocols may have different 
	convergence time, for example, OSPF has a much shorter time to converge than RIP. 
}