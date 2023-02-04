import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import os

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://team-comunicaciones.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', 'OqJ3a4jFir4o9Kx71YbjY4QJxgSQKN6BhxMujjScYfD6WP8MzSN0NYDlV93YMKEVUyNnIjsJD319ACDbRyRFKg=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'TeamDB'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'Data2'),
}

def container_id(name):
    return os.environ.get('COSMOS_CONTAINER', name)


class Azure_db:

    def __init__(self):
        HOST = settings['host']
        MASTER_KEY = settings['master_key']
        DATABASE_ID = settings['database_id']
        CONTAINER_ID = settings['container_id']
        client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY}, user_agent="CosmosDBPythonQuickstart", user_agent_overwrite=True)
        self.db =client.get_database_client(DATABASE_ID)
        container = self.db.get_container_client(CONTAINER_ID)

    def create_container(self, container):
        name= container_id(container)
        container = self.db.create_container(id=name, partition_key=PartitionKey(path='/id'))
    
    def create_item(self, container, data):
        container = self.db.get_container_client(container)
        container.create_item(body= data)
    
    def read_item(self, container, id, ):
        container = self.db.get_container_client(container)
        response = container.read_item( item=id, partition_key=id)
        return response
    
    def read_items(self,container):
        container = self.db.get_container_client(container)
        items_list = list(container.read_all_items(max_item_count=10))
        return items_list
    
    def query_items(self, container, filters):
        container = self.db.get_container_client(container)
        query=f'SELECT * FROM c WHERE'
        for i in range (0, len(filters)):
            if i == 0:
                query = f'{query} c.{filters[i]["name"]} = "{filters[i]["value"]}"'
            else:
                query = f'{query} and c.{filters[i]["name"]} = "{filters[i]["value"]}"'
        items = list(container.query_items(query = query, enable_cross_partition_query=True))
        return items
