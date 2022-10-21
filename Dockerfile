FROM python:latest
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY mainscrap.py ./mainscrap.py




