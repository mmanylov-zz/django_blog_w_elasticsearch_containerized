from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Text, Date, Search
from . import models

connections.create_connection()

class PostIndex(DocType):
    posted_date = Date()
    title = Text()
    text = Text()
    excerpt = Text()

    class Meta:
        index = 'post-index'


def bulk_indexing():
    PostIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))

def search(query):
    s = Search().filter('term', text=query)
    response = s.execute()
    return response