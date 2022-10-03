from flask import Flask, render_template, request, redirect, url_for, current_app, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    items = db.relationship('Item', backref='item_user', lazy='dynamic')


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(120), unique=False, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<item {self.item}>'


db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/shopping_list')
def shopping_list():
    prices = 0
    items = db.session.query(Item).all()
    for item in items:
        prices += item.price
    return render_template("index.html", items=items, prices=prices)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_item = Item(
            item=request.form["item"],
            category=request.values["category"],
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

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':

        if User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        salted_hashed_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form['email'],
            password=salted_hashed_password,
            name=request.form['name']
        )
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)

        return redirect(url_for("shopping_list", name=new_user.name))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered.
        user = User.query.filter_by(email=email).first()

        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('shopping_list'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route("/logout")
def logout():

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
