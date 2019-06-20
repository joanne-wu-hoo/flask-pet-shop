"""Flask application for a pet store: can view and add pets."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from db import Pet

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"

toolbar = DebugToolbarExtension(app)

@app.route("/")
def list_pets():
    """ Show list of pets from database on the landing page """
    pet_list = Pet.get_all()
    return render_template("show-pet-list.html", pets=pet_list)

@app.route("/add-pet")
def show_add_pet_form():
    """ Shows form to add a new pet to the database """
    return render_template("add-pet-form.html")

@app.route("/add-pet", methods=["POST"])
def handle_new_pet():
    """ When the new pet info form is submitted:
    - get inputed data about the new pet
    - add the new pet's info to the database 
    - redirect user to homepage (and flash confirmation)
    """   
    pet_name = request.form["name"]
    pet_age = request.form["age"]
    pet_color = request.form["color"]
    pet_photo = request.form["photo"]

    Pet.add(pet_name, pet_color, pet_age, pet_photo)
    
    flash("Pet information added!") # flash msg added to show-pet-list.html
    return redirect("/")

@app.route("/pets/<id_of_pet>")
def show_pet(id_of_pet):
    """ Show pet information. If pet not found, redirect to homepage (and flash error msg) """
    pet_info = Pet.find_by_id(id_of_pet)

    if (pet_info):
        return render_template("show-pet.html", pet=pet_info)
    else:
        flash("Pet not found") # flash msg added to show-pet-list.html
        return redirect("/")
