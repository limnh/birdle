"""Models for bird-guessing app, Birdle."""

from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Bird(db.Model):
    """A bird."""

    __tablename__ = "birds"

    bird_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sci_name = db.Column(db.String, unique=True)
    com_name = db.Column(db.String, unique=True)
    order = db.Column(db.String)
    family_sci_name = db.Column(db.String)
    family_com_name = db.Column(db.String)
    bird_photo = db.Column(db.String)
    # bird_call = db.Column(db.String)
    
    # answers = a list of Answer objects

    def __repr__(self):
        return f"<Bird bird_id={self.bird_id}, com_name={self.com_name}>"


class Answer(db.Model):
    """An answer."""

    __tablename__ = "answers"

    date = db.Column(db.Date, primary_key=True)
    bird_id = db.Column(db.Integer, db.ForeignKey("birds.bird_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    correct_answer = db.Column(db.Boolean)

    bird = db.relationship("Bird", backref="answers")
    
    # user = a single User object

    def __repr__(self):
        return f"<Answer date={self.date}, bird_id={self.bird_id}>"


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    streak = db.Column(db.Integer)

    answers = db.relationship("Answer", backref="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


def connect_to_db(flask_app, db_uri="postgresql:///birds", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    db.create_all()
