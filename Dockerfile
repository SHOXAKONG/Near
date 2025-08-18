FROM python:3.11

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgdal-dev \
      netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip wheel

COPY ./requirements.txt .

RUN pip install -r requirements.txt && \
    pip install "uvicorn[standard]"

COPY . /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000
