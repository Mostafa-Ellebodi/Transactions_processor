FROM python:3.8.16-slim-buster
RUN apt-get update && \
    apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install -U pip
WORKDIR /app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
