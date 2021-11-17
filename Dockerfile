FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY web /app/
COPY d2runes.json /app/
COPY runes.txt /app
RUN /app/manage.py load_runes runes.txt runewords.json

