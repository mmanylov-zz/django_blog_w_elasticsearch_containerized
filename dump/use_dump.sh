#!/bin/bash
pg_dump -U bloguser -h localhost -W blog < <file_name_here>.sql
