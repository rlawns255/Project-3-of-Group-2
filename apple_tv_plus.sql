DROP TABLE "titles";
DROP TABLE "credits";

CREATE TABLE "titles" (
	"id" varchar(30) PRIMARY KEY,
	"title" varchar(100),
	"type" varchar(5),
	"description" varchar,
	"release_year" int,
	"age_certification" varchar(10),
	"runtime" int,
	"genres" varchar(250),
	"production_countries" varchar(250),
	"seasons" real,
	"imdb_id" varchar,
	"imdb_score" real,
	"imdb_votes" real,
	"tmdb_popularity" real,
	"tmdb_score" real
);

CREATE TABLE "credits" (
	"person_id" int,
	"id" varchar, 
	"name" varchar,
	"character" varchar,
	"role" varchar
);

ALTER TABLE credits
ADD CONSTRAINT titles_fk FOREIGN KEY(id) REFERENCES titles(id)

SELECT * FROM credits;
SELECT * FROM titles;

----------------------
For Trey's computer
----------------------

DROP TABLE "titles";
DROP TABLE "credits";

CREATE TABLE "titles" (
	"id" varchar(30) PRIMARY KEY,
	"title" varchar(100),
	"type" varchar(5),
	"description" varchar,
	"release_year" int,
	"age_certification" varchar(10),
	"runtime" int,
	"genres" varchar(250),
	"production_countries" varchar(250),
	"seasons" real,
	"imdb_id" varchar,
	"imdb_score" real,
	"imdb_votes" real,
	"tmdb_popularity" real,
	"tmdb_score" real
);

CREATE TABLE "credits" (
	"person_id" int,
	"id" varchar, 
	"name" varchar,
	"character" varchar,
	"role" varchar
);


RENAME id TO title_id
ALTER TABLE credits
ADD CONSTRAINT titles_fk FOREIGN KEY(title_id) REFERENCES titles(id)

ALTER TABLE credits
ADD unique_id serial PRIMARY KEY

SELECT * FROM credits;
SELECT * FROM titles;
