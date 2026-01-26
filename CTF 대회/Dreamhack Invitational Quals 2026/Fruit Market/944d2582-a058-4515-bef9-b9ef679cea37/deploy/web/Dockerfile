FROM php:8.3-apache

COPY flag.txt /flag.txt         # flag.txt는 컨테니어 내부의 최상위 경로에 복사
COPY src/ /var/www/html/        # src디렉토리의 모든 파일을 /var/www/html/ 에 복사함

COPY zz-security.ini /usr/local/etc/php/conf.d/zz-security.ini      # zz-security.ini를 php 설정 디렉토리에 추가함

EXPOSE 80
