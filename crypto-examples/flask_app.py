import sys
import time
import json
import sqlite3
from flask import Flask, g
from flask import render_template

app = Flask(__name__)

SLEEP = None
if len(sys.argv) > 2:
    print("=" * 60)
    try:
        SLEEP = int(sys.argv[-1])
        print(f"Each request will be delayed by {SLEEP} seconds")
    except ValueError:
        print("Invalid sleep parameter.")
    print("=" * 60)

@app.before_request
def before_request():
    g.db = sqlite3.connect('prices.db')


@app.teardown_request
def teardown_request_func(error=None):
    g.db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exchanges')
def exchanges():
    cursor = g.db.execute("SELECT DISTINCT exchange FROM price ORDER BY exchange ASC;")
    results = cursor.fetchall()
    exchanges = [exc for sub in results for exc in sub]
    return json.dumps(exchanges), 200, {'Content-Type': 'application/json'}


@app.route('/symbols')
def symbols():
    cursor = g.db.execute("SELECT DISTINCT symbol FROM price ORDER BY symbol ASC;")
    results = cursor.fetchall()
    symbols = [exc for sub in results for exc in sub]
    return json.dumps(symbols), 200, {'Content-Type': 'application/json'}


@app.route('/price/<exchange>/<symbol>/<date>')
def price(exchange, symbol, date):
    time.sleep(.2)
    g.db.row_factory = sqlite3.Row
    cursor = g.db.execute("""
        SELECT exchange, symbol, open, high, low, close, volume, day FROM price
        WHERE exchange = ? AND symbol = ? AND day = ?;
    """, (exchange, symbol, date))
    results = [dict(r) for r in cursor.fetchall()]
    result = None
    if len(results):
        result = results[0]
    if SLEEP:
        time.sleep(SLEEP)
    return json.dumps(result), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.debug = True
    app.run()