import os
from flask import Flask, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'user')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'pass')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'users')
mysql = MySQL(app)

template ='''
<pre style="font-size:200%">SELECT * FROM user WHERE uid='{uid}';</pre><hr/>
<form>
    <input tyupe='text' name='uid' placeholder='uid'>
    <input type='submit' value='submit'>
</form>
'''

@app.route('/', methods=['POST', 'GET'])
def index():
    uid = request.args.get('uid')
    if uid:
        try:
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT * FROM user WHERE uid='{uid}';")
            return template.format(uid=uid)
        except Exception as e:
            return str(e)
    else:
        return template


if __name__ == '__main__':
    app.run(host='0.0.0.0')

# SQL-Injection을 조금 아는 게 아니면 풀기 힘드네요
# https://velog.io/@son030331/%EC%9B%8C%EA%B2%8C%EC%9E%84-%EB%93%9C%EB%A6%BC%ED%95%B5-error-based-sql-injectionchallenges-412
# 위 링크가 도움이 될듯


# USE `users`;
# CREATE TABLE user(
#   idx int auto_increment primary key, -- 숫자가 자동으로 1씩 증가하는 고유키 idx
#   uid varchar(128) not null,          -- 128개의 글자를 저장할 수 있는 가변길이 문자열 uid
#   upw varchar(128) not null           -- 128개의 글자를 저장할 수 있는 가변길이 문자열 upw
# );

# INSERT INTO user(uid, upw) values('admin', 'DH{**FLAG**}');
# INSERT INTO user(uid, upw) values('guest', 'guest');
# INSERT INTO user(uid, upw) values('test', 'test');


# ' and extractvalue(1, concat(0x5c, database()));

