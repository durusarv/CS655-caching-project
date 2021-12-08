from __future__ import division
import socket # for socket
import sys
import time
import re
import os
from base64 import b64decode
from typing import Sized
import pandas as pd
import random
import string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import numpy as np


# hitCount = 0
# missCount= 0
cache_type= ''

def setup_connection(ip, port) : 
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket successfully created")
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))
    
    # default port for socket
    #port = 1980
    
    try:
        host_ip = socket.gethostbyname(ip)
        #host_ip = "localhost"
    except socket.gaierror:
    
        # this means could not resolve the host
        print ("there was an error resolving the host")
        sys.exit()
    
    s.connect((host_ip, port))
    print ("the socket has successfully connected to server")
    
    return s 





def set_up_experiment(ip, port, loss, delay):

    # global hitCount
    # global missCount
    data = pd.read_csv("source.csv")
    # print(data.loc[0])
   
    # return 
    source_data = data["website"].tolist()

    iteration_num = 100 # number of iteration for each probe
    experiment_num = 50
    miss =[]
    hit =[]
    
     # initiate empty array to store delay or throughput
    average_rtt=[]
    average_size=[]
    average_th=[]
    for _ in range(experiment_num):
        rtt = []
        res_size = []
        hitCount = 0
        missCount = 0
        for i in range(iteration_num):
            req = random.choice(source_data)
            print("experiment "+str(_)+" iteration "+str(i))
            print(req)
            # start_time =  time.time()
            r,s,t  = send_request_to_cache(ip, port, req)
            
            
            
            print("size", s)
            
            r_number = np.random.normal(1,10)
            r_number = r_number/10

            if r_number < loss :
                t= 2 # default loss
                s = 1  # default size
                missCount = missCount +1
            else:
                if r == 'HIT':
                    hitCount = hitCount+1
                    print(r, hitCount)
                elif r == 'MISS':
                    missCount = missCount +1
            
            t = t+ delay
            
            rtt.append(t)
            res_size.append(s)

        average_rtt.append(sum(rtt)/iteration_num) 
        average_size.append(sum(res_size)/iteration_num)
        average_th.append(sum(res_size)/sum(rtt))
        print("MISS ", missCount/iteration_num)
        miss.append(missCount/iteration_num)
        hit.append(hitCount/iteration_num)


    print("Miss avg ",sum(miss)/experiment_num)
    print("Hit avg ",sum(hit)/experiment_num)
    rtt_df = pd.DataFrame()
    rtt_df["RTT"] = average_rtt
    rtt_df["MISS"] = miss
    rtt_df["HIT"] = hit
    rtt_df["TH"] = average_th

    now = datetime.now()
    current_time = now.strftime("%H%M%S")

    rtt_df.to_csv(cache_type+str(current_time)+"loss"+str(loss)+"delay"+str(delay)+'rtt.csv')
    # ts = pd.Series(rtt)
    # ts.plot()
    

    figure, axis = plt.subplots(3)
    figure.tight_layout(pad=3.0)
  
    # For Sine Function
    axis[0].plot(average_rtt)
    axis[0].set_title("Average RTT")
    
    # For Cosine Function
    axis[1].plot(miss, label=' Miss')
    axis[1].plot(hit, label='Hit')
    axis[1].set_title("Hit and Miss")
    axis[1].legend()

    axis[2].plot(average_th)
    axis[2].set_title("Average Throughput")

    # plt.show()
    plt.savefig(cache_type+str(current_time)+"loss"+str(loss)+"delay"+str(delay)+'.png')
   


def send_request_to_cache(ip, port, message):
    # global hitCount
    # global missCount

    res = ''
    bitSize = 0
    
    s = setup_connection(ip, port)
    # hasError = False
    # message = "http://www.bu.edu"    
    s.sendall(message.encode())
    completeData = ''
    unformatData = None

    st =  time.time()

    while True:
        data = s.recv(4096 * 1024)
        # print(data)
        if data:
            if unformatData is None:
                unformatData = data
            else:
                unformatData = unformatData + data
                
        else:
            s.close()
            break
        
    et =  time.time()
    delay = et - st
    completeData = unformatData.decode('utf-8', 'ignore')  

    if ('404 ERROR' in completeData):
        # print("404 ERROR")
        res = "404 ERROR"
    elif('HIT' in completeData):
        #  print("HIT")
         res = 'HIT'
        #  hitCount = hitCount+1
    elif('MISS' in completeData):
        # print("MISS")
        res = 'MISS'
        # missCount = missCount+1
    bitSize = sys.getsizeof(completeData)/1000000
    return res, bitSize, delay
    # print(completeData) 
    
    

if __name__ == '__main__':

    #global cache_type
    server_address = sys.argv[1:]
    if (len(server_address) < 4):        
        print("Please add ip address of server and type of cache loss delay")
        print("python client.py localhost LRU_CACHE 0.5 2")
    else:
        
        ip_address = server_address[0]
        cache_type = server_address[1]
        loss = float(server_address[2])
        delay = float(server_address[3])
        port = 9000
        # ip = "localhost"  #ip address of the server
        set_up_experiment(ip_address, port, loss, delay)
    

    
    #validate the argument 
    