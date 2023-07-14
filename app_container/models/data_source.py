from app_container.services.data_source_service import DataSourceService


class DataSource:
    def __init__(self):
        self.dataSourceService = DataSourceService()

    def initialize(self, data_source_name, url, username, password, user_id):
        self.data_source_name = data_source_name
        self.url = url
        self.username = username
        self.password = password
        self.user_id = user_id

    def create(self, data_source):
        return self.dataSourceService.create_data_source(data_source)

    def get(self, data_source):
        return self.dataSourceService.get_data_source_by_id(data_source)

    def fetch(self, data_source):
        return self.dataSourceService.fetch_data_source_by_parameter(data_source)
