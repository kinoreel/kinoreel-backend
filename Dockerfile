FROM python:3
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["manage.py runserver 0.0.0.0:8000"]