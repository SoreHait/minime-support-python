from flask import Flask, request, jsonify
from sqlQuery import SqlQuery
from settings import *


app = Flask(__name__)
sqlQuery = SqlQuery(MINIME_DB_PATH)

def run(debug = False):
    app.run(host = "0.0.0.0", port = PORT, debug = debug)

@app.route('/query')
def query():
    card = request.args.get('card')
    tableName = request.args.get('table')
    return jsonify(sqlQuery.query_data(card, tableName))
