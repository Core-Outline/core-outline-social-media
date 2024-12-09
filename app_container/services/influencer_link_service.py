from app_container.repositories.snowflake import createClient, create, get, fetch, fetch_account_queries
from config.query_config import query_actions, queries_table, influencer_link_table
from config.rebrandly_config import rebrandly_api, rebrandly_base_url
from app_container.services.data_source_service import DataSourceService
# from app_container.repositories.selenium import instagram_user_engagement
from app_container.repositories.request import post
import pandas as pd
import subprocess


class InfluencerLinkService():
    def __init__(self):
        self.db = createClient()

    def create_influencer_link(self, influencer_link):
        influencer_link['redirect_url'] = f"https://data.coreoutline.com/update-conversions/{influencer_link['query_id']}"
        influencer_link['shortened_link'] = post(
            url=rebrandly_base_url, 
            data={
                "destination": influencer_link['redirect_url']
            },
            headers={
                "apikey": rebrandly_api
            },
            params={}
        )['shortUrl']
        return create(self.db, influencer_link_table, influencer_link)

    def get_influencer_link(self, influencer_link):
        return get(self.db, influencer_link_table, influencer_link)

    def fetch_influencer_link(self, influencer_link):
        return fetch(self.db, influencer_link_table, influencer_link)
    
    def fetch_influencer_link_account(self, account):
        return fetch_account_queries(self.db, influencer_link_table, account)


    # def insta_user_engagement(self, query):
    #     dataSourceService = DataSourceService()
    #     dataSource = dataSourceService.get_data_source_by_id(query)

    #     if(dataSource['subtype'] == 'instagram'):
    #         data = instagram_user_engagement(dataSource['username'])

    #     return data
