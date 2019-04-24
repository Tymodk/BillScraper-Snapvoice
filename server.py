from flask import Flask, render_template, request, jsonify
import json

from Exercises.bol import scrapeBol
from Exercises.coolblue import scrapeCool

from dateutil.relativedelta import relativedelta
import datetime

app = Flask(__name__, template_folder='./views')


@app.route("/")
def pageStart():
    return render_template('index.html')  

@app.route("/bolscraper/<username>/<password>")
def appStartBol(username, password):
    try:
        scrapeBol(username, password)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@app.route("/coolscraper/<username>/<password>")
def appStartCool(username, password):
    try:
        scrapeCool(username, password)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
