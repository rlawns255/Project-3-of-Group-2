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
        movie_titles = []
        release_year = []
        characters = []
        imdb_scores = []
        for row in results:
            if row[3] == actor:
                movie_titles.append(row[0])
                release_year.append(row[1])
                characters.append(row[4])
                imdb_scores.append(row[2])


        actors['movies'] = movie_titles 
        actors['release_year'] = release_year
        actors['characters'] = characters
        actors['imdb_scores'] = imdb_scores
        
        actors_list.append(actors)

    return jsonify(actors_list)


if __name__ == '__main__':
    app.run(debug=True)
