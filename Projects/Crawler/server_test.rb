require "socket"
dts = TCPServer.new('localhost', 20000)
while (s = dts.accept)
  print(s, " is accepted\n")
  loopCount = 0;
  loop do
    Thread.start(s) do
    loopCount = loopCount + 1
      lineRcvd = s.recv(1024)
      if ( !lineRcvd.empty? )
        puts("#{loopCount} Received: #{lineRcvd}")
        s.write(Time.now)
      end
    end
  end
  s.close
  print(s, " is gone\n")
end