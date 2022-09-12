from flask import Flask, render_template, request, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
import os
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f'<item {self.title}>'


db.create_all()


@app.route('/')
def home():
    items = db.session.query(Item).all()
    return render_template("index.html", items=items)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_item = Item(
            item=request.form["item"],
            category=request.form["category"],
            price=request.form["price"])
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":

        item_id = request.form["id"]
        item_to_update = Item.query.get(item_id)
        item_to_update.price = request.form["price"]
        db.session.commit()
        return redirect(url_for('home'))
    item_id = request.args.get('id')
    item_selected = Item.query.get(item_id)
    return render_template("edit_rating.html", item=item_selected)



@app.route("/delete")
def delete():
    item_id = request.args.get('id')
    item_to_delete = Item.query.get(item_id)
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
