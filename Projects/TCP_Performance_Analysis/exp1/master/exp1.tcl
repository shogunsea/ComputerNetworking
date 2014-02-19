if {$argc!=1} {
	puts "Usage ns exp1.tcl TCPVersion"
	puts "Example: ns exp1.tcl Reno"
}

set par1 [lindex $argv 0]

#Create a simulator object
set ns [new Simulator]

set tf [open output_$par1.tr w]
$ns trace-all $tf

#trace cwnd 
set f0 [open cwnd_$par1.tr w]

# #Define a 'finish' procedure
proc finish {} {
        global ns tf
        $ns flush-trace
        close $tf
        exit 0
}

# Define 'record' procedure to record cwnd
proc record { } {
	global ns tcp f0
	set now [$ns now]
	puts $f0 "$now [$tcp set cwnd_]"
	$ns at [expr $now+0.01] "record"
}

#Create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail


if {$par1=="Tahoe"} {
	set tcp [new Agent/TCP]
} elseif {$par1=="Reno"} {
	set tcp [new Agent/TCP/Reno]
} elseif {$par1=="Newreno"} {
	set tcp [new Agent/TCP/Newreno]
} elseif {$par1=="Vegas"} {
	set tcp [new Agent/TCP/Vegas]
}
$ns attach-agent $n1 $tcp
#set window size smaller/larger? to observe cwnd change
# default tcp window_ size is 20!!
$tcp set window_ 20
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1


#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

# Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 2

# Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 9.5mb
$cbr set random_ false

$ns at 0.1 "record"
#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp start"
$ns at 20.0 "$ftp stop"
$ns at 20.0 "$cbr stop"

#Call the finish procedure after 5 seconds of simulation time
$ns at 21.0 "finish"

#Print CBR packet size and interval
# puts "CBR packet size = [$cbr set packet_size_]"
# puts "CBR interval = [$cbr set interval_]"
 puts "Default tcp window size is: [$tcp set window_]"
#Run the simulation
$ns run
close $tf
close $f0
