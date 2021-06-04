from flask import Flask, render_template, redirect, url_for, request, logging, flash, session, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    session.clear()
    return render_template('index.html')

@app.after_request
def add_header(r):
    """
    This code disable caching in Flask.
    This behaviour is convenient for development because when refreshing the webpage,
    cached versions of CSS and JS files are loaded instead of the most recent versions.
    Code from: https://stackoverflow.com/questions/47376744/how-to-prevent-cached-response-flask-server-using-chrome
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# Example trigger
@app.route("/additem", methods=['POST'])
def AddItem():
    """
    Expects request parameters in the form of ?itemName={string}
    """
    if request.method == 'POST':
        food_item = request.args.get('itemName')
        
        # Retrieve food item here. IDK how to work with excel/csv in python nor do I currently have our storage format
        food_obj = 1 
        # Expecting an object at the end here
        return jsonify(food_obj)
    
@app.route("/getall", methods=['get'])
def AddItem():
    if request.method == 'GET':
        # TODO
    return None

@app.route("/findfoodcombination", methods=['POST'])
def FindRandomFoodCombination():
    if request.method == 'POST':
        # TODO
    return None


if __name__ == '__main__':
    app.run(debug=True)
