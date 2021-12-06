import socket # for socket
import sys
import time
import re
import os
from base64 import b64decode
import pandas as pd
import random
import string
import matplotlib.pyplot as plt

hitCount = 0
missCount= 0

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

    global hitCount
    global missCount
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
            send_request_to_cache(ip, port, req)
            end_time =  time.time()
            t = end_time-start_time
            rtt.append(t)

        average_rtt.append(sum(rtt)/iteration_num) 
        miss.append(missCount/iteration_num)
        hit.append(hitCount/iteration_num)


    print("Miss avg ",sum(miss)/experiment_num)
    print("Hit avg ",sum(hit)/experiment_num)
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
    
   



   


def send_request_to_cache(ip, port, message):
    global hitCount
    global missCount
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
        print("404 ERROR")
    elif('HIT' in completeData):
         print("HIT")
         hitCount = hitCount+1
    elif('MISS' in completeData):
        print("MISS")
        missCount = missCount+1

    # print(completeData) 
    
    

if __name__ == '__main__':

    port = 9000
    ip = "localhost"
    set_up_experiment(ip, port)
    

    
    #validate the argument 
    