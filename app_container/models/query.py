from app_container.services.query_services import QueryService


class Query:
    def __init__(self):
        self.queryService = QueryService()

    def create(self, query):
        return self.queryService.create_query(query)

    def get(self, query):
        return self.queryService.get_query(query)

    def fetch(self, query):
        return self.queryService.fetch_query_by_parameter(query)

    def execute(self, query):
        return self.queryService.execute_query(query)
