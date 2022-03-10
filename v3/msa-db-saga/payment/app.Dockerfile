FROM python:3.9

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 3050

CMD ["python", "main.py"]