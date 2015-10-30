#!/bin/bash

sleep 8

echo "Launching python multi-thread server"
gunicorn -k meinheld.gmeinheld.MeinheldWorker -b 0.0.0.0:5000 -w4 run:app
