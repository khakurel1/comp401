# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /api
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5174
COPY . .
CMD ["python", "main.py"]
