import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from collections import OrderedDict
from flask import Flask, jsonify
import datetime as dt
import configparser

# Add in postgres credentials
parser = configparser.ConfigParser()
parser.read("credentials.conf")
host = parser.get("postgres_config" , "host_name")
db_name = parser.get("postgres_config" , "db_name")
user = parser.get("postgres_config" , "user")
password = parser.get("postgres_config" , "password")
port = parser.get("postgres_config" , "port")

### Create engine 
        ### Create a f string and pass it to a variable
        ### create engine 



conn_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
engine = create_engine(conn_string)

# Reflect apple_tv database into a model
Base = automap_base()
Base.prepare(autoload_with=engine) 

#Create references to class
titles = Base.classes.titles
credits = Base.classes.credits

# Flask Setup
app = Flask(__name__)
#Prevent flask from sorting  dictionary keys alphabetically
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def welcome():
    "List of available routes"
    return(
        f"Welcome to the Climate API! The available routes are:<br/>"
        f" <br/>"
        f"/api/v1.0/actors<br/>"
        f"<br/>"
        f"/api/v1.0/titles"
    )

# Create route to actors table
@app.route("/api/v1.0/actors")

def actors():
    session = Session(engine)

    results = session.query(titles.title , titles.release_year , titles.imdb_score , credits.name , credits.character)\
       .filter(titles.id == credits.title_id).all()

    session.close()



    actors = set([row[3] for row in results])

    actors_list = []

    for actor in actors:
        actors = {}
        actors['actor'] = actor
        movies_shows = []
        release_year = []
        characters = []
        imdb_scores = []
        for row in results:
            if row[3] == actor:
                movies_shows.append(row[0])
                release_year.append(row[1])
                characters.append(row[4])
                imdb_scores.append(row[2])


        actors['titles'] = movies_shows 
        actors['release_year'] = release_year
        actors['characters'] = characters
        actors['imdb_scores'] = imdb_scores
        
        actors_list.append(actors)

    return jsonify(actors_list)

# Create route to title table
@app.route("/api/v1.0/titles")

def movies_shows():

    session = Session(engine)
    
    results = session.query(titles.title , titles.release_year , titles.imdb_score , credits.name , credits.character ,titles.age_certification , titles.description)\
        .filter(titles.id == credits.title_id).all()

    session.close()

    movies_shows = set([row[0] for row in results])

    movies_shows_list = []

    for name in movies_shows:
        productions = {}
        productions['title'] = name
        actors = []
        release_year = set()
        rating = set()
        imdb_score = set()
        description = set()
        for row in results:
            if row[0] == name:
                actors.append(row[3])
                release_year.add(row[1])
                rating.add(row[5])
                imdb_score.add(row[2])
                description.add(row[6])

        productions['release_year'] = list(release_year)[0]
        productions['rating'] = list(rating)[0]
        productions['imdb_score'] = list(imdb_score)[0]
        productions['cast'] = actors
        productions['description'] = list(description)[0]
        movies_shows_list.append(productions)

    return jsonify(movies_shows_list)

##############################################################################
# Create Age Certification route
@app.route("/api/v1.0/age-certification")

def age_certification():
    session = Session(engine)

    results = session.query(titles.age_certification,
                            func.count(titles.age_certification),
                            titles.imdb_score)\
                                    .group_by(titles.age_certification).all()

    session.close()

    age_certification = set([row[0] for row in results])

    age_cert_list = []

    for loop in age_certification:
        age_dictionary = {}
        age_dictionary['age_certification'] = loop
        age_list = []
        age_count_list = []
        imdb_list = []
        age_dictionary['imdb_score'] = imdb_list
        for row in results:
            if row[0] == loop:
                age_list.append(row[1])
                age_count_list.append(row[2])
                imdb_list.append(row[3])

        avg_imdb_score = np.mean(imdb_list)
        imdb_list.append(avg_imdb_score)
        age_cert_list.append(age_dictionary)

##############################################################################

# The end of the app
if __name__ == '__main__':
    app.run(debug=True)

