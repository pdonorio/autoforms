#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testing stuff
"""

import os
from sqlalchemy import create_engine

############################################
dbdriver = "postgresql"

# DB_NAME=/autoforms_web_1/db
# DB_ENV_POSTGRES_USER=myadmin
# DB_PORT=tcp://172.17.0.107:5432
# DB_PORT_5432_TCP_PORT=5432

dbhost = os.environ["DB_NAME"].split('/')[2]
dbport = int(os.environ["DB_PORT"].split(':')[2])
dbuser = os.environ["DB_ENV_POSTGRES_USER"]
dbpw = os.environ["DB_ENV_POSTGRES_PASSWORD"]

connection_string = "%s://%s:%s@%s:%d" \
    % (dbdriver, dbuser, dbpw, dbhost, dbport)


############################################
engine = create_engine(connection_string)
connection = engine.connect()
print("Connected")

############################################
# result = connection.execute("select username from users")
# for row in result:
#     print("username:", row['username'])
connection.close()

