"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime, date

import crud
import model
import server

os.system("dropdb birds")
os.system("createdb birds")

model.connect_to_db(server.app)
model.db.create_all()

# Load bird data from JSON file
with open("data/testbirds.json") as f:
    bird_data = json.loads(f.read())

# Create birds, store information in list so we can use them
# to create fake entries
birds_in_db = []
for bird in bird_data:
    sci_name, com_name, order, family_com_name, family_sci_name, bird_photo = (
        bird["sci_name"],
        bird["com_name"],
        bird["order"],
        bird["family_com_name"],
        bird["family_sci_name"],
        bird["bird_photo"]
    )
    # release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_bird = crud.create_bird(sci_name, com_name, order, family_com_name, family_sci_name, bird_photo)
    birds_in_db.append(db_bird)

model.db.session.add_all(birds_in_db)

db_answer = crud.create_answer(3, date.today())
model.db.session.add(db_answer)
    
model.db.session.commit()



# Create 10 users
#for n in range(10):
 #   email = f"user{n}@test.com"  # Voila! A unique email!
  #  password = "test"
#
 #   user = crud.create_user(email, password)
  #  model.db.session.add(user)

# model.db.session.commit()