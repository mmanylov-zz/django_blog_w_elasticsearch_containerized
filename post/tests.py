from django.test import TestCase
from .models import Post
from .search import ES_INDEX_NAME
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections

connections.create_connection()


class PostModelTest(TestCase):
    fixtures = ['posts.json', ]

    def test_all_published_posts_indexed_with_elastic_search(self):
        """
        Checks if number of published posts in the DB and its titles is equal to the indexed ones in the ES
        """
        # get posts titles list from the DB
        db_posts_titles_list = list(Post.published.values_list('title', flat=True))

        # create ES client to get posts from the index
        es = Elasticsearch()
        # query all the indexed posts objects from the ES index
        es_res = es.search(index=ES_INDEX_NAME, body={"query": {"match_all": {}}})

        # access count of the found objects
        es_total = es_res['hits']['total']
        self.assertEqual(es_total, len(db_posts_titles_list),
                         "Number of posts in the DB is NOT equal to number of posts in the ES index")
        # check if ES and DB posts's titles match
        es_and_db_posts_titles_match = True
        # make a list of posts's titles received by querying the ES to compare against the ones from the DB
        es_res_titles_list = list(map(lambda x: x['_source']['title'], es_res['hits']['hits']))
        for db_posts_title in db_posts_titles_list:
            if db_posts_title not in es_res_titles_list:
                es_and_db_posts_titles_match = False
        self.assertTrue(es_and_db_posts_titles_match,
                        "ES and DB posts titles DO NOT match")
