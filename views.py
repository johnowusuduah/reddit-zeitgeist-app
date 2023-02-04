from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_caching import Cache
from decouple import config
from datetime import datetime
import requests
import praw
import json
import chartjs


views = Blueprint(__name__, "views")

# HOME VIEW
@views.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("views.callendpoint"))
    else:
        return render_template("home-form.html")


# VIEW TO BE PLAYED WITH
@views.route("/predict", methods=["POST","GET"])
def callendpoint():
    
    # PULL SUBMISSIONS FROM REDDIT API
    RED_CLIENT_ID = config('RED_CLIENT_ID')
    RED_CLIENT_SECRET = config('RED_CLIENT_SECRET')
    RED_USER_AGENT = config('RED_USER_AGENT')

    # praw object with credentials that returns reddit data
    reddit = praw.Reddit(
    client_id=RED_CLIENT_ID,
    client_secret=RED_CLIENT_SECRET,
    redirect_uri="http://localhost:8000",
    user_agent=RED_USER_AGENT)

    # fetch the 50 hottest submissions across all subreddits
    titles = set()
    for sub in reddit.subreddit("politics").hot(limit=50):
        titles.add(sub.title)

    # cast titles as list
    titles = list(titles)

    # payload of Reddit submissions to use for inference from sagemaker enpoint via API Gateway
    payload = {"text": titles}

    # make post request to AWS Sagemaker Endpoint
    headers = {'Content-Type': 'application/json'}
    response = requests.post("https://9le09xvq8l.execute-api.us-east-1.amazonaws.com/first-stage/sentiment", json=payload, headers=headers)

    # cast json response from AWS Lambda to dictionary
    sentiments = json.loads(response.json())
    
    # encode 0, 1 integer response to negative and postive strings, respectively
    parsed_sentiment = ["positive" if lbl == 1 else "negative" for lbl in sentiments['sentiment']]

    # pair submissions and predicted sentiments in an iterable of tuples
    result_tuple = zip(titles, parsed_sentiment)

    #prelim_result = zip(arr_text, sentiment)
    pos_ls_tp = []
    neg_ls_tp = []
    
    for tuple in result_tuple:
        if tuple[1] == "positive":
            pos_ls_tp.append(tuple)
        else:
            neg_ls_tp.append(tuple)
    
    date_time = datetime.now()
        
    # simulate draw a barchart of sentiments
    labels = ['Positive','Negative']
    data = [len(pos_ls_tp), len(neg_ls_tp)]

    return render_template("predict.html", pos_content=pos_ls_tp, neg_content=neg_ls_tp, date=date_time, labels=labels, data=data)

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