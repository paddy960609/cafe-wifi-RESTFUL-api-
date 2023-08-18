# display cafes, add and delete them

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import random
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# migrate = Migrate(app, db)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    # date = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.String, nullable=False)
    has_wifi = db.Column(db.String, nullable=False)
    has_sockets = db.Column(db.String, nullable=False)
    can_take_calls = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    # def to_dict(self):
    #     # Method 1.
    #     dictionary = {}
    #     # Loop through each column in the data record
    #     for column in self.__table__.columns:
    #         # Create a new dictionary entry;
    #         # where the key is the name of the column
    #         # and the value is the value of the column
    #         dictionary[column.name] = getattr(self, column.name)
    #     return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}
with app.app_context():
    db.create_all()
class CreateCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    map_url = StringField("Cafe Location URL", validators=[DataRequired(), URL()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    seats = SelectField('Any Seat?', choices=["Yes there are", "No there are not"], validators=[DataRequired()])
    has_toilet = SelectField("Any toilets?", choices=["Yes there are", "No there are not"], validators=[DataRequired()])
    has_wifi = SelectField("Any wifi?", choices=["Yes there is", "No there is not"], validators=[DataRequired()])
    has_sockets = SelectField("Any sockets?", choices=["Yes there are", "No there are not"], validators=[DataRequired()])
    can_take_calls = SelectField("Can I take calls?",choices=["Yes you can", "No you cannot"], validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Submit Cafe")

@app.route("/")
def home():
    cafes = Cafe.query.all()
    return render_template("index.html", all_cafes=cafes)


@app.route("/post/<int:cafe_id>", methods=["GET", "POST"])
def show_cafe(cafe_id):
    requested_cafe = Cafe.query.get(cafe_id)

    return render_template("cafe.html", cafe=requested_cafe)


## HTTP POST - Create Record
@app.route("/add", methods=["GET", "POST"])
def post_new_cafe():
    form = CreateCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,

            img_url=form.img_url.data,
            map_url=form.map_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data,

        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("make-cafe.html", form=form)
## HTTP PUT/PATCH - Upf Record
@app.route("/update-price/<int:cafe_id>", methods=["GET","POST"])
def update_data(cafe_id):
    current_cafe = Cafe.query.get(cafe_id)
    edited_cafe = CreateCafeForm(
        name=current_cafe.name,
        location = current_cafe.location,
        map_url = current_cafe.map_url,
        img_url = current_cafe.img_url,
        seats = current_cafe.seats,
        has_toilet = current_cafe.has_toilet,
        has_wifi = current_cafe.has_wifi,
        has_sockets = current_cafe.has_sockets,
        can_take_calls = current_cafe.can_take_calls,
        coffee_price = current_cafe.coffee_price
    )
    if edited_cafe.validate_on_submit():
        current_cafe.name = edited_cafe.name.data
        current_cafe.location = edited_cafe.location.data
        current_cafe.map_url = edited_cafe.map_url.data
        current_cafe.img_url = edited_cafe.img_url.data
        current_cafe.seats = edited_cafe.seats.data
        current_cafe.has_toilet = edited_cafe.has_toilet.data
        current_cafe.has_wifi = edited_cafe.has_wifi.data
        current_cafe.has_sockets = edited_cafe.has_sockets.data
        current_cafe.can_take_calls = edited_cafe.can_take_calls.data
        current_cafe.coffee_price = edited_cafe.coffee_price.data

        db.session.commit()
        return redirect(url_for('show_cafe', cafe_id=current_cafe.id))
    return render_template("make-cafe.html", form=edited_cafe, is_edit=True)


## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["GET", "DELETE"])
def delete_data(cafe_id):
    cafe_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
