from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_info

@app.route('/scrape')
def scrape():
    latestMarsData = scrape_mars.scrape()
    print("\n\n\n")
    db.mars_info.insert_one(latestMarsData)
    return "Scrappin' the data..."

@app.route("/")
def home():
    latestMarsData = list(db.mars_info.find())
    print(latestMarsData)
    return render_template("index.html", latestMarsData = latestMarsData)

if __name__ == "__main__":
    app.run(debug=True)