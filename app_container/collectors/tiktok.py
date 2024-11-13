import http.client
import re
import json
import pandas as pd
import numpy as np
import os
import sys
sys.path.append(f"{os.getcwd()}/app/utils")

from gcs import saveToCloud
from datetime import datetime
def get_tiktok_data(accounts_path):
    time = datetime.now()
    accounts_df = pd.read_csv(accounts_path, index_col=0)
    trending_df = getTrendingTikToks(region="ke")
    bucket_name = "oxygene-storage"
    saveToCloud(trending_df, f"digital-media/tiktok/trending/{time.strftime('%Y%m%d')}.parquet", bucket_name)
    
    users_df = pd.DataFrame()
    for acc in accounts_df['account'].values:
        _account = getUserDetails(acc)
        users_df = pd.concat([users_df, _account])
    saveToCloud(users_df, f"digital-media/tiktok/users/{time.strftime('%Y%m%d')}.parquet", bucket_name)
    posts_df = pd.DataFrame() 
    for ids in users_df['id'].values:
        _posts = getUserPosts(user_id=ids, cursor=0, videos=[], music=[], caption=[], video_ids=[] )
        posts_df = pd.concat([posts_df,_posts])
        saveToCloud(_posts, f"digital-media/tiktok/posts/{ids}/{time.strftime('%Y%m%d')}.parquet", bucket_name)
    
    
def getTrendingTikToks(region='ke'):
    conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
    }
    conn.request("GET", "/feed/list?region=ke&count=30", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    df = pd.DataFrame(result['data'])
    df['username'] = [ i['unique_id'] for i in df['author'] ]
    df['profile_picture'] = [ i['avatar'] for i in df['author'] ]
    df['full_text'] = [ i['title'] for i in df ]
    return df

def getUserDetails(keyword='crazy_kennar'):
    def extract_info(data):
        return [ i['user'] for i in data]
    conn = http.client.HTTPSConnection("tiktok-video-no-watermark2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    conn.request("GET", f"/user/search?keywords={keyword}&count=10&cursor=0", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    if result['msg'] == 'success':
       return pd.DataFrame(extract_info(result['data']['user_list'])).iloc[0:1]
   
def getUserPosts(user_id='6832234195638207494', cursor=0, df=pd.DataFrame()):
    def extract_info(data):
        ids = [i['video_id'] for i in data]
        vids = [i['play'] for i in data]
        song = [i['music'] for i in data]
        text = [i['title'] for i in data]
        return ids, vids, song, text
    conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
    }
    conn.request("GET", f"/user/posts?user_id={user_id}&count=20&cursor={cursor}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    
    df = pd.concat([df, pd.DataFrame(result['data'])])
    print(result['data']['cursor'])
    if result['data']['cursor'] != '0' and result['data']['cursor'] != 0:             
        getUserPosts(user_id=user_id, cursor=result['data']['cursor'],df=df)
    return df        

def getPostComments(video_id='7093219391759764782', cursor = '0', df = pd.DataFrame()):
    def extract_info(data):
        text = [i['text'] for i in data]
        ids = [i['id'] for i in data]
        return ids, text
    conn = http.client.HTTPSConnection("tiktok-video-no-watermark2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    conn.request("GET", f"/comment/list?url=https%3A%2F%2Fwww.tiktok.com%2F%40tiktok%2Fvideo%2F{video_id}&count=10&cursor={cursor}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    df = pd.concat([df, pd.DataFrame(result['data'])])
    print(result['data']['cursor'])
    if result['data']['cursor'] != '0' and result['data']['cursor'] != 0:             
        getPostComments(video_id=video_id, cursor=result['data']['cursor'],  df=df)
    return df  

def getReplies(video_id='7093219391759764782',comment_id='7093229463530046213', cursor = '0', comment_ids=[], comments=[]):
    def extract_info(data):
        text = [i['text'] for i in data]
        ids = [i['id'] for i in data]
        return ids, text
    conn = http.client.HTTPSConnection("tiktok-video-no-watermark2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    conn.request("GET", f"/comment/reply?video_id={video_id}&comment_id={comment_id}&count=20&cursor={cursor}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    result = json.loads(data)
    if result['msg'] == 'success':
        ids, text = extract_info(result['data']['comments'])
        comment_ids.extend(ids)
        comments.extend(text)
    if result['data']['cursor'] != '0':             
        getReplies(video_id=video_id, comment_id=comment_id, cursor=result['data']['cursor'], comment_ids=comment_ids, comments=comments)
    return pd.DataFrame({'id':comment_ids, 'comment': comments})

def searchTikTokVideos(region='ke', keywords='Adani',cursor=0, tiktoks=pd.DataFrame()):
    conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
    }
    
    conn.request("GET", f"/feed/search?keywords={keywords}&region={region}&count=30&cursor={cursor}&publish_time=0&sort_type=0", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    result = json.loads(data)
    try:
        df = pd.DataFrame(result['data']['videos'])
        df['username'] = [ i['unique_id'] for i in df['author'] ]
        df['profile_picture'] = [ i['avatar'] for i in df['author'] ]
        df['full_text'] = [ i for i in df['title'] ]
        tiktoks = pd.concat([tiktoks, df])
        tiktoks.to_csv("tiktok_videos.csv")
        cursor = result['data']['cursor']
        print(cursor)
        return searchTikTokVideos(region=region, keywords=keywords, cursor=cursor, tiktoks=tiktoks)
    except Exception as e:
        print(e)
        print(result['data']['cursor'])
        return tiktoks
def searchTikTokPhotos(region='ke', keywords='Adani',cursor=0, tiktoks=pd.DataFrame()):
    conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
    }
    
    conn.request("GET", f"/photo/search?keywords={keywords}&region={region}&count=30&cursor={cursor}&publish_time=0&sort_type=0", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    result = json.loads(data)
    try:
        df = pd.DataFrame(result['data']['videos'])
        df['username'] = [ i['unique_id'] for i in df['author'] ]
        df['profile_picture'] = [ i['avatar'] for i in df['author'] ]
        df['full_text'] = [ i for i in df['title'] ]
        tiktoks = pd.concat([tiktoks, df])
        tiktoks.to_csv("tiktok_photos.csv")
        cursor = result['data']['cursor']
        print(cursor)
        return searchTikTokVideos(region=region, keywords=keywords, cursor=cursor, tiktoks=tiktoks)
    except Exception as e:
        print(e)
        print(result['data']['cursor'])
        return tiktoks

def searchTikTokChallenge(region='ke', keywords='Adani',cursor=0, tiktoks=pd.DataFrame()):
    conn = http.client.HTTPSConnection("tiktok-scraper7.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "cb50110465msh7ab905f9be94fa7p1c6954jsn63ec422eb069",
        'x-rapidapi-host': "tiktok-scraper7.p.rapidapi.com"
    }
    
    conn.request("GET", f"/challenge/search?keywords={keywords}&region={region}&count=30&cursor={cursor}&publish_time=0&sort_type=0", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    result = json.loads(data)
    try:
        df = pd.DataFrame(result['data']['videos'])
        df['username'] = [ i['unique_id'] for i in df['author'] ]
        df['profile_picture'] = [ i['avatar'] for i in df['author'] ]
        df['full_text'] = [ i for i in df['title'] ]
        tiktoks = pd.concat([tiktoks, df])
        tiktoks.to_csv("tiktok_photos.csv")
        cursor = result['data']['cursor']
        print(cursor)
        return searchTikTokVideos(region=region, keywords=keywords, cursor=cursor, tiktoks=tiktoks)
    except Exception as e:
        print(e)
        print(result['data']['cursor'])
        return tiktoks