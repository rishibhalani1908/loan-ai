from flask import Flask,render_template,request,redirect,session,jsonify
import sqlite3
import os
from model import check_loan
from database import create_db

app = Flask(__name__)
app.secret_key="123"

create_db()

# REGISTER
@app.route('/register',methods=['POST'])
def register():
    conn=sqlite3.connect('loan.db')
    c=conn.cursor()
    c.execute("INSERT INTO users(username,password) VALUES(?,?)",
              (request.form['username'],request.form['password']))
    conn.commit()
    conn.close()
    return redirect('/')

# LOGIN
@app.route('/login',methods=['POST'])
def login():
    conn=sqlite3.connect('loan.db')
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (request.form['username'],request.form['password']))
    user=c.fetchone()
    conn.close()

    if user:
        session['user']=request.form['username']
        return redirect('/dashboard')
    return "Invalid Login"

# HOME
@app.route('/')
def home():
    return render_template('login.html')

# DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# PREDICT
@app.route('/predict',methods=['POST'])
def predict():
    data=request.get_json()

    res=check_loan(int(data['income']),int(data['credit']),
                   int(data['loan']),int(data['age']))

    # SAVE DATA
    conn=sqlite3.connect('loan.db')
    c=conn.cursor()
    c.execute("INSERT INTO history(username,age,income,credit,loan,status) VALUES(?,?,?,?,?,?)",
              (session['user'],data['age'],data['income'],data['credit'],data['loan'],res['status']))
    conn.commit()
    conn.close()

    # AUTO TRAIN
    os.system("python train_model.py")

    return jsonify(res)

# HISTORY
@app.route('/history')
def history():
    conn=sqlite3.connect('loan.db')
    c=conn.cursor()
    c.execute("SELECT * FROM history WHERE username=?",(session['user'],))
    data=c.fetchall()
    conn.close()
    return render_template('history.html',data=data)

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)