from flask_app import app, bcrypt
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User


@app.get("/")
def index():

    return render_template("index.html")


@app.post("/users/register")
def register():
    """This route processes the register form."""

    if not User.register_form_is_valid(request.form):
        return redirect("/")

    portential_user = User.find_by_email(request.form["email"])

    if portential_user != None:
        flash("Email in use. Please log in.")
        return redirect("/")

    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    user_id = User.register(user_data)
    session["user_id"] = user_id
    return redirect("/users/dashboard")


@app.post("/users/login")
def login():
    """This route processes the login form."""

    if not User.login_form_is_valid(request.form):
        return redirect("/")

    return redirect("/users/dashboard")


@app.get("/users/dashboard")
def dashboard():
    """This route displays the users dashboard"""
    return render_template("dashboard.html")


@app.post("/users/logout")
def logout():
    session.clear()
    return redirect("/")
