#!/bin/sh
echo "[start.sh] Starting Streamlit app"

# Use Yandex Cloud's PORT environment variable or default to 8080
PORT=${PORT:-8080}
echo "[start.sh] Using port: $PORT"

streamlit run app.py --server.port $PORT --server.address 0.0.0.0
