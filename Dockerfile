FROM python:3.12

WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /

EXPOSE 5000

ENV FLASK_APP=app.py
ENV DATABASE_URL="postgresql://financial:strx4012@localhost:5432/postgres"
ENV SECRET_KEY="qz27o8t5m9ocmufnafagnirm33ubc2sb"

CMD ["python", "./src/app.py"]
