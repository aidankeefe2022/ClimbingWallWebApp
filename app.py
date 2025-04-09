from flask import Flask, render_template, request, jsonify, make_response,  redirect, url_for
import sqlite3
import pandas as pd
from typing import Dict

app = Flask(__name__)


boulder_grades = [{"grade" : "v"+str(x)} for x in range(0, 10)]
tr_grades = [{"grade" : "5."+str(x)} for x in range(5, 14)]
colors = [{"color":x} for x in ["white","black","pink","green","orange","yellow","red","blue","purple"]]



@app.route('/')
def hello_world():  # put application's code here
    data=boulder_data()
    setters = get_setters()
    climb_type=""
    return render_template("index.html", data=data, setters=setters, grades=boulder_grades, colors=colors)


@app.route('/Boulder')
def boulder():
    data=boulder_data()
    setters = get_setters()
    climb_type=""

    html = render_template('boulder.html', data=data, setters=setters,grades=boulder_grades, colors=colors)
    resp = make_response(html)
    resp.headers['HX-Trigger-After-Swap'] =  '{"updateChartBoulder": ""}'
    resp.status_code = 200

    return resp

@app.route('/TR')
def TR():
    tr = tr_data()
    setters = get_setters()
    climb_type = "TR"
    html = render_template("topRope.html", data=tr, setters=setters, grades=tr_grades, colors=colors)
    resp = make_response(html)
    resp.headers['HX-Trigger-After-Swap'] =  '{"updateChartTR": ""}'
    resp.status_code = 200
    return resp


@app.route('/insertTR', methods=['POST'])
def TR_insert():
    name = request.form.get('name').lower()
    color = request.form.get('color').lower()
    setter = request.form.get('setter')
    grade = request.form.get('grade').lower()
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO toprope (name,color,setter,grade) VALUES (?,?,?,?)", (name, color, setter, grade))
    conn.commit()
    conn.close()

    data = tr_data()

    html = render_template("tr_table_row.html", data=data)
    resp = make_response(html)
    resp.headers['HX-Trigger-After-Swap'] =  '{"updateChartTR": ""}'
    resp.status_code = 200
    return resp

@app.route('/admin')
def admin():
    setters = get_setters()
    return render_template("admin.html", users=setters)

@app.route('/adminTR')
def adminTR():
    setters = get_setters()
    return render_template("admin_tr.html", users=setters)

@app.route('/addUser', methods=['POST'])
def addUser():
    name = request.form.get('name').lower().capitalize()
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    setters = get_setters()
    html = render_template("user_table_row.html", users=setters)
    resp = make_response(html)
    resp.headers["HX-Trigger-After-Swap"] = '{"formSubmit": ""}'
    resp.status_code = 200
    return resp

@app.route('/chartInfo')
def chartInfo():
    data = boulder_data()
    if (len(data) == 0):
        return jsonify({})
    df = pd.DataFrame.from_dict(data)
    print(df)
    counts = df['grade'].value_counts().sort_index(ascending=True)
    print(counts)
    return jsonify({
        'labels': list(counts.to_dict().keys()),
        'values': list(counts.to_dict().values())
    })

@app.route('/chartInfoTR')
def chartInfoTR():
    data = tr_data()
    if (len(data) == 0):
        return jsonify({})
    df = pd.DataFrame.from_dict(data)
    print(df)
    counts : Dict[str, int] = df['grade'].value_counts().to_dict()
    keys = list(counts.keys())
    keys.sort(key=lambda x: int(x.replace('.','')))
    print(keys)
    values = [counts[key] for key in keys]
    return jsonify({
        'labels': keys,
        'values': values
    })

@app.route('/insertBoulder', methods=['POST'])
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

    html = render_template("climb_table_row.html", data=data)
    resp = make_response(html)
    resp.headers["HX-Trigger-After-Swap"] =  '{"updateChartBoulder": ""}'
    resp.status_code = 200

    return resp
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

    html = render_template("climb_table_row.html", data=data)
    resp = make_response(html)
    resp.headers["HX-Trigger-After-Swap"] = '{"updateChartBoulder": ""}'
    resp.status_code = 200

    return resp

@app.route('/deleteTR', methods=['DELETE'])
def deleteTR():
    id = request.args.get('id')
    conn = sqlite3.connect('boulder.db')
    print(id)
    cur = conn.cursor()
    cur.execute("DELETE FROM toprope WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    data = tr_data()

    html = render_template("tr_table_row.html", data=data)
    resp = make_response(html)
    resp.headers['HX-Trigger-After-Swap'] =  '{"updateChartTR": ""}'
    resp.status_code = 200

    return resp

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

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    id = request.args.get('id')
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    data = get_setters()



    return render_template("user_table_row.html", users=data)

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
