import pandas as pd
import sqlite3
from sklearn.linear_model import LogisticRegression
import pickle

conn = sqlite3.connect('loan.db')
data = pd.read_sql_query("SELECT * FROM history", conn)
conn.close()

if len(data) < 10:
    print("Need more data to train AI")
    exit()

data['approved'] = data['status'].apply(lambda x: 1 if x == "Approved" else 0)

X = data[['income','credit','loan','age']]
y = data['approved']

model = LogisticRegression()
model.fit(X,y)

pickle.dump(model, open('model.pkl','wb'))

print("AI trained using database")