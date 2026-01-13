-- 'users'라는 이름의 데이터베이스를 만듦, 만약 이미 'users'가 존재하면 그냥 넘어감
CREATE DATABASE IF NOT EXISTS `users`;    

-- 모든 GRANT ALL PRIVILEGES -> 모든 권한 부여(읽기, 쓰기, 수정, 삭제 등을 포함한 모든 권한)
-- On users.* -> users라는 데이터 베이스의 모든 테이블에 대한 권한을 부여, users.alpha면 users의 alpha 테이블에 대한 권한만 부한
-- TO 'dbuser' -> ubuser라는 사용자에게 권한을 부여함
-- @'localhost' -> 접속을 허용할 호스트(위치)를 제한하는 문구, 데이터베이스가 설치된 localhost(해당 컴퓨터 내부)에서만 접속할 수 있음
-- IDENTIFIED BY 'dbpass' -> users가 접속할 때 사용할 비밀번호는 'dbpass'임
GRANT ALL PRIVILEGES ON users.* TO 'dbuser'@'localhost' IDENTIFIED BY 'dbpass';

-- 위에서 users라는 데이터베이스를 생성했고, 지금부터 'users'라는 데이터베이스를 사용하겠다는 의미
USE `users`;
CREATE TABLE user(
  idx int auto_increment primary key, -- 숫자가 자동으로 1씩 증가하는 고유키 idx
  uid varchar(128) not null,          -- 128개의 글자를 저장할 수 있는 가변길이 문자열 uid
  upw varchar(128) not null           -- 128개의 글자를 저장할 수 있는 가변길이 문자열 upw
);

INSERT INTO user(uid, upw) values('admin', 'DH{**FLAG**}');
INSERT INTO user(uid, upw) values('guest', 'guest');
INSERT INTO user(uid, upw) values('test', 'test');
FLUSH PRIVILEGES;   -- 지금 수정한 권한 설정들을 메모리에 즉시 반영해라! 라는 뜻














