# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 17:27:12 2020

@author: Chris
"""

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_CJM

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    info = mongo.db.info.find_one()
    return render_template("index.html", info=info)

@app.route("/scrape")
def scraper():
    info = mongo.db.info
    info_data = scrape_mars_CJM.scrape()
    info.update({}, info_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)