from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Text, Date, Search, Short
from elasticsearch_dsl.query import MultiMatch
from . import models

ES_INDEX_NAME = 'blog-post-index'

connections.create_connection()

class PostIndex(DocType):
    published_at = Text()
    title = Text()
    body = Text()
    excerpt = Text()
    slug = Text()
    minutes_to_read = Short()
    
    class Meta:
        index = ES_INDEX_NAME


def bulk_indexing():
    PostIndex.init()
    client = Elasticsearch()
    bulk(client=client, actions=(b.indexing() for b in models.Post.objects.all().iterator()))

def search(query):
    client = Elasticsearch()
    s = Search(using=client)
    # mm= MultiMatch(query='python django', fields=['title', 'text', 'excerpt'])
    # s = Search()
    s = s.query("multi_match", query=query, fields=['title', 'text', 'excerpt'])
    response = s.execute()
    return response

def drop_index():
    es = Elasticsearch()
    es.indices.delete(index=ES_INDEX_NAME, ignore=[400, 404])