FROM python:latest

WORKDIR /app/

EXPOSE 8080
CMD [ "fastapi", "run", "main.py", "--port=8080" ]

COPY requirements.txt /install/
RUN pip install -r /install/requirements.txt \
    && pip install directory_tree \
    && apt-get update \
    && apt-get install -y  \
      ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    ;

COPY ./main.py /app/
COPY ./hydrus_ytdl_proxy  /app/hydrus_ytdl_proxy/

RUN python -m directory_tree \
    && echo "<[ cache breaker: 000 ]>"
