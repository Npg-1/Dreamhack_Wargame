FROM python:3.11-slim

WORKDIR /app

RUN pip install flask
COPY app.py /app/
COPY templates /app/templates
COPY flag /flag

EXPOSE 5000

CMD ["python", "app.py"]
