import socket  # for socket
import sys
import time
import re
import os
from base64 import b64decode
import pandas as pd
import random
import matplotlib.pyplot as plt
import subprocess

hitCount = -1
missCount = -1


def set_up_experiment():
    global hitCount
    global missCount
    data = pd.read_csv("source.csv")
    # print(data.loc[0])

    # return
    source_data = data["website"].tolist()

    iteration_num = 20  # number of iteration for each probe
    experiment_num = 100
    miss = []
    hit = []
    # initiate empty array to store delay or throughput
    average_rtt = []

    for _ in range(experiment_num):
        rtt = []
        hitCount = 0
        missCount = 0

        for i in range(iteration_num):
            req = random.choice(source_data)
            print("iteration ", i)
            print("curl -x localhost:8888 " + req)
            start_time = time.time()
            subprocess.call("curl -x localhost:8888 " + req, shell=True)
            end_time = time.time()
            t = end_time - start_time
            rtt.append(t)

        counts = read_nginx_log()
        average_rtt.append(sum(rtt) / iteration_num)
        miss.append(counts[1] - missCount)
        hit.append(counts[0] - hitCount)
        hitCount += counts[0]
        missCount += counts[1]

    print("Miss avg ", sum(miss) / experiment_num)
    print("Hit avg ", sum(hit) / experiment_num)
    rtt_df = pd.DataFrame()
    rtt_df["RTT"] = average_rtt
    rtt_df["MISS"] = miss
    rtt_df["HIT"] = hit

    rtt_df.to_csv('rtt.csv')
    # ts = pd.Series(rtt)
    # ts.plot()

    figure, axis = plt.subplots(2)

    # For Sine Function
    axis[0].plot(average_rtt)
    axis[0].set_title("average RTT")

    # For Cosine Function
    axis[1].plot(miss, label=' Miss')
    axis[1].plot(hit, label='Hit')
    axis[1].set_title("Hit and Miss")
    axis[1].legend()

    plt.show()


def read_nginx_log():
    global hitCount
    global missCount
    hit = 0
    miss = 0
    file = '/var/log/nginx/cache_access.log'
    f = open(file, "r")
    for line in f:
        print(line)
        if "HIT" in line:
            hit += 1
        else:
            miss += 1

    return [hit, miss]


if __name__ == '__main__':
    # validate argument
    set_up_experiment()
