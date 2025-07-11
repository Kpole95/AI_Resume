FROM python:3.10-slim
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm
ENV SENTENCE_TRANSFORMERS_HOME=/code/models
RUN mkdir -p /code/models
COPY ./api /code/api
COPY ./backend /code/backend
COPY ./config /code/config
COPY ./models /code/models
EXPOSE 8080
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]