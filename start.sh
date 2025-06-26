#!/bin/bash
echo "Started by VØAT for Aaru Babe..."
gunicorn app:app &
GUNICORN_PID=$!
python main.py
wait $GUNICORN_PID
