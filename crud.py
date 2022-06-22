"""CRUD operations."""

from model import db, Bird, Answer, User, connect_to_db


def create_bird(sci_name, com_name, order, family_com_name, family_sci_name, bird_photo):
    """Create and return a new bird."""

    bird = Bird(sci_name=sci_name, com_name=com_name, order=order, family_com_name=family_com_name, family_sci_name=family_sci_name, bird_photo=bird_photo)

    return bird

def get_all_birds():
    """Return a bird's common name."""

    return Bird.query.all()

def get_bird(bird_id):
    """Return a bird's common name."""

    return Bird.query.get(bird_id)

def get_answer(date):
    """Returns answer for given date."""
    return Answer.query.get(date)

def create_answer(bird_id, date):
    """Creates an answer."""
    answer = Answer(bird_id=bird_id, date=date)
    return answer

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()
    

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
