import configparser
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

from sqlalchemy import create_engine, func
from collections import OrderedDict
from flask import Flask, jsonify
import datetime as dt
import configparser
from flask_cors import CORS


# Add in postgres credentials
parser = configparser.ConfigParser()
parser.read("credentials.conf")
host = parser.get("postgres_config", "host_name")
db_name = parser.get("postgres_config", "db_name")
user = parser.get("postgres_config", "user")
password = parser.get("postgres_config", "password")
port = parser.get("postgres_config", "port")

# Create engine & f-string, pass it to a variable
conn_string =\
    f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
engine = create_engine(conn_string)

# Reflect apple_tv database into a model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Create references to class
titles = Base.classes.titles
credits = Base.classes.credits

# Flask Setup
app = Flask(__name__)
CORS(app)

# Prevent flask from sorting  dictionary keys alphabetically
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# Design app routes


@app.route("/")
def welcome():

    return(
        f"Welcome to the apple_tv API! The available routes are:<br/>"
        f" <br/>"

    return (
        f"{'Welcome to the Apple TV+ API! The available routes are:<br/>'}"
        f"<br/>"

        f"/api/v1.0/actors<br/>"
        f"<br/>"
        f"/api/v1.0/titles<br/>"
        f"<br/>"
        f"/api/v1.0/age-certification<br/>"
        f"<br/>"
        f"/api/v1.0/genres<br/>"
    )

# Create route to actors table


@app.route("/api/v1.0/actors")
def actors():
    session = Session(engine)

    # Query the actors table
    results = session.query(titles.title,
                            titles.release_year,
                            titles.imdb_score,
                            credits.name,
                            credits.character).filter(
                                titles.id == credits.title_id).all()

    # Close the session
    session.close()


    actors_list = []

    actors = set([row[3] for row in results])
    actor_data = {}
    actor_data['names'] = list(actors)
    metadata = []

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

        # Append the actors to the list
        actors['titles'] = movies_shows
        actors['release_year'] = release_year
        actors['characters'] = characters
        actors['imdb_scores'] = imdb_scores

        
        metadata.append(actors)
    actor_data['metadata'] = metadata


    return jsonify(actor_data)

# Create a route to titles table


@app.route("/api/v1.0/titles")
def movies_shows():

    # Create a session
    session = Session(engine)

    # Query all the movies and shows
    results = session.query(titles.title,
                            titles.release_year,
                            titles.imdb_score,
                            credits.name,
                            credits.character,
                            titles.age_certification,
                            titles.description).filter(
                                titles.id == credits.title_id).all()

    # Close the session
    session.close()

    # Create a set of movies and shows
    movies_shows = set([row[0] for row in results])


    titles_data = {}
    titles_data['titles'] = list(movies_shows)

    movies_shows_data = []


    # Loop through the movies and shows
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

        # Append the movies and shows to the list
        productions['release_year'] = list(release_year)[0]
        productions['rating'] = list(rating)[0]
        productions['imdb_score'] = list(imdb_score)[0]
        productions['cast'] = actors
        productions['description'] = list(description)[0]
        movies_shows_data.append(productions)
        titles_data['metadata'] = movies_shows_data

    return jsonify(titles_data)

# Create Age Certification route


@app.route("/api/v1.0/age-certification")
def age_cert():
    session = Session(engine)

    results = session.query(titles.title,
                            titles.release_year,
                            titles.imdb_score,
                            titles.age_certification,
                            titles.description)

    session.close()

    age_cert = set([row[3] for row in results])

    age_cert_list = []

    for age in age_cert:
        age_dictionary = {}
        age_dictionary['age_certification'] = age
        age_title = []
        age_release_year = []
        age_imdb_score = []
        age_description = []
        for row in results:
            if row[3] == age:
                age_title.append(row[0])
                age_release_year.append(row[1])
                age_imdb_score.append(row[2])
                age_description.append(row[4])

        age_dictionary['titles'] = age_title
        age_dictionary['release_year'] = age_release_year
        age_dictionary['imdb_score'] = age_imdb_score
        age_dictionary['description'] = age_description
        age_cert_list.append(age_dictionary)

    return jsonify(age_cert_list)

# Create a route to genres table


@app.route("/api/v1.0/genres")
def genres():
    session = Session(engine)

    # Query all the genres
    results = session.query(titles.genres,
                            func.avg(titles.imdb_score),
                            func.max(titles.imdb_score)
                            ).filter(titles.id == credits.title_id).group_by(titles.genres).all()

    session.close()

    genres = set([row[0] for row in results])

    genres_list = []

    # Loop through the genres and append them to the list
    for genre in genres:
        genres = {}
        genres['genre'] = genre
        imdb_scores = []
        for row in results:
            if row[0] == genre:
                imdb_scores.append(row[1])


        genres['imdb_scores'] = imdb_scores
        genres_list.append(genres)

    return jsonify(genres_list)

# Run the app


if __name__ == '__main__':
    app.run(debug=True)
