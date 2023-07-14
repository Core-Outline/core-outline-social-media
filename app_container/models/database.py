from app_container.repositories.database import createClient, create, get, fetch


class Database():
    def __init__(self) -> None:
        pass

    def createDBClient(self):
        return createClient()

    def create(self, document):
        return create(document)

    def get(self, condition):
        return get(condition)

    def fetch(self, array_of_conditions):
        return fetch(array_of_conditions)
