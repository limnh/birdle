"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from datetime import date
from model import connect_to_db, db
from passlib.hash import argon2
from sqlalchemy.inspection import inspect
import crud

# constant for the number of allowed guesses before a game over
ALLOWED_GUESSES = 100

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
    hashed = argon2.hash(password)

    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, hashed)
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
    hashed = user.password

    if argon2.verify(password, hashed):
        session['user_email'] = user.email
        flash(f"Welcome back, {user.email}!")
        
    else:
        flash("The email or password you entered was incorrect.")
        return redirect('/')

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

    # compare user guess to answer
    guess      = request.args.get("guess")
    answer     = crud.get_full_answer(date.today())
    is_correct = guess.lower() == answer.com_name.lower()
    print("user_guess:", guess)
    
    # get the user object
    email = session.get("user_email")
    user  = crud.get_user_by_email(email)
    
    # add the guess to the database
    create_guess = crud.create_guess(date.today(), user.user_id, is_correct)
    db.session.add(create_guess)
    db.session.commit()
    
    num_guesses = crud.get_user_guesses(date.today(), user.user_id)
    if num_guesses >= ALLOWED_GUESSES:
        return {"success": False, "status": "game-over"}
    
    # get the guessed bird and convert to a dictionary so we can return it as JSON
    guess_bird  = crud.get_bird_by_name(guess)
    answer_bird = crud.get_bird_by_name(answer.com_name)

    answer_bird_dict = {c: getattr(answer_bird, c) for c in inspect(answer_bird).attrs.keys()}
    print("answer_bird:", answer_bird_dict)

    resp = {
        "success": is_correct,
        "answer": {c: getattr(answer_bird, c) for c in inspect(answer_bird).attrs.keys()},
        "guess": {c: getattr(guess_bird, c) for c in inspect(guess_bird).attrs.keys()},
        "guesses": num_guesses,
    }
    
    if is_correct:
        return resp | {"status": "You named the bird correctly!"}
    else:
        return resp | {"status": f"You didn't get it correct. You've used {num_guesses} guesses!"}
        

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
