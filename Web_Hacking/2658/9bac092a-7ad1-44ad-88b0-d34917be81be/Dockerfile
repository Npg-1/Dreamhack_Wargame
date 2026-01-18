FROM python:3.9-slim

#**redacted**
#**redacted**
#**redacted**

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .
COPY Secrets.txt .

EXPOSE 8000
CMD ["python", "app.py"]
