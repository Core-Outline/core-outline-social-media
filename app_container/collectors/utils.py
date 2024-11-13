import boto3
import pandas as pd
from io import BytesIO
import os
from elasticsearch import Elasticsearch
import json
from dotenv import load_dotenv

load_dotenv()
es = Elasticsearch([{'host': 'localhost', 'port': 9200,'scheme': "http"}])

def upload_dataframe_to_s3_parquet(df, bucket_name, s3_key, aws_access_key, aws_secret_key, region='us-east-1'):
    buffer = BytesIO()
    df.to_parquet(buffer, engine='pyarrow', index=False)
    buffer.seek(0)

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body=buffer.getvalue())

    print(f"Data uploaded to s3://{bucket_name}/{s3_key}")


def load_df_to_es(df, source):
    index_name = source
    data = df.to_dict(orient='records')
    [es.index(index=index_name, id=i, body=doc) for i, doc in enumerate(data)]