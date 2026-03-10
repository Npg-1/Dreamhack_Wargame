import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.urandom(32)

def init_db():
    conn = sqlite3.connect('secret_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,         # id는 고유 식별자임
            username TEXT UNIQUE,           # 중복된 값 허용 X
            password TEXT                   # 중복된 값 허용
        )
    ''')


    cursor.execute('''
        CREATE TABLE secret_data (
            id INTEGER,
            title TEXT,
            content TEXT,
            is_confidential INTEGER
        )
    ''')
    
    # admin, (모르는 헥사값 16자리)
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('admin', '{os.urandom(8).hex()}')")

    

    dummy_data = [
        ('Project Alpha', 'Top secret military project', 1),            # 얘는 기밀임
        ('Budget Report', 'Annual financial report', 0),
        ('Employee List', 'Company employee directory', 0),
        ('Security Protocol', 'Network security guidelines', 1),        # 얘도 기밀임
        ('Meeting Minutes', 'Weekly team meeting notes', 0)
    ]
    
    for title, content, is_confidential in dummy_data:
        cursor.execute("INSERT INTO secret_data (title, content, is_confidential) VALUES (?, ?, ?)", 
                      (title, content, is_confidential))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query', '')
        
        conn = sqlite3.connect('secret_data.db')
        cursor = conn.cursor()
        
        sql = f"SELECT COUNT(*) FROM secret_data WHERE title LIKE '%{query}%'"
        
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            conn.close()
            
            if result[0] > 0:
                return render_template('search.html', message="Found! Data exists in our records.", query=query)
            else:
                return render_template('search.html', message="Not found! No matching data.", query=query)
        except Exception as e:
            conn.close()
            return render_template('search.html', message="Not found! No matching data.", query=query)
    
    return render_template('search.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('secret_data.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')





@app.route('/admin')
def admin():
    if 'user_id' not in session:
        flash('Please login to access admin panel!', 'error')
        return redirect(url_for('login'))
    
    try:
        with open('flag.txt', 'r') as f:
            flag = f.read().strip()
    except:
        flag = "DH{testflag}"
    
    return render_template('admin.html', flag=flag, username=session.get('username'))



@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=False)