from flask import Flask, request, jsonify
from Util.sqlQuery import SqlQuery
from Util.exceptions import *
from settings import *

app = Flask(__name__)
sqlQuery = SqlQuery(MINIME_DB_PATH)

def run(debug = False):
    app.run(host = "0.0.0.0", port = PORT, debug = debug)

@app.route('/query')
def query():
    card = request.args.get('card')
    tableName = request.args.get('table')
    try:
        data = sqlQuery.query_data(card, tableName)
    except SQLQueryException as err:
        return jsonify(err.resp)
    return jsonify(data)

@app.route('/items')
def items():
    card = request.args.get('card')
    action = request.args.get('action')
    item_id = request.args.get('item_id')
    item_count = request.args.get('item_count')
    try:
        data = sqlQuery.item_operation(card, action, item_id, item_count)
    except SQLQueryException as err:
        return jsonify(err.resp)
    return jsonify(data)

@app.route('/userInfo')
def userInfo():
    card = request.args.get('card')
    user_name = request.args.get('user_name')
    team_name = request.args.get('team_name')
    try:
        data = sqlQuery.mod_user_info(card, user_name, team_name)
    except SQLQueryException as err:
        return jsonify(err.resp)
    return jsonify(data)
