from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import chartjs


views = Blueprint(__name__, "views")

# VIEW TO BE PLAYED WITH
@views.route("/play", methods=["POST","GET"])
def experiment():
    
    # simulate draw a barchart of sentiments
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    data = [12, 19, 3, 5, 2]
    
    # simulate parsing string returned from Reddit API and Sentiment Predictions 
    arr_text = ["Matt is charming", "When do you want to see Erica" ,"Ashis is disgusting", "Ayush hates grapes"]
    sentiment = ["positive", "positive", "negative", "negative"]
    
    prelim_result = zip(arr_text, sentiment)
    pos_ls_tp = []
    neg_ls_tp = []
    
    for tuple in prelim_result:
        if tuple[1] == "positive":
            pos_ls_tp.append(tuple)
        else:
            neg_ls_tp.append(tuple)
    
    date_time = datetime.now()
    return render_template("play.html", pos_content=pos_ls_tp, neg_content=neg_ls_tp, date=date_time, labels=labels, data=data)

@views.route("/", methods=["POST","GET"])
def home():
    return render_template("sent-form.html")

# RETURN JSON
@views.route("/json")
def get_json():
    return jsonify({"name": "John", "Coolness": 2/10})
    
# HOW TO ACCESS JSON DATA COMING TO A ROUTE (THIS CASE THE ROUTE IS "/DATA")
@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

# REDIRECT TO A DIFFERENT PAGE (THIS CASE )
@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))