#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" App MAIN """

from app import create_app
from config import DevelopmentConfig
app = create_app(DevelopmentConfig)

# ##############################################
# #http://stackoverflow.com/a/9511655/2114395
# import os
# extra_dirs = ['app']
# extra_files = extra_dirs[:]
# for extra_dir in extra_dirs:
#     for dirname, dirs, files in os.walk(extra_dir):
#         for filename in files:
#             filename = os.path.join(dirname, filename)
#             if os.path.isfile(filename):
#                 extra_files.append(filename)
# #print(extra_files)

if __name__ == '__main__':
    host = app.config.get("HOST")
    port = app.config.get("PORT")
    app.run(host=host, port=port)#, extra_files=extra_files)
