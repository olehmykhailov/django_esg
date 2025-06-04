FROM python:3.10.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080  


WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



COPY project/ ./


ENV PYTHONPATH=/app


RUN python manage.py collectstatic --noinput --clear


EXPOSE 8080  

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 project.wsgi:application
