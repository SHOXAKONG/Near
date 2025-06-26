FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY .env /app/.env

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000

CMD ["gunicorn", "src.core.wsgi:application", "--bind", "0.0.0.0:8000", "-w", "5"]