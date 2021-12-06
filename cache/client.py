from __future__ import division
import socket # for socket
import sys
import time
import re
import os
from base64 import b64decode
import pandas as pd
import random
import string
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime


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





def set_up_experiment(ip, port):

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
  
    for _ in range(experiment_num):
        rtt = []
        hitCount = 0
        missCount = 0
        for i in range(iteration_num):
            req = random.choice(source_data)
            print("experiment "+str(_)+" iteration "+str(i))
            print(req)
            start_time =  time.time()
            r = send_request_to_cache(ip, port, req)
            
            if r == 'HIT':
                hitCount = hitCount+1
                print(r, hitCount)
            elif r == 'MISS':
                missCount = missCount +1
            
            end_time =  time.time()
            t = end_time-start_time
            rtt.append(t)

        average_rtt.append(sum(rtt)/iteration_num) 
        print("MISS ", missCount/iteration_num)
        miss.append(missCount/iteration_num)
        hit.append(hitCount/iteration_num)


    print("Miss avg ",sum(miss)/experiment_num)
    print("Hit avg ",sum(hit)/experiment_num)
    rtt_df = pd.DataFrame()
    rtt_df["RTT"] = average_rtt
    rtt_df["MISS"] = miss
    rtt_df["HIT"] = hit

    now = datetime.now()
    current_time = now.strftime("%H%M%S")

    rtt_df.to_csv(cache_type+str(current_time)+'rtt.csv')
    # ts = pd.Series(rtt)
    # ts.plot()
    

    figure, axis = plt.subplots(2)
    figure.tight_layout(pad=3.0)
  
    # For Sine Function
    axis[0].plot(average_rtt)
    axis[0].set_title("average RTT")
    
    # For Cosine Function
    axis[1].plot(miss, label=' Miss')
    axis[1].plot(hit, label='Hit')
    axis[1].set_title("Hit and Miss")
    axis[1].legend()

    # plt.show()
    plt.savefig(cache_type+str(current_time)+'.png')
   



   


def send_request_to_cache(ip, port, message):
    # global hitCount
    # global missCount

    res = ''
    
    s = setup_connection(ip, port)
    # hasError = False
    # message = "http://www.bu.edu"    
    s.sendall(message.encode())
    completeData = ''
    unformatData = None

    while True:
        data = s.recv(4096 *4 )
        # print(data)
        if data:
            if unformatData is None:
                unformatData = data
            else:
                unformatData = unformatData + data
                
        else:
            s.close()
            break
        
    
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

    return res
    # print(completeData) 
    
    

if __name__ == '__main__':

    #global cache_type
    server_address = sys.argv[1:]
    if (len(server_address) < 2):        
        print("Please add ip address of server and type of cache")
        print("python client.py localhost LRU_CACHE")
    else:
        
        ip_address = server_address[0]
        cache_type = server_address[1]
        port = 9000
        # ip = "localhost"  #ip address of the server
        set_up_experiment(ip_address, port)
    

    
    #validate the argument 
    