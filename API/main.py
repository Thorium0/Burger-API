import flask
from flask import request, jsonify
import sqlite3


app = flask.Flask(__name__)
app.config["DEBUG"] = True
dbPath = "./db/burger.db"
baseURL = "/api/v1/"

subMenuTables = ["beverage", "burger"]
subBurgerTables = ["bun", "condiment", "meat", "salad"]
hasSubs = ["burger"]



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found. Blame Anders...</p>", 404


@app.route('/', methods=['GET'])
def home():
    return flask.render_template("index.html.j2", burgerParts=subBurgerTables)


@app.route(baseURL+'/menu-all', methods=['GET'])
def menu_all():
    conn = sqlite3.connect(dbPath)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM menu;").fetchall()
    return jsonify(result)


@app.route(baseURL+'/menu', methods=['GET'])
def menu_id():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id specified"

    conn = sqlite3.connect(dbPath)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM menu WHERE id = ?;", id).fetchall()

    return jsonify(result)


@app.route(baseURL+'/menu/<table>-all', methods=['GET'])
def sub_all(table):
    if table not in subMenuTables:
            return "Invalid table"
    conn = sqlite3.connect(dbPath)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    result = cur.execute("SELECT * FROM %s;" % table).fetchall()
    return jsonify(result)


@app.route(baseURL+'/menu/<table>', methods=['GET'])
def sub_id(table):
    if table not in subMenuTables:
            return "Invalid table"
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id specified"

    conn = sqlite3.connect(dbPath)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute("SELECT * FROM %s WHERE id = ?;" % table, id).fetchall()

    return jsonify(result)


@app.route(baseURL+'/menu/<table1>/<table2>-all', methods=['GET'])
def sub_sub_all(table1, table2):
    if table1 not in subMenuTables:
        return "Invalid sub-menu table"
    elif table1 not in hasSubs:
        return "Table has no sub tables"
    elif table2 not in subBurgerTables:
        return "Invalid sub-"+table1+" table"
    conn = sqlite3.connect(dbPath)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    if table2 == "meat":
        result = cur.execute("SELECT * FROM meat INNER JOIN meatType ON meatType.id = meat.TypeID;").fetchall()
    else:
        result = cur.execute("SELECT * FROM %s;" % table2).fetchall()
    return jsonify(result)


@app.route(baseURL+'/menu/<table1>/<table2>', methods=['GET'])
def sub_sub_id(table1, table2):
    if table1 not in subMenuTables:
        return "Invalid sub-menu table"
    elif table1 not in hasSubs:
        return "Table has no sub tables"
    elif table2 not in subBurgerTables:
        return "Invalid sub-"+table1+" table"

    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id specified"

    conn = sqlite3.connect(dbPath)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if table2 == "meat":
        result = cur.execute("SELECT * FROM meat INNER JOIN meatType ON meatType.id = meat.TypeID WHERE meat.id = ?;", id).fetchall()
    else:
        result = cur.execute("SELECT * FROM %s WHERE id = ?;" % table2, id).fetchall()

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000)
