# first of all import the socket library
import socket
import sys   
import re 
import time   
import requests

cache = dict()
response_message =''


def get_article_from_server(url):
    global response_message
    res = None
    #print("Fetching article from server...")
    try:
        response = requests.get(url)
        response_message = "MISS"
        res = response.text
    except:
        response_message = '404 NOT FOUND'
        
    
    return res

def get_article(url):
    global response_message
    #print("Getting article...")
    # print(url)
    if (url.startswith("www.")):
        url = "http://"+url
    elif not (url.startswith("http://www.")):
        url = "http://www."+url
    # print(url)

    if url not in cache:
        cache[url] = get_article_from_server(url)
    else:
        response_message = 'HIT'
   
    #print(response_message)
    return cache[url]



def server_program(port):
    global response_message
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
    print ("Socket successfully created")

    # 10.0.0.219
    host = socket.gethostname()
    print("host: "+host)
    server_address = ('', port)

    s.bind(server_address)
         
    print("socket binded to %s" %port)
    
    # put the socket into listening mode
    s.listen(5)    
    print("socket is listening")

    # the program keep  running waiting for connection from client 
    while True:
        print('waiting for connection ...')
        
      

        # server recieved connection from client 
        c, addr = s.accept()    
        print ('Got connection from', addr )
        # a forever loop until we interrupt it or
        # an error occurs
        while True:
            try:
                completeData = ''
                # loop until all data is recived. siince the server only recieve 256 byte
                # some data is much bigger than that
                while True:
                    data = c.recv(1024)
                    if data:
                        completeData = completeData + data.decode()  
                        if(len(data) < 1024):
                            break     
                       
                    else:
                        print ("No data")
                        resp = '404 ERROR' # if no data recieved, send error to client and close connection
                        #c.sendall(resp.encode())
                        # c.close()                    
                        break
                #parse the data and validate data
                # print ("processing request ", completeData)                
                res = get_article(completeData) 
                if res:
                    response_message = response_message + res

                # print(response_message)
                c.sendall(response_message.encode())
                c.close()
                break

            except:
                print('close connection because of error')
                #resp = '404 ERROR'
                #c.sendall(resp.encode()) # send error message and close connection 
                break
               
            
            finally:
                print('close connection')


if __name__ == '__main__':
    # validate argument 
    
    port = 9000
    server_program(port)
    
    