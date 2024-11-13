from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
from twitter import searchUserPostsTwitter, searchKeywordsTwitter, getUserDetails
import snowflake.connector
import os
import time
import json

load_dotenv()

def createClient(schema_name):
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=schema_name
    )
    cur = conn.cursor()

    return conn, cur

def collectTwitterAccountQueries():
    yesterday = str(datetime.now() - timedelta(days=1))
    conn, cur = createClient(os.getenv('SNOWFLAKE_CORE_SCHEMA'))
    df = pd.read_sql("SELECT QUERIES FROM query WHERE type='twitter_account'",con=conn)
    df_ = pd.DataFrame()
    for i in df['QUERIES'].values:
        time.sleep(10)
        _ = searchUserPostsTwitter(i, yesterday)
        df_ = pd.concat([df_, _])
        time.sleep(10)
    df_.to_csv("safcom_user_tweets.csv")

def collectTwitterSearchQueries():
    yesterday = str(datetime.now() - timedelta(days=1))
    conn, cur = createClient(os.getenv('SNOWFLAKE_CORE_SCHEMA'))
    df = pd.read_sql("SELECT QUERIES FROM query WHERE type='twitter_search'",con=conn)
    df_ = pd.DataFrame()
    for i in df['QUERIES'].values:
        df_ = pd.concat([df_, searchKeywordsTwitter(i, yesterday)]) 
        time.sleep(10)
    df_.to_csv("safcom_tweets.csv")

def collectAccountData():
    conn, cur = createClient(os.getenv('SNOWFLAKE_CORE_SCHEMA'))
    df = pd.read_sql("SELECT QUERIES FROM query WHERE type='twitter_account'",con=conn)
    df_ = pd.DataFrame()
    for i in df['QUERIES'].values:
        df_ = pd.concat([ df_ ,pd.DataFrame(getUserDetails(username=i)) ])
    return df_.to_csv("twitter_user.csv")

# collectTwitterSearchQueries()
collectTwitterAccountQueries()
