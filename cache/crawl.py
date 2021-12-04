import requests
import pandas as pd

cache = dict()
response_message = ""


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


if __name__ == '__main__':
    # validate argument 
    
    data = pd.read_csv("source.csv")
    # print(data.loc[0])
   
    # return 
    source_data = data["website"].tolist()

    
    for d in source_data:
        print(d)
        get_article(d)
        if response_message == '404 NOT FOUND':
            print(d)
            print(response_message)
            
   
