FROM python:3.10-slim-bookworm@sha256:66a6e8a211a02794515d4e1aa1970fc037ec4dde1429395e1321bdd63af01256

# ENV
ENV user warp
ENV port 8000

# chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl gnupg unzip ca-certificates apt-transport-https \
    fonts-liberation libasound2 libatk1.0-0 libc6 libcairo2 libcups2 \
    libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libglib2.0-0 libgtk-3-0 \
    libnspr4 libnss3 libpango-1.0-0 libu2f-udev libx11-6 libx11-xcb1 \
    libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxi6 \
    libxrandr2 libxrender1 libxss1 libxtst6 libdrm2 libgbm1 \
 && install -m 0755 -d /etc/apt/keyrings \
 && wget -qO- https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /etc/apt/keyrings/google.gpg \
 && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update && apt-get install -y --no-install-recommends google-chrome-stable \
 && rm -rf /var/lib/apt/lists/*

# chromedriver
RUN set -eux; \
    CHROME_VERSION="$(google-chrome --version | awk '{print $3}')" ; \
    MAJOR="${CHROME_VERSION%%.*}" ; \
    LATEST="$(curl -s https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${MAJOR})" ; \
    echo "Chrome: $CHROME_VERSION  |  Major: $MAJOR  |  CFT: $LATEST" ; \
    curl -fSL "https://storage.googleapis.com/chrome-for-testing-public/${LATEST}/linux64/chromedriver-linux64.zip" -o /tmp/chromedriver.zip ; \
    unzip -q /tmp/chromedriver.zip -d /opt/chromedriver ; \
    mv /opt/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver ; \
    chmod +x /usr/local/bin/chromedriver ; \
    rm -rf /opt/chromedriver /tmp/chromedriver.zip

# SET challenges
RUN adduser $user
ADD ./deploy /app
WORKDIR /app
RUN pip3 install -r requirements.txt

RUN chown root:$user /app/flag.txt

# RUN
USER $user
EXPOSE $port
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER=/usr/local/bin/chromedriver

ENTRYPOINT ["python3"]
CMD ["app.py"]
