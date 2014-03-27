all: clean table
clean:
	rm -f *.php *.html *.log
table:
	sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP