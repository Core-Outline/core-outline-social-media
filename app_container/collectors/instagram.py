import re
import http.client
import json
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(f"{os.getcwd()}/app")
from utils.gcs import saveToCloud
from datetime import datetime


def get_instagram_data(accounts_path, topics_df, ):
    accounts_df = pd.read_csv(path, index_col=0)
    topics_df = pd.read_csv(path, index_col=0)
    
    posts_and_likes_df = pd.DataFrame()
    for acc in accounts_df['account'].values:
        _posts_likes = getPostsAndLikes(username_id_or_url=acc, pagination_token=None, posts=[])
        posts_and_likes_df = pd.concat([posts_and_likes_df, _posts_likes])
        _reels = getReels(username_id_or_url=acc, pagination_token=None, reels=[])
        _stories = getStories(username_id_or_url=acc)
        _highlights = getHighlights(username_id_or_url=acc)
        time = datetime.now()
        saveToCloud(_posts_likes, f"digital-media/instagram/{acc}/posts_and_likes/{time.strftime('%Y%m%d')}.parquet", bucket_name)
        saveToCloud(_reels, f"digital-media/instagram/{acc}/reels/{time.strftime('%Y%m%d')}.parquet", bucket_name)
        saveToCloud(_stories, f"digital-media/instagram/{acc}/stories/{time.strftime('%Y%m%d')}.parquet", bucket_name)
        saveToCloud(_highlights, f"digital-media/instagram/{acc}/highlights/{time.strftime('%Y%m%d')}.parquet", bucket_name)
    
    for ids in posts_and_likes_df['id'].values:
        _comments = getPostsComments(code_or_id_or_url=id, pagination_token=None, comments=[])
        saveToCloud(_comments, f"digital-media/instagram/comments/{time.strftime('%Y%m%d')}.parquet", bucket_name)
     
def getPostsAndLikes(username_id_or_url="eco_elma", pagination_token = None, df=pd.DataFrame()):
    def extract_full_text(input_string):
        pattern = r"'text':\s*'([^']+)'\s*,?"
        pattern2 = r"'video_url':\s*'([^']+)'\s*,?"
        pattern3 = r"'url':\s*'([^']+)'\s*,?"
        caption = re.findall(pattern, str(input_string))
        vids = re.findall(pattern2, str(input_string))
        img = re.findall(pattern3, str(input_string))
        post_id = input_string['id']
        return post_id,caption, vids, img
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    if pagination_token == None:
        conn.request("GET", f"/v1.2/posts?username_or_id_or_url={username_id_or_url}", headers=headers)
    else:    
        conn.request("GET", f"/v1.2/posts?username_or_id_or_url={username_id_or_url}&pagination_token={pagination_token}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    print(result['pagination_token'])
    try:
        res_df = pd.DataFrame(result['data']['items'])
        _df = pd.DataFrame(index=[i for i in range(len(res_df))])
        ids = []
        full_texts = []
        created_ats = []
        comment_counts = []
        like_counts = []
        play_counts = []
        share_counts = []
        video_urls = []
        image_urls = []
        screen_names = []
        full_names = []
        profile_pictures = []
        try: 
            ids = [ i for i in res_df['id'] ]
        except:
            pass
        try: 
            full_texts = [ i['text'] for i in res_df['caption'] ]
        except:
            pass
        try: 
            created_ats = [ i['created_at'] for i in res_df['caption'] ]  
        except:
            pass
        try: 
            comment_counts = [ i for i in res_df['comment_count'] ]
        except:
            pass
        try: 
            like_counts = [ i for i in res_df['like_count'] ]
        except:
            pass
        try: 
            play_counts = [ i for i in res_df['ig_play_count'] ]
        except:
            pass
        try: 
            share_counts = [ i for i in res_df['share_count'] ]
        except:
            pass
        try: 
            like_counts = [ i for i in res_df['like_count'] ]
        except:
            pass
        try: 
            video_urls = [ i for i in res_df['video_url'] ]
        except:
            pass
        try: 
            image_urls = [ [ j['url'] for j in i['items'] ] for i in res_df['image_versions'] ]
        except:
            pass
        try: 
            screen_names = [ i['username'] for i in res_df['user'] ]
        except:
            pass
        try: 
            full_names = [ i['full_name'] for i in res_df['user'] ]
        except:
            pass
        try: 
            profile_pictures = [ i['profile_pic_url'] for i in res_df['user'] ]
        except:
            pass
        _df = pd.DataFrame([ids, full_texts, created_ats, comment_counts, like_counts, play_counts, share_counts, video_urls, image_urls, screen_names, full_names,profile_pictures]).T 
        _df.columns = ['id','full_text','created_at','comment_count','like_count','play_count','share_count','video_url','image_urls','screen_name','full_name','profile_picture']
    
        _df['source'] = "instagram"
        df = pd.concat([df,_df])
        if result['pagination_token'] == None:
            return df
        return getPostsAndLikes(username_id_or_url=username_id_or_url,  pagination_token=result['pagination_token'], df=df)
    except Exception as e:
        print(e)
        return result         
 
def getReels(username_id_or_url="mrbeast", pagination_token = None, reels=[]):
    def extract_info(input_string):
        pattern = r'"video_url":\s*"([^"]+)"\s*,?'
        matches = re.findall(pattern, input_string)
        if matches:
            return matches
        else:
            return None
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    if pagination_token == None:
        conn.request("GET", f"/v1.2/posts?username_or_id_or_url={username_id_or_url}", headers=headers)
    else:    
        conn.request("GET", f"/v1.2/posts?username_or_id_or_url={username_id_or_url}&pagination_token={pagination_token}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    try:
        reels.extend(extract_info(data.decode("utf-8")))
    except Exception as e:
        print(extract_info(data.decode("utf-8")))
    if result['pagination_token'] != None:
       getReels(username_id_or_url=username_id_or_url,  pagination_token=result['pagination_token'], reels=reels)
    pd.DataFrame({'user':username_id_or_url, 'reels': reels})     
 
def getStories(username_id_or_url="eco_elma"):
    def extract_info(result):
        return [i for i in result['data']['items']]
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    conn.request("GET", f"/v1/stories?username_or_id_or_url={username_id_or_url}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    stories = extract_info(result)
    return pd.DataFrame(stories)
         
def getHighlights(username_id_or_url="eco_elma"):
    def extract_info(result):
        return [i for i in result['data']['items']]
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    conn.request("GET", f"/v1/highlights?username_or_id_or_url={username_id_or_url}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    result = json.loads(data)
    return pd.DataFrame(extract_info(result))
        
def getPostsComments(code_or_id_or_url="3362814775367218923", pagination_token=None, comments=[]):
    def extract_full_text(input_string):
        pattern = r'"text":\s*"([^"]+)"\s*,?'
        
        return re.findall(pattern, input_string)

    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "instagram-scraper-api2.p.rapidapi.com"
    }
    if pagination_token == None:
        conn.request("GET", f"/v1/comments?code_or_id_or_url={code_or_id_or_url}&include_insights=true", headers=headers)
    else:    
        conn.request("GET", f"/v1/comments?code_or_id_or_url={code_or_id_or_url}&pagination_token={pagination_token}&include_insights=true", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    comments.extend(extract_full_text(data.decode("utf-8")))
    if result['pagination_token'] != None and result['pagination_token'] != 0 and result['pagination_token'] != '':
       getPostsComments(code_or_id_or_url=code_or_id_or_url,  pagination_token=result['pagination_token'], comments=comments)
    return comments     
           
        
    