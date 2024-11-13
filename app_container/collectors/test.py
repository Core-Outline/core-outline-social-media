import pandas as pd

df= pd.read_csv("sf_tweets.csv")

print(df['created_at'])