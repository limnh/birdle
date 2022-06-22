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
    
@app.route("/test_answer")
def test_answer():
    answer = crud.get_answer(date.today())
    return answer

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
