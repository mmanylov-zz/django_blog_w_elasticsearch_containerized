#!/bin/bash
d=$(date +%Y-%m-%d)
pg_dump -U bloguser -h localhost -W blog > $d.sql
