from app_container.repositories.database import createClient, create, get, fetch
from config.query_config import query_actions, queries_table
from app_container.services.data_source_service import DataSourceService
from app_container.repositories.selenium import instagram_user_engagement
import pandas as pd
import subprocess


class QueryService():
    def __init__(self):
        self.db = createClient()

    def create_query(self, query):
        return create(self.db, queries_table, query)

    def get_query(self, query):
        return get(self.db, queries_table, query)

    def fetch_queries(self, query):
        return get(self.db, queries_table, query)

    def insta_user_engagement(self, query):
        dataSourceService = DataSourceService()
        dataSource = dataSourceService.get_data_source_by_id(query)

        if(dataSource['subtype'] == 'instagram'):
            data = instagram_user_engagement(dataSource['username'])

        return data
