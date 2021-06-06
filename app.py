from flask import Flask, render_template, redirect, url_for, request, logging, flash, session, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import click
import os
import data_process

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
db = SQLAlchemy(app)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(80), nullable=False)
    packWeight = db.Column(db.Float, nullable=False)
    minPackWeight = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False) # Unit of package weight
    price = db.Column(db.Float, nullable=False)
    minPackPrice = db.Column(db.Float, nullable=False)  # Price of the minimum package
    minPackProtein = db.Column(db.Float, nullable=True) # Amount of protein in each minimum package
    proteinUnit = db.Column(db.String(10), nullable=True)   # Unit of protein
    minPackCarbohydrate = db.Column(db.String(20), nullable=True)
    carbohydrateUnit = db.Column(db.String(10), nullable=True)
    minPackFiber = db.Column(db.String(20), nullable=True)
    fiberUnit = db.Column(db.String(10), nullable=True)
    minPackFat = db.Column(db.String(20), nullable=True)
    fatUnit = db.Column(db.String(10), nullable=True)
    minPackSodium = db.Column(db.String(20), nullable=True)
    sodiumUnit = db.Column(db.String(10), nullable=True)
    # allergic = db.Column(db.String(50), nullable=True)    # Should be a list of allergic sources, causing problem so commented out temporarily. Need to be fixed
    vegetables = db.Column(db.Boolean, nullable=False)  # Whether it is vegetables
    liquid = db.Column(db.Boolean, nullable=False)  # Whether it is liquid
    snacks = db.Column(db.Boolean, nullable=False)
    fruit = db.Column(db.Boolean, nullable=False)
    meat = db.Column(db.Boolean, nullable=False)
    grain = db.Column(db.Boolean, nullable=False)
    source = db.Column(db.String(50), nullable=True)    # Where to buy the product
    brand = db.Column(db.String(50), nullable=True)     # The brand of the product

    # Temporary defined for testing purpose, need to be modified
    def __repr__(self):
        text = ''
        for key, val in self.__dict__.items():
            text += f'{key}:     {val}'
            text += '<br />'
        return text



# read in and convert the sample data into SQL database. Set drop to be True if 
# want to clean the previous database
def initdb(drop=False):
    """Initialize the database."""
    if drop: db.drop_all()
    db.create_all()
    df = data_process.read_csv_file('food_data.csv')
    for ind, row in df.iterrows():
        food = Food(id = row['Item number'],
                    itemName = row['Item name'],
                    packWeight = row['Package Weight'],
                    minPackWeight = row['Minimum Package Weight'],
                    unit = row['Unit'],
                    price = row['Price'],
                    minPackPrice = row['Minimum Package Price'],
                    proteinUnit = row['Protein Unit'],
                    minPackProtein = row['Minimum Package Protein'],
                    carbohydrateUnit = row['Carbohydrate Unit'],
                    minPackCarbohydrate = row['Minimum Package Carbohydrate'],
                    fiberUnit = row['Fiber Unit'],
                    minPackFiber = row['Minimum Package Fiber'],
                    fatUnit = row['Fat Unit'],
                    minPackFat = row['Minimum Package Fat'],
                    sodiumUnit = row['Sodium Unit'],
                    minPackSodium = row['Minimum Package Sodium'],
                    # allergic = row['Allergic'],
                    vegetables = row['Liquid'],
                    liquid = row['Vegetables'],
                    snacks = row['Snacks'],
                    fruit = row['Fruit'],
                    meat = row['Meat'],
                    grain = row['Grain'],
                    brand = row['Brand'],
                    source = row['Source']
                    )
        db.session.add(food)
    db.session.commit()


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
