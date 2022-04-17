FROM python:3.10

WORKDIR /project

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.main:app", "--host",  "0.0.0.0"]
