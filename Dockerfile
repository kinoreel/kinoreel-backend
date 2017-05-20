FROM python:3
USER root
COPY . /app
WORKDIR /app
RUN chmod +x start.sh
RUN pip install -r requirements.txt
CMD ["./start.sh"]