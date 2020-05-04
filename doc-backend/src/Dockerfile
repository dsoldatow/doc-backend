FROM python:3.6-stretch

WORKDIR /app

COPY app /app
#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "service.py"]
