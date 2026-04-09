import sqlite3

def create_db():
    conn = sqlite3.connect('loan.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        age INTEGER,
        income INTEGER,
        credit INTEGER,
        loan INTEGER,
        status TEXT
    )
    ''')

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect('loan.db')
    c = conn.cursor()
    c.execute("INSERT INTO users(username,password) VALUES(?,?)",(username,password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('loan.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    user = c.fetchone()
    conn.close()
    return user

def save_history(username, age, income, credit, loan, status):
    conn = sqlite3.connect('loan.db')
    c = conn.cursor()
    c.execute("INSERT INTO history(username,age,income,credit,loan,status) VALUES(?,?,?,?,?,?)",
              (username,age,income,credit,loan,status))
    conn.commit()
    conn.close()

def get_history(username):
    conn = sqlite3.connect('loan.db')
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE username=?",(username,))
    data = c.fetchall()
    conn.close()
    return data