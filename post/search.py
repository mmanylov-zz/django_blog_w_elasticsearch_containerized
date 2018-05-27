from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Text, Date, Search, Short
from elasticsearch_dsl.query import MultiMatch
from . import models

connections.create_connection()

class PostIndex(DocType):
    posted_date = Date()
    title = Text()
    body = Text()
    excerpt = Text()
    slug = Text()
    minutes_to_read = Short()
    
    class Meta:
        index = 'post-index'


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