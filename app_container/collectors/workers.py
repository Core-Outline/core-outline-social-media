from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
from twitter import searchUserPostsTwitter, searchKeywordsTwitter
import snowflake.connector
import os
import time

load_dotenv()

def createClient():
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )
    cur = conn.cursor()

    return conn, cur

def collectTwitterAccountQueries():
    yesterday = str(datetime.now() - timedelta(days=1))
    conn, cur = createClient()
    df = pd.read_sql("SELECT QUERIES FROM query WHERE type='twitter_account'",con=conn)
    print(df)
    for i in df['QUERIES'].values:
        time.sleep(10)
        _ = searchUserPostsTwitter(i, yesterday)
        time.sleep(10)

def collectTwitterSearchQueries():
    yesterday = str(datetime.now() - timedelta(days=1))
    conn, cur = createClient()
    df = pd.read_sql("SELECT QUERIES FROM query WHERE type='twitter_search'",con=conn)
    df_ = pd.DataFrame()
    for i in df['QUERIES'].values:
        df_ = pd.concat([df_, searchKeywordsTwitter(i, yesterday)]) 
        time.sleep(10)
    df_.to_csv("safcom_tweets.csv")

collectTwitterSearchQueries()
# collectTwitterAccountQueries()