require 'debugger'

path = ARGV[0]

File.open(path, "r"){ |f|
	f.each_line do |l|
		# debugger
		puts l
	end
}