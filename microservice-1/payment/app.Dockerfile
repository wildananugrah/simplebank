FROM python:3.9

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 7040

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7040"]