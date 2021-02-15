#!/bin/bash
# psql -U bloguser -h localhost -W blog < 2018-05-22.sql
cat dump/2018-05-22.sql | docker exec -i django_blog_real_db_1 psql -U bloguser -W blog