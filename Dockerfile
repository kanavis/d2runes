FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY web /app/
COPY runewords.json /app/
COPY runes.txt /app
RUN python /app/manage.py migrate
RUN python /app/manage.py load_runes runes.txt runewords.json

