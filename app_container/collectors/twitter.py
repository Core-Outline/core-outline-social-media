import http.client
import re
import json
import os
import pandas as pd
import itertools
from dateutil import parser
from dotenv import load_dotenv
import sys
from datetime import datetime

load_dotenv()

from scripts import sanitizeParams

def get_twitter_data(path):
    pass

def getPostComments(post_id=1552735248026411010):
    def extract_full_text(input_string):
        pattern = r'"full_text":\s*"([^"]+)"\s*,?'
        matches = re.findall(pattern, input_string)
        if matches:
            return matches
        else:
            return None
    conn = http.client.HTTPSConnection(os.getenv('TWITTER_RAPID_API_HOST'))

    headers = {
        'x-rapidapi-key': os.getenv('TWITTER_RAPID_API_KEY'),
        'x-rapidapi-host': os.getenv('TWITTER_RAPID_API_HOST')
    }

    conn.request("GET", f"/comments?pid={post_id}&count=40&rankingMode=Relevance", headers=headers)

    res = conn.getresponse()
    data = str(res.read().decode("utf-8"))
    result = extract_full_text(data)
    return pd.DataFrame({"comment": [i for i in result]})

def searchTopic(topic='"Adani"%20and%20"Safaricom"', tweets=pd.DataFrame(), cursor=None, cursor_history=[], start_date='2024-11-01'):
    conn = http.client.HTTPSConnection(os.getenv('TWITTER_RAPID_API_HOST'))
    
    headers = {
        'x-rapidapi-key': os.getenv('TWITTER_RAPID_API_KEY'),
        'x-rapidapi-host': os.getenv('TWITTER_RAPID_API_HOST')
    }
    if cursor == None or cursor == 0:
        conn.request("GET", f'/search-v2?type=Latest&count=20&query={topic}', headers=headers)
    else:
        conn.request("GET", f'/search-v2?type=Latest&count=20&query={topic}&cursor={cursor}', headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    # return res
    
    try:
        cursor = json.loads(data)['cursor']['bottom']
        if cursor in cursor_history:
            return tweets
        print(cursor)
        res = [ i['content'] for i in json.loads(data)["result"]["timeline"]["instructions"][0]['entries'] if i['content']['__typename'] == 'TimelineTimelineItem']
        cursor = json.loads(data)['cursor']['bottom']
        view_count = []
        user_details = []
        views_details = []
        full_texts = []
        quote_counts = []
        reply_counts = []
        retweet_count = []
        user_ids = []
        created_ats = []
        full_names = []
        screen_names = []
        profile_pictures = []
        user_ids = []
        followers_count = []
        created_ats = []
        
        try:
            view_count = [ (i['itemContent']['tweet_results']['result']['views'])['count'] for i in res  if "tweet_results" in [j for j in i['itemContent'].keys()] ]
        except Exception as e:
            pass
        try:   
            user_details = [ i['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()]]
        except Exception as e:
            pass
        try:   
            full_names = [ i['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['name'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()]]
        except Exception as e:
            pass
        try:   
            screen_names = [ i['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['screen_name'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()]]
        except Exception as e:
            pass
        try:   
            profile_pictures = [ i['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['profile_image_url_https'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()]]
        except Exception as e:
            pass
        try:   
            views_details = [ i['itemContent']['tweet_results']['result']['views'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()] ]
        except Exception as e:
            pass
        try:   
            full_texts = [i['itemContent']['tweet_results']['result']['legacy']['full_text'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()] ]
        except Exception as e:
            pass
        try:  
            quote_counts = [i['itemContent']['tweet_results']['result']['legacy']['quote_count'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()] ]
        except Exception as e:
            pass
        try:   
            reply_counts = [i['itemContent']['tweet_results']['result']['legacy']['reply_count'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()] ]
        except Exception as e:
            pass
        try:   
            retweet_count = [i['itemContent']['tweet_results']['result']['legacy']['retweet_count'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()] ]
        except Exception as e:
            pass
        try:   
            user_ids = [i['itemContent']['tweet_results']['result']['legacy']['user_id_str'] for i in res  if "tweet_results" in [j for j in i['itemContent'].keys()]]
        except Exception as e:
            pass
        try:   
            followers_count = [ i['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']['followers_count'] for i in res  if "tweet_results" in [j for j in i['itemContent'].keys()]]
        except Exception as e:
            pass
        try:   
            created_ats = [i['itemContent']['tweet_results']['result']['legacy']['created_at'] for i in res if "tweet_results" in [j for j in i['itemContent'].keys()]]
        except Exception as e:
            pass
        

        result = [user_ids,full_texts,view_count,user_details,views_details,quote_counts,reply_counts,retweet_count,created_ats, full_names, screen_names, profile_pictures,followers_count]
        
        df = pd.DataFrame(result).T
        df.columns=["user_id","full_text","view_count","user_details","views_details","quote_count","reply_count","retweet_count","created_at", "full_name", "screen_name","profile_picture","followers_count"]
        df['source'] = 'twitter'
        df['cursor'] = cursor
        df['created_at'] = [ str(i) for i in df['created_at']]
        tweets = pd.concat([tweets, df])
        tweets.to_csv("latest_tweets.csv")

        
        lastDate = parser.parse(str(start_date))
        for i in df['created_at'].values:          
            if( parser.parse(start_date) > parser.parse(i).replace(tzinfo=None) ):
                return tweets.loc[tweets['created_at'].to_datetime() > lastDate]
        # if len(tweets) > 0:
        #     print(f"Found {len(tweets.loc[tweets['full_text'].isin(df['full_text'])])} duplicates")
        # if len(tweets) > 0 and len(tweets.loc[tweets['full_text'].isin(df['full_text'])]) > 0 and len(tweets.loc[tweets['full_text'].isin(df['full_text'])]) == len(df):
        #     print(f"Found {len(tweets.loc[tweets['full_text'].isin(df['full_text'])])} duplicates")
        #     return tweets 
        # return tweets       
        return searchTopic(topic=topic, tweets=tweets, cursor=cursor)
    except Exception as e:
        print(e)
        return tweets
    
def getUserDetails(username=None):
    conn = http.client.HTTPSConnection(os.getenv('TWITTER_RAPID_API_HOST'))

    headers = {
        'x-rapidapi-key': os.getenv('TWITTER_RAPID_API_KEY'),
        'x-rapidapi-host': os.getenv('TWITTER_RAPID_API_HOST')
    }
    
    conn.request("GET", f"/user?username={username}", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))['result']['data']['user']['result']

def getUserPosts(rest_id="2455740283", cursor = None, df = pd.DataFrame(), depth=0, start_date='2024-11-11'):
    def extract_full_text(input_string):
        pattern = r'"full_text":\s*"([^"]+)"\s*,?'
        pattern_id = r'"rest_id":\s*"([^"]+)"\s*,?'
        matches = re.findall(pattern, input_string)
        matchesId = re.findall(pattern_id, input_string)
        if matches or matchesId:
            return matches, matchesId
        else:
            return None
    conn = http.client.HTTPSConnection(os.getenv('TWITTER_RAPID_API_HOST'))
    
    headers = {
        'x-rapidapi-key': os.getenv('TWITTER_RAPID_API_KEY'),
        'x-rapidapi-host': os.getenv('TWITTER_RAPID_API_HOST')
    }
    if cursor == None:
        conn.request("GET", f"/user-tweets?user={rest_id}&count=20", headers=headers)
    else:
        conn.request("GET", f"/user-tweets?user={rest_id}&count=20&cursor={cursor}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data.decode("utf-8"))
    
    
    depth+=1
    print(result)
    try:
        cursor = json.loads(data.decode("utf-8"))['cursor']['bottom']
        r1 = [ i for i in result['result']['timeline']['instructions']  if "entries" in [j for j in i.keys()] ]
        r2 = list(itertools.chain(*[ i['entries'] for i in r1 ]))
        r3 = [ i['content']['__typename'] for i in r2 ]
        legacy = pd.DataFrame()
        timelineItems = [ i['content']['itemContent']['tweet_results']['result'] for i in r2 if i['content']['__typename'] == 'TimelineTimelineItem']
        timelineModules = [ i['content'] for i in r2 if i['content']['__typename'] == 'TimelineTimelineModule']
        legacy = pd.DataFrame([ i['legacy'] for i in timelineItems ])
        legacy['rest_id'] = [ i['rest_id'] for i in timelineItems]
        legacy['source'] = "twitter"
        
        legacy['created_at'] = [ str(i) for i in legacy['created_at']]
        # legacy.to_csv("sf_tweets.csv")
        lastDate = parser.parse(str(start_date))

        df = pd.concat([df,legacy])
        for i in legacy['created_at'].values:         
            if( parser.parse(start_date) > parser.parse(str(i)).replace(tzinfo=None) ):
                return df.loc[df['created_at'].to_datetime() > lastDate]
        # df.to_csv("user_tweets.csv")
        # return df
        return getUserPosts(rest_id=rest_id,cursor=cursor,df=df, depth=depth)
    except Exception as e:
        print(df)
        return df
    
def searchKeywords(topic="Adani+AND+Safaricom", tweets=pd.DataFrame(), cursor=None, start_date="2022-01-01", cursor_history=[]):
    import http.client
    conn = http.client.HTTPSConnection(os.getenv('TWITTER_RAPID_API_HOST'))
    headers = {
        'x-rapidapi-key': os.getenv('TWITTER_RAPID_API_KEY'),
        'x-rapidapi-host': os.getenv('TWITTER_RAPID_API_HOST')
    }
    print(f"/search/search?query={topic}&section=top&limit=50&start_date={start_date}&language=en")
    if cursor == None:
        conn.request("GET", f"/search/search?query={topic}&section=top&limit=50&start_date={start_date}&language=en", headers=headers)
    else:
        conn.request("GET", f"/search/search?query={topic}&section=top&limit=50&start_date={start_date}&language=en&continuation_token={cursor}", headers=headers)
    res = conn.getresponse()
    data = res.read()   
    cursor = json.loads(data.decode("utf-8"))['continuation_token']
    print(cursor)
    if cursor in cursor_history:
        return tweets
    cursor_history.append(cursor)
    # try:
    df = pd.DataFrame(json.loads(data.decode("utf-8"))['results'])
    df.to_csv("twitter_uncleaned.csv")
    print(len(df))
    if len(tweets) > 0:
        print(f"Found {len(tweets.loc[tweets['tweet_id'].isin(df['tweet_id'])])} duplicates out of {len(df)}")
    if len(tweets) > 0 and len(tweets.loc[tweets['tweet_id'].isin(df['tweet_id'])]) > 0 and len(tweets.loc[tweets['tweet_id'].isin(df['tweet_id'])]) >= len(df):
        print(f"Found {len(tweets.loc[tweets['tweet_id'].isin(df['tweet_id'])])} duplicates")
        return tweets
    df['user_id'] = [ i['user_id'] for i in df['user'] ]
    df['full_text'] = df['text']
    df['view_count'] = df['views']
    df['user_details'] =  df['user']
    df['created_at'] = df['creation_date']
    df['full_name'] = [ i['name'] for i in df['user'] ]
    df['screen_name'] = [ i['username'] for i in df['user'] ]
    df['followers_count'] = [ i['follower_count'] for i in df['user'] ]
    df['profile_picture'] = [ i['profile_pic_url'] for i in df['user'] ]
    tweets = pd.concat([tweets, df])
    tweets.to_csv("twitter.csv")
    if cursor != None and cursor != '' and cursor != 0:
        return searchKeywords(topic=topic, tweets=tweets, cursor=cursor, start_date=start_date, cursor_history=cursor_history)
    else:
        return tweets
    # except Exception as e:
    #     print(e)
    #     return tweets

def searchKeywordsTwitter(query, start_date="2024-11-05"):
    query = sanitizeParams(query)
    return searchTopic(topic= query, tweets=pd.DataFrame(), cursor=None, start_date=start_date)

def searchUserPostsTwitter(username, start_date="2024-11-05"):
    user = getUserDetails(username=username)
    df =  getUserPosts(rest_id=user['rest_id'], start_date=start_date)
    df['favourites_count'] = user['legacy']['favourites_count']
    df['followers_count'] = user['legacy']['followers_count']
    df['friends_count'] = user['legacy']['friends_count']
    return df