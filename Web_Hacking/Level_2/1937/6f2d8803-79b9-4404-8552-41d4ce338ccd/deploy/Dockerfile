FROM python:3.9-slim

# ENV
ENV port 8000


RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-pip wget curl unzip gnupg2 apt-utils ca-certificates \
 && install -m 0755 -d /etc/apt/keyrings \
 && curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /etc/apt/keyrings/google-linux-signing-key.gpg \
 && chmod a+r /etc/apt/keyrings/google-linux-signing-key.gpg \
 && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends google-chrome-stable \
 && apt-get purge -y --auto-remove gnupg \
 && rm -rf /var/lib/apt/lists/*

# Fetch the latest ChromeDriver version matching the installed Google Chrome version
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+') && \
    wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

# Set up application
ADD ./ /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Create uploads directory
RUN mkdir -p /app/uploads && chmod -R 777 /app/uploads

# Expose port
EXPOSE $port

ENTRYPOINT ["python3"]
CMD ["app.py"]
