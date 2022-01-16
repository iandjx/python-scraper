import os
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape import scrape_all

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("DB")
mongo = PyMongo(app).db


@app.route("/")
def index():
    mars = mongo.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.mars
    mars_data = scrape_all()
    mars.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect('/', code=302)
