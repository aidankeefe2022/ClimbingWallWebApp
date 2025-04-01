from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

boulder_grades = [{"grade" : "v"+str(x)} for x in range(0, 10)]
tr_grades = [{"grade" : "5."+str(x)} for x in range(5, 14)]
colors = [{"color":x} for x in ["pink","green","orange","yellow","red","blue","purple"]]



@app.route('/')
def hello_world():  # put application's code here
    data=boulder_data()
    setters = get_setters()
    return render_template("index.html", data=data, setters=setters, grades=boulder_grades, colors=colors)

@app.route('/TR')
def TR():
    tr = tr_data()
    setters = get_setters()
    return render_template("topRope.html", data=tr, setters=setters, grades=tr_grades, colors=colors)

@app.route('/admin')
def admin():
    setters = get_setters()
    return render_template("admin.html", users=setters)


@app.route('/addUser', methods=['POST'])
def addUser():
    name = request.form.get('name').lower().capitalize()
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    setters = get_setters()
    return render_template("user_table_row.html", users=setters)

@app.route('/chartInfo')
def chartInfo():
    data = boulder_data()
    if (len(data) == 0):
        return jsonify({})
    df = pd.DataFrame.from_dict(data)
    print(df)
    counts = df['grade'].value_counts().sort_index(ascending=False)
    print(counts)
    return jsonify(counts.to_dict())

@app.route('/insert', methods=['POST'])
def insert():
    name=request.form.get('name').lower()
    color = request.form.get('color').lower()
    setter = request.form.get('setter')
    grade = request.form.get('grade').lower()
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO boulders (name,color,setter,grade) VALUES (?,?,?,?)", (name, color, setter, grade))
    conn.commit()
    conn.close()

    data=boulder_data()

    return render_template("climb_table_row.html", data=data)
@app.route('/delete', methods=['DELETE'])
def delete():
    id = request.args.get('id')
    conn = sqlite3.connect('boulder.db')
    print(id)
    cur = conn.cursor()
    cur.execute("DELETE FROM boulders WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    data = boulder_data()

    return render_template("climb_table_row.html", data=data)

def get_setters():
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM users")
    data = []
    for row in res:
        data.append(
            {'id':row[0], 'name':row[1]}
        )
    conn.close()
    return data

def boulder_data():
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM boulders")
    data = []
    for row in res:
        print(row)
        data.append({
            'id': row[0], 'name': row[1], 'color': row[2], 'setter': row[3], 'grade': row[4]
        })
    conn.close()
    return data

def tr_data():
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM toprope")
    data = []
    for row in res:
        print(row)
        data.append({
            'id': row[0], 'name': row[1], 'color': row[2], 'setter': row[3], 'grade': row[4]
        })
    conn.close()
    return data


if __name__ == '__main__':
    app.run()
