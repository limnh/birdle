"""CRUD operations."""

from model import db, Bird, Answer, User, connect_to_db


def create_bird(sci_name, com_name, order, family_com_name, family_sci_name, bird_photo):
    """Create and return a new bird."""

    bird = Bird(sci_name=sci_name, com_name=com_name, order=order, family_com_name=family_com_name, family_sci_name=family_sci_name, bird_photo=bird_photo)

    return bird


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
    

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
