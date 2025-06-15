FROM python:3.10-slim

# the working directory inside the container
WORKDIR /code

# Copy requirements file and install all necessary packages
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Download the spaCy NLP models during the build process
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm

# pre download and cache the Sentence Transformer model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')"

# copy your application's source code into the container
COPY ./api /code/api
COPY ./backend /code/backend
COPY ./config /code/config

# set the port the container will listen on
EXPOSE 8000

# the command to run your FastAPI server when the container starts
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
