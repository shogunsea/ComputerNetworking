1.[Done]Updated parse.rb method: when generating files from hash, first sort by hash keys, since ccs macine has Ruby version 1.8.7, it outputs different results from 2.0 (did not figure why), so I modified the method to sort hash values.
[Result]: Running on ccis machine has same result as I run on my machine(2.0), but due to extra process it runs quite slow when .tr file size is large.

2. Update throughput/loss/delay method for 1.8.7, test outputs to be correct.

3. [Done]Close cbr flow, only start tcp flow, see how much average throughput of tcp is smaller than the link bottleneck capacity.
[Result]:Throughput curve is similar to ones when cbr present but not yet congested, when divied by 1million, the y axis should be Mbps, turns out the stable value is around 0.4mb, with the bandwidth to be 10mb.

4. [Done]Do not set tcp window size, conduct No.3. So single tcp flow experiments have two groups of results, first one is when tcp window size set to 24(though not quite sure about the unit to be byte or bit, I guess it should be byte), second one is using default size(not explicitly set it).
[Result]:

5. Set cbr rate at 9mb(capacity 10mb), plot cwnd of Tahoe and Reno to see the difference.


6. CBR&TCP, parse throughput for both flow, in unit of Mbps, plot two lines together.