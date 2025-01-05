FROM python:latest

WORKDIR /app/
COPY requirements.txt /install/
RUN pip install -r /install/requirements.txt \
    && apt-get update \
    && apt-get install -y  \
      ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    ;

COPY ./main.py ./utils /app/

EXPOSE 8080
CMD [ "fastapi", "run", "main.py", "--port=8080" ]

