FROM python:3.8

COPY . /app

WORKDIR /app

RUN apt-get install -y libxslt-dev

RUN pip install -r requirements.txt

CMD ["python", "main.py"]