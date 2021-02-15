#!/bin/bash
#d=$(date +%Y-%m-%d)
#pg_dump -U bloguser -h localhost -W blog > $d.sql
docker exec -t django_blog_real_db_1 pg_dumpall -c -U bloguser > dump_`date '+%d-%m-%Y_%H_%M_%S'`.sql