from app_container.repositories.database import createClient, create, get, fetch
from config.query_config import query_actions, queries_table
from app_container.services.data_source_service import DataSourceService
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

    def execute_query(self, query):
        dataSourceService = DataSourceService()
        dataSource = dataSourceService.get_data_source_by_id(query)
        latestCommit = dataSource['commit']
        subprocess.run(['bash', 'dvc_usage.sh', latestCommit])
        queries = query.queries

        data = pd.read_csv('app/scripts/file.csv')
        for q in queries:
            column = q.keys[0]
            operation = q[column].keys[0]
            value = q[column][operation]

            data = data.loc[query_actions[operation](data[column], value)]

        return data
