from flask import Flask, render_template, request, jsonify
import json

from Exercises.bol import scrapeBol
from Exercises.coolblue import scrapeCool
from Exercises.github import scrapeGit
from Exercises.telenet import scrapeTelenet
from Exercises.ocean import scrapeOcean

from dateutil.relativedelta import relativedelta
import datetime

app = Flask(__name__, template_folder='./views')


@app.route("/")
def pageStart():
    return render_template('index.html')  

@app.route("/bolcomscraper/", methods=['POST'])
def appStartBol():
    data = request.data.decode("utf-8") 
    data = json.loads(data)
    try:
        scrapeBol(data['username'], data['password'], data['userId'], data['key'])      
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@app.route("/coolbluescraper/", methods=['POST'])
def appStartCool():
    data = request.data.decode("utf-8") 
    data = json.loads(data)
    try:
        scrapeCool(data['username'], data['password'], data['userId'], data['key'])
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@app.route("/githubscraper/", methods=['POST'])
def appStartGit():
    data = request.data.decode("utf-8") 
    data = json.loads(data)
    try:
        scrapeGit(data['username'], data['password'], data['userId'], data['key'])
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@app.route("/telenetscraper/", methods=['POST'])
def appStartTelenet():
    data = request.data.decode("utf-8") 
    data = json.loads(data)
    try:
        scrapeTelenet(data['username'], data['password'], data['userId'], data['key'])
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@app.route("/digitaloceanscraper/", methods=['POST'])
def appStartOcean():
    data = request.data.decode("utf-8") 
    data = json.loads(data)
    scrapeOcean(data['username'], data['password'], data['userId'], data['key'])
    return jsonify({'success': True})






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
