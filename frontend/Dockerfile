FROM python:3.10-slim
WORKDIR /app
COPY ./frontend/frontend-requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./frontend /app
RUN chmod +x /app/start.sh
EXPOSE 8080
CMD ["/app/start.sh"]