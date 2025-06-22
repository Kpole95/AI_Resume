FROM python:3.10-slim
WORKDIR /code
<<<<<<< HEAD

# Copy the requirements file
=======
>>>>>>> f3e9499a61ba98af25341bb3fad9afc203e9b957
COPY ./requirements.txt /code/requirements.txt

# [OPTIMIZATION] Install the large PyTorch library first from its official source.
# This can be more reliable and sometimes faster than getting it from the general package index.
# We are installing the CPU-only version which is slightly smaller.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Now, install the rest of your requirements. Pip will see that torch is
# already installed and skip it, which speeds up this step.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
<<<<<<< HEAD

# Download the spaCy NLP models
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm

# [NEW] Set an environment variable to tell the sentence-transformers library
# where to find its cache of models inside the container.
ENV SENTENCE_TRANSFORMERS_HOME=/code/models

# [NEW] This ensures the directory for the models exists.
RUN mkdir -p /code/models

# Copy your application's source code and the downloaded model into the container
COPY ./api /code/api
COPY ./backend /code/backend
COPY ./config /code/config
COPY ./models /code/models

# Set the port the container will listen on
EXPOSE 8080

# The command to run your FastAPI server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
=======
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ru_core_news_sm
COPY ./api /code/api
COPY ./backend /code/backend
COPY ./config /code/config
EXPOSE 8080
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]

>>>>>>> f3e9499a61ba98af25341bb3fad9afc203e9b957
