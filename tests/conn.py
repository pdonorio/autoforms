#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tests
"""

from sqlalchemy import create_engine
engine = create_engine('postgresql://myadmin:averYsecretpw@db:5432')

connection = engine.connect()
result = connection.execute("select username from users")
for row in result:
    print("username:", row['username'])
connection.close()

