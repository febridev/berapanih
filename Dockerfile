FROM python:latest
WORKDIR /app
RUN mkdir -p /app/export
COPY mainscrap.py mainscrap.py
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python", "mainscrap.py" ]

