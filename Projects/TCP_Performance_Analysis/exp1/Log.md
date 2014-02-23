1.[Done]Updated parse.rb method: when generating files from hash, first sort by hash keys, since ccs macine has Ruby version 1.8.7, it outputs different results from 2.0 (did not figure why), so I modified the method to sort hash values.
[Result]: Running on ccis machine has same result as I run on my machine(2.0), but due to extra process it runs quite slow when .tr file size is large.

2. Update throughput/loss/delay method for 1.8.7, test outputs to be correct.

3. [Done]Close cbr flow, only start tcp flow, see how much average throughput of tcp is smaller than the link bottleneck capacity.
[Result]:Throughput curve is similar to ones when cbr present but not yet congested, when divied by 1million, the y axis should be Mbps, turns out teh stable value is around 0.4mb, with the bandwidth to be 10mb.

4. [Done]Do not set tcp window size, conduct No.3. So single tcp flow experiments have two groups of results, first one is when tcp window size set to 24(though not quite sure about the unit to be byte or bit, I guess it should be byte), second one is using default size(not explicitly set it).
[Result]: The default tcp window size is 20, turns out to be the packet amount! (In next exp I should set a very small value to test cwnd change.) The output of two groups are almost identical, with minor change in yaxis value.

5.[Done]Set receiver window size to small value(3), to observe cwnd change, with/without cbr flow. 
[Result]:Without cbr flow, the cwnd oscillate happends only when window size is greater than around 200, seems no congestion at all, so it can reach some sort of capacity I guess. When there is cbr flow,congestion happens, so cwnd will periodly drop around window size. ##Good Result##

6.[Done] Set cbr rate at 9.5mb(capacity 10mb), plot cwnd of Tahoe and Reno to see the difference.
[Result]:Only ploted the throughput, do have differences.

7.[Done]CBR&TCP, parse throughput for both flow, in unit of Mbps, plot two lines together.
[Result]:Ploted four lines togeter, same as 6.

8.Test drop rate method, and RTT method, using Tahoe9.5mb trace file.

9. [Done]Test different calculation of throught/droprate/rtt, flowid vs pkttype. 
[Result]: ***Big Mistake***Found out that in trace file, node id is not parsed from node variable name, but rather the object id, so if you initialized two node objects named "n14" and "n15", in the trace file they are denoted as "0" and "1". Damn...
Use 'flowid=1' or 'packet_type=tcp' both have same result for tcp flow.

10.***IMPORTANT***:{
	1.'Steady state behaviour', time
	2.How to calculate:'discreet time intervals', 10-second intervals.
	3.No right answer, part goal of the project is to decide what is important in order to prove your conclusions. 
	4.In exp3, cbr rate needs to be high enough to cause pressure on tcp, 50% of bandwidth should be enough, but try an expermient to see throughput of tcp when cbr rate is 5mb.
	5.In exp3, default queue size should be sufficient.
}


11.[Done] Conduct experiments for exp1, vary cbr from 1 to 9, total 9*4=36 experiments, 36*2 = 72 trace files(one for output, one for cwnd), rearrange all the output files, move into Tahoe/Reno/Newreno/Vegas folder respectively.

12.Experiment one command summary:{
	1.Integrated throughput overtime(as in bash script 'throughput_overtime_steady_state':{
		# echo "Calculating throughput over time when cbr=1mb..."
		# ruby parse.rb throughputovertime './Tahoe/output_Tahoe1mb.tr'
		...
		# echo "Plotting integrated throughput over time when cbr=1mb..."
		# ./plot_multifiles "Time(s)" "Throughput(Mbs)" "IntegratedThroughput_CBR1mb.gif" './Tahoe/throughputovertime_Tahoe1mb.tr' './Reno/throughputovertime_Reno1mb.tr' './Newreno/throughputovertime_Newreno1mb.tr' './Vegas/throughputovertime_Vegas1mb.tr'
	}output{
		1.Will generate file like 'throughputovertime_Tahoe1mb.tr' under each variant's folder.'
		2.Will generate graphs named like "IntegratedThroughput_CBR1mb.gif" under current folder.
	}
	2.Throughput, for each variant, calculate 9 cbr values:{
		ruby parse.rb allthroughput './Tahoe/output_Tahoe1mb.tr'
		./plot_multifiles "CBR(Mbps)" "Throughput(Mbps)" "Integrated_throughput_cbr.gif" "./Tahoe/all_throughput_Tahoe.tr" "./Reno/all_throughput_Reno.tr" "./Newreno/all_throughput_Newreno.tr" "./Vegas/all_throughput_Vegas.tr"
	}output{
		1.File named like 'all_throughput_Tahoe.tr' under each variant folder.
		2.File named like "Integrated_throughput_cbr.gif" under current folder.
	}
	3.RTT, for each variant, calculate 9 cbr values:{
		ruby parse.rb allrtt './Tahoe/output_Tahoe1mb.tr'
		./plot_multifiles "CBR(Mbps)" "RTT(ms)" "Integrated_rtt_cbr.gif" "./Tahoe/all_rtt_Tahoe.tr" "./Reno/all_rtt_Reno.tr" "./Newreno/all_rtt_Newreno.tr" "./Vegas/all_rtt_Vegas.tr"
	}output{
		1.File named like 'all_rtt_Tahoe.tr' under each variant folder.
		2.File named like "Integrated_rtt_cbr.gif" under current folder.
	}
	3.droprate, for each variant, calculate 9 cbr values:{
		ruby parse.rb alldroprate './Tahoe/output_Tahoe1mb.tr'
		./plot_multifiles "CBR(Mbps)" "DropRate(%)" "Integrated_droprate_cbr.gif" "./Tahoe/all_droprate_Tahoe.tr" "./Reno/all_droprate_Reno.tr" "./Newreno/all_droprate_Newreno.tr" "./Vegas/all_droprate_Vegas.tr"
	}
}


13.[Done] Updated gnuplot style, using linespoints, key/legent out side of graph.

14.[Results] Drops occurs only at node3(id=2)

15. [Done]wrote a ruby script to generate experiment 2 commands, combining 4 types of comparisons
	and cbr values vary from 0.5 to 10.5, approximately saves me 4*20 = 80 lines of code.

16. Experiment 2 command summary:{
	1.Generate ns2 script, and trace file:{
		ruby exp2_ruby_command_generator.rb 0.5 10.5 rr
		./exp2_ns_script
	}output:{
		1. 'exp2_ns_script' under current folder.
		2. Trace files of Reno/Reno when cbr vary from 0.5 to 10.5, under current folder. 
	}
	2.Calculate throughput, rtt, droprate, for Reno/Reno comparison when cbr vary from 0.5 to 10.5 mb.{
		ruby parse.rb allthroughput './RenoReno/output_rr0.5mb.tr'
		ruby parse.rb alldroprate './RenoReno/output_rr0.5mb.tr'
		ruby parse.rb allrtt './RenoReno/output_rr0.5mb.tr'
	}output:{
		1.'all_throughput_rr.tr' under each variant folder.
		2.'all_droprate_rr.tr' under each variant folder.
		3.'all_rtt_rr.tr' under each variant folder.
	}****What is different from exp1*****: parser output single tracefile, contains there
	columns, in exp1 that is two. First one is cbr vlaue, second is for tcp1, 
	third column is for tcp2, then you should modify plot script, to plot two lines
	using single file.
	3.Plot throughput, rtt, droprate for Reno/Reno comparison, using plot_singlefile_multilines script:{
		./plot_singlefile_multilines "CBR(Mbps)" "Throughput(Mbps)" "rr_comparison_throughput.gif" "./RenoReno/all_throughput_rr.tr" "Reno1" "Reno2"
		./plot_singlefile_multilines "CBR(Mbps)" "RTT(ms)" "rr_comparison_rtt.gif" "./RenoReno/all_rtt_rr.tr" "Reno1" "Reno2"
		./plot_singlefile_multilines "CBR(Mbps)" "DropRate(%)" "rr_comparison_droprate.gif" "./RenoReno/all_droprate_rr.tr" "Reno1" "Reno2"
	}
	4.Generate tracefile for outer groups of comparison:{
		ruby exp2_ruby_command_generator.rb 0.5 10.5 nr
		./exp2_ns_script
		ruby exp2_ruby_command_generator.rb 0.5 10.5 vv
		./exp2_ns_script
		ruby exp2_ruby_command_generator.rb 0.5 10.5 nv
		./exp2_ns_script
	}
	4.Repeat step 2-3 for NewReno/Reno, Vegas/Vegas, Newreno/Vegas:{
		1.NewReno/Reno:{
			ruby parse.rb allthroughput './NewrenoReno/output_nr0.5mb.tr'
			ruby parse.rb alldroprate './NewrenoReno/output_nr0.5mb.tr'
			ruby parse.rb allrtt './NewrenoReno/output_nr0.5mb.tr'

			./plot_singlefile_multilines "CBR(Mbps)" "Throughput(Mbps)" "nr_comparison_throughput.gif" "./NewrenoReno/all_throughput_nr.tr" "Newreno" "Reno"
			./plot_singlefile_multilines "CBR(Mbps)" "RTT(ms)" "nr_comparison_rtt.gif" "./NewrenoReno/all_rtt_nr.tr" "Newreno" "Reno"
			./plot_singlefile_multilines "CBR(Mbps)" "DropRate(%)" "nr_comparison_droprate.gif" "./NewrenoReno/all_droprate_nr.tr" "Newreno" "Reno"
		}
		2.Vegas/Vegas:{
			ruby parse.rb allthroughput './VegasVegas/output_vv0.5mb.tr'
			ruby parse.rb alldroprate './VegasVegas/output_vv0.5mb.tr'
			ruby parse.rb allrtt './VegasVegas/output_vv0.5mb.tr'

			./plot_singlefile_multilines "CBR(Mbps)" "Throughput(Mbps)" "vv_comparison_throughput.gif" "./VegasVegas/all_throughput_vv.tr" "Vegas1" "Vegas2"
			./plot_singlefile_multilines "CBR(Mbps)" "RTT(ms)" "vv_comparison_rtt.gif" "./VegasVegas/all_rtt_vv.tr" "Vegas1" "Vegas2"
			./plot_singlefile_multilines "CBR(Mbps)" "DropRate(%)" "vv_comparison_droprate.gif" "./VegasVegas/all_droprate_vv.tr" "Vegas1" "Vegas2"
		}
		3.Newreno/Vegas:{
			ruby parse.rb allthroughput './NewrenoVegas/output_nv0.5mb.tr'
			ruby parse.rb alldroprate './NewrenoVegas/output_nv0.5mb.tr'
			ruby parse.rb allrtt './NewrenoVegas/output_nv0.5mb.tr'

			./plot_singlefile_multilines "CBR(Mbps)" "Throughput(Mbps)" "nv_comparison_throughput.gif" "./NewrenoVegas/all_throughput_nv.tr" "Newreno" "Vegas"
			./plot_singlefile_multilines "CBR(Mbps)" "RTT(ms)" "nv_comparison_rtt.gif" "./NewrenoVegas/all_rtt_nv.tr" "Newreno" "Vegas"
			./plot_singlefile_multilines "CBR(Mbps)" "DropRate(%)" "nv_comparison_droprate.gif" "./NewrenoVegas/all_droprate_nv.tr" "Newreno" "Vegas"
		
		}
	}
}

