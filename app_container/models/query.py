from app_container.services.query_services import QueryService


class Query:
    def __init__(self):
        self.queryService = QueryService()

    def create(self, query):
        if type(query['queries']) == list:
            query['queries'] = ",".join(query['queries'])
        return self.queryService.create_query(query)

    def get(self, query):
        return self.queryService.get_query(query)

    def fetch(self, query):
        return self.queryService.fetch_queries(query)
    
    def fetch_account_queries(self, query):
        return self.queryService.fetch_queries_account(query)

    def instaUserEngagement(self, query):
        return self.queryService.insta_user_engagement(query)
