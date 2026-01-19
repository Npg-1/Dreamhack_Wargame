FROM python:3.9-slim

#**redacted**
#**redacted**
#**redacted**

# 명령어들이 실행 될 작업폴더를 /app 으로 지정하는 코드
WORKDIR /app    

# 내 컴퓨터의 requierments.txt를 도커의 현재 폴더로 복사함
COPY requirements.txt .
# requirements.txt를 보고 파이썬 라이브러리를 설치함
RUN pip install --no-cache-dir -r requirements.txt

# 내 컴퓨터의 app을 도커의 현재 폴더로 복사함
COPY app .
# 내 컴퓨터의 app을 도커의 현재 폴더로 복사함
COPY Secrets.txt .

# 이 어플리케이션이 사용할 포트가 8000임을 명시함
EXPOSE 8000
# 컨테이너가 실행될 때 마지막으로 수행할 명령으로 터미널에서 'python app.py'를 입력하여 서버를 띄우는 것과 같음
CMD ["python", "app.py"]