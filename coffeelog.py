#!/usr/bin/python
# encoding=utf8

from flask import Flask, render_template, flash, request
from flask_pymongo import MongoClient
from wtforms import Form, TextField, DateField, DateTimeField, IntegerField, SelectField, RadioField, DecimalField, validators, SubmitField
import ast, datetime, json

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# MongoDB config
client = MongoClient('mongodb://localhost:27017/')
db = client.coffeelogdb

class ReusableForm(Form):
    date = DateField('Date:', default=datetime.date.today, validators=[validators.DataRequired()])
    time = DateTimeField('Time:', default=datetime.datetime.now, format='%H:%M:%S', validators=[validators.DataRequired()])
    cups = IntegerField('Cups:', default='1', validators=[validators.DataRequired()])
    drink = SelectField('Drink:', default='filter', choices=[('americano','Americano'), ('espresso','Espresso'), ('filter','Filter'), ('fw','Flat White'), ('machiatto', 'Machiatto'), ('v60','V60'), ('other', 'Other')], validators=[validators.DataRequired()])
    notes = TextField('Notes:', validators=[validators.DataRequired()])
    shop = TextField('Shop:')
    cost = DecimalField('Cost:', places=2)
    rating = RadioField('Rating:', default='3', choices=[('1','One'),('2','Two'),('3','Three'),('4','Four'),('5','Five')], validators=[validators.DataRequired()])

def mongoInput(jsonobj):
    result = db.coffees.insert(ast.literal_eval(jsonobj))
    return (result)

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        date=request.form['date']
        time=request.form['time']
        cups=request.form['cups']
        drink=request.form['drink']
        notes=request.form['notes']
        shop=request.form['shop']
        cost=request.form['cost']
        rating=request.form['rating']
        print date
        print time
        print cups
        print drink
        print notes
        print shop
        print cost
        print rating

        if form.validate():
            # Save the comment here.
            flash('You drank ' + cups +' cups of '+ drink + ' on ' + date + ' at ' + time + ', and rated it ' + rating + ' stars.')
            flash('This coffee was bought from ' + shop + ' for ' + cost)
            flash('Your notes about the drink: ' + notes)
            # Build json document
            jsonData = json.dumps({'version':'1.0', 'date': date, 'time': time, 'cups': cups, 'drink':drink, 'notes':notes, 'shop':shop, 'cost':cost, 'rating':rating})
            # Input JSON data
            a = mongoInput(jsonData)
            flash(jsonData)
            flash(a)
        else:
            flash('Make sure all required fields are filled. ')

    return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run()
