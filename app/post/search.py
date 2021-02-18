from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
# from elasticsearch_dsl.query import MultiMatch
from blog.settings import ES_INDEX_NAME, ES_HOST_NAME, ES_PORT
from .models import PostType, Post

ES_SOCK = f'{ES_HOST_NAME}:{ES_PORT}'

connections.create_connection(hosts=[ES_SOCK])


def bulk_indexing():
    PostType.init()
    client = Elasticsearch(ES_SOCK)
    bulk(client=client, actions=(b.indexing() for b in Post.objects.all().iterator()))


def create_index():
    es = Elasticsearch(ES_SOCK)
    es.indices.create(index=ES_INDEX_NAME, ignore=400)


def init():
    create_index()
    bulk_indexing()


def drop_index():
    es = Elasticsearch(ES_SOCK)
    es.indices.delete(index=ES_INDEX_NAME, ignore=[400, 404])


def search(query):
    client = Elasticsearch(ES_SOCK)
    # mm= MultiMatch(query='python django', fields=['title', 'text', 'excerpt'])
    s = Search(using=client, index=ES_INDEX_NAME).query('multi_match', query=query, fields=['title', 'text', 'excerpt'])
    response = s.execute()
    return response
