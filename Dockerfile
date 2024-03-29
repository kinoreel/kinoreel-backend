FROM python:3.6-slim
USER root
ARG PG_SERVER
ARG PG_PORT
ARG PG_DB
ARG PG_USERNAME
ARG PG_PASSWORD
ARG ALLOWED_HOST
ENV PG_SERVER $PG_SERVER
ENV PG_PORT $PG_PORT
ENV PG_DB $PG_DB
ENV PG_USERNAME $PG_USERNAME
ENV PG_PASSWORD $PG_PASSWORD
ENV ALLOWED_HOST $ALLOWED_HOST
COPY . /app
WORKDIR /app
RUN chmod +x start.sh
RUN pip install -r requirements.txt
CMD ["./start.sh"]