from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    data=refresh_data()
    return render_template("index.html", data=data)

@app.route('/chartInfo')
def chartInfo():
    data = refresh_data()
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

    data=refresh_data()

    return render_template("table_row.html", data=data)
@app.route('/delete', methods=['DELETE'])
def delete():
    id = request.args.get('id')
    conn = sqlite3.connect('boulder.db')
    print(id)
    cur = conn.cursor()
    cur.execute("DELETE FROM boulders WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    data = refresh_data()

    return render_template("table_row.html", data=data)


def refresh_data():
    conn = sqlite3.connect('boulder.db')
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM boulders")
    data = []
    for row in res:
        print(row)
        data.append({
            'id': row[0], 'name': row[1], 'color': row[2], 'setter': row[3], 'grade': row[4]
        })
    return data


if __name__ == '__main__':
    app.run()
