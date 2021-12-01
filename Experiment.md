# Introduction
	
This experiment aims to demonstrate the benefits of caching. First, we will compare the performance of clients with a web cache with the performance of clients with no web cache. Second, we intend to compare the performance of clients using various caches running different caching algorithms.

Also, we will compare our web retrieval performance by modifiying the loss rate and delay of the connection between the clients and the server.


# Part 1: Retrieving Objects with and without Caching

## Design

Our design will consist of several clients with a cache server on one GENI rack and a remote server on another GENI rack. 

The purpose of the remote server is to hold web objects for the clients to download. The cache server can be disconnected and reconnected in order to test clients with a cache and without a cache.

## Methodology

1. Set-up
	1. Load many (?) web objects onto the remote server
	2. Clear the cache server (start with a fresh cache)

### For steps 2-6:
- Run a script that makes these three clients pull random web objects from the remote server
- Have the script run for a minute long
- Script should be tracking throughput, RTT, average memory access time (hit time + miss rate * miss penalty)

2. Test 3 clients without caching without delay and without loss
3. Test 3 clients without caching with delay and without loss
4. Test 3 clients without caching without delay and with loss
5. Test 3 clients without caching with delay and with loss
6. Repeat Steps 2-5 with caching

## Analysis

(Here we'd display differences in throughput, RTT, and average memory access time with the different cases above)

# Part 2: Comparing Caches

## Design

Similarly to part 1, our design will consist of several clients with two different cache servers on one GENI rack and a remote server on another GENI rack. 

However, in this part, we will switch between our two different caches in order to compare clients with a cache and without a cache.

## Methodology

1. Set-up
	1. Load many (?) web objects onto the remote server
	2. Clear the cache server (start with a fresh cache)

### For steps 2-6:
- Run a script that makes these three clients pull random web objects from the remote server
- Have the script run for a minute long
- Script should be tracking throughput, RTT, average memory access time (hit time + miss rate * miss penalty)

2. Test 3 clients with our cache without delay and without loss
3. Test 3 clients with our cache with delay and without loss
4. Test 3 clients with our cache without delay and with loss
5. Test 3 clients with our cache with delay and with loss
6. Repeat Steps 2-5 with the ATS cache

(We can save time by doing half of this part in Part 1... aka we would have the measurements for one cache already.)

## Analysis

(Here we'd display differences in throughput, RTT, and average memory access time with the different cases above)

# Conclusion

(Here we'd discuss how caching is better than not caching and show our evidence. We'd also discuss the differences between our created cache and ATS)
