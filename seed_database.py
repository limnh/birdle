"""Script to seed database."""

import os
import json
import random
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
    continue
    sci_name, com_name, order, family_com_name, family_sci_name, bird_photo = (
        bird["sci_name"],
        bird["com_name"],
        bird["order"],
        bird["family_com_name"],
        bird["family_sci_name"],
        bird["bird_photo"]
    )

    db_bird = crud.create_bird(sci_name, com_name, order, family_com_name, family_sci_name, bird_photo)
    birds_in_db.append(db_bird)

model.db.session.add_all(birds_in_db)

selection = random.randint(1, len(bird_data))
db_answer = crud.create_answer(selection, date.today())
model.db.session.add(db_answer)
    
model.db.session.commit()
