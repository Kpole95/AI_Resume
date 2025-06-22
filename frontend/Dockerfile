FROM python:3.10-slim
<<<<<<< HEAD

WORKDIR /app

COPY ./frontend/frontend-requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./frontend /app

RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]
=======
WORKDIR /app
COPY ../requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app
EXPOSE 8080
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
>>>>>>> f3e9499a61ba98af25341bb3fad9afc203e9b957
