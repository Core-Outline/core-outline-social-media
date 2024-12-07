from app_container.repositories.snowflake import createClient, create, get, fetch
from config.data_source_config import data_source_table
from app_container.repositories import base64
import subprocess
import os


class DataSourceService():
    def __init__(self):
        self.db = createClient()

    def create_data_source(self, data_source):
        return create(self.db, data_source_table, data_source)

    def get_data_source_by_id(self, data_source):
        return get(self.db, data_source_table, data_source)

    def fetch_data_source_by_parameter(self, data_source):
        return fetch(self.db, data_source_table, data_source)
