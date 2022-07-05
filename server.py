"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from datetime import date
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")

@app.route("/all_birds")
def all_birds():
    birds = crud.get_all_birds()
    return render_template("all_birds.html", birds=birds)

@app.route("/birds/<bird_id>")
def show_bird(bird_id):
    """Show details on a particular bird."""

    bird = crud.get_bird(bird_id)

    return render_template("bird_details.html", bird=bird)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

        return redirect("/game")

@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)
    
@app.route("/game")
def test_answer():
    bird = crud.get_full_answer(date.today())
    print("Today's bird is", bird)
    return render_template("game.html", bird=bird)

@app.route("/submit-guess")
def check_answer():
    """Checks if user's guess is correct."""

    user_guess = request.args.get("guess")
    print("user_guess:", user_guess)
    answer = crud.get_full_answer(date.today())
    correct_guess = user_guess == answer.com_name
    logged_in_email = session.get("user_email")
    user = crud.get_user_by_email(logged_in_email)
    
    if crud.get_user_guesses(date.today(), user.user_id) >= 1000:
        return {"state": "game-over"}
    else:
        create_guess = crud.create_guess(date.today(), user.user_id, correct_guess)
        db.session.add(create_guess)
        db.session.commit()
    
    if correct_guess:
        return {"state": "correct"}
    else:
        return {"state": "incorrect"}
        

    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
