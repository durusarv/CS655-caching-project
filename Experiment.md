# Introduction
	
This experiment aims to demonstrate the benefits of caching. First, we will compare the performance of clients with a web cache with the performance of clients with no web cache. Second, we intend to compare the performance of clients using various caches running different caching algorithms.

Also, we will compare our web retrieval performance by modifiying the loss rate and delay of the connection between the clients and the server.

# Terminology

- ATS
	- Shorthand for Apache Traffic Server, one of the types of caches that we will be using in this experiment
- LRU
	- Shorthand for Least Recently Used. This is the caching algorithm that we have implemented in our created cache.
- Average memory access time
	- A measurement of a cache's performance
	- Equal to the hit time of the cache plus the miss rate of the cache times the miss penalty of the cache
- Delay
	- Simulated network delay for the clients accessing web objects
- Loss
	- Simulated loss rate for the clients accessing web objects

# Part 1: Retrieving Objects with and without Caching

## Design

Our design will consist of several clients with a cache server on one GENI rack and a remote server on another GENI rack. 

The purpose of the remote server is to hold web objects for the clients to download. The cache server can be disconnected and reconnected in order to test clients with a cache and without a cache.

We have configured our setup so that a client will access their cache before downloading a web object. There is no extra setup required by the client to configure the cache server.

## Methodology

1. Set-up
	1. Load many (?) web objects onto the remote server
	2. Clear the cache server (start with a fresh cache)

### For steps 2-6:
- Run a script that makes these three clients pull web objects from the remote server at random
- Have the script run for a minute long
- Script should be tracking throughput and RTT, and also average memory access time if a cache is used
- At the end, the script will output average throughput, average RTT, and average memory access time for the clients over the minute

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

However, in this part, we will switch between our two different caches (our LRU cache and ATS) in order to compare their performance.

## Methodology

1. Set-up
	1. Load many (?) web objects onto the remote server
	2. Clear the cache server (start with a fresh cache)

### For steps 2-6:
- Run a script that makes these three clients pull web objects from the remote server at random
- Have the script run for a minute long
- Script should be tracking throughput, RTT, average memory access time (hit time + miss rate * miss penalty)
- At the end, the script will output average throughput, average RTT, and average memory access time for the clients over the minute

2. Test 3 clients with our LRU cache without delay and without loss
3. Test 3 clients with our LRU cache with delay and without loss
4. Test 3 clients with our LRU cache without delay and with loss
5. Test 3 clients with our LRU cache with delay and with loss
6. Repeat Steps 2-5 with the ATS cache

(We can save time by doing half of this part in Part 1... aka we would have the measurements for one cache already.)

## Analysis

(Here we'd display differences in throughput, RTT, and average memory access time with the different cases above)

# Conclusion

(Here we'd discuss how caching is better than not caching and show our evidence. We'd also discuss the differences between our created cache running LRU and ATS)
