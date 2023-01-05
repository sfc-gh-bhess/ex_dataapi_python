FROM python:3.8-slim
EXPOSE 8080
WORKDIR /app
COPY snow_rest .
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev g++
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]