import json


# Get the movie by its id
def movie_with_id(
    _, info, _id
):  # _ (first parameter) is the route since the route is Query than _ is written
    with open("{}/data/movies.json".format("."), "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                return movie


# Get the movie by its title
def movie_with_title(_, info, _title):
    with open("{}/data/movies.json".format("."), "r") as file:
        movies = json.load(file)
    for movie in movies["movies"]:
        if movie["title"] == _title:
            return movie


# Get all the movies with the given rate
def movies_with_rate(_, info, _rating):
    with open("{}/data/movies.json".format("."), "r") as file:
        movies = json.load(file)
        res = []
        for movie in movies["movies"]:
            if movie["rating"] == _rating:
                res.append(movie)
        return res


# Get all the movies
def movies(_, info):
    with open("{}/data/movies.json".format("."), "r") as file:
        movies = json.load(file)
        return movies["movies"]


# Update an existing movie
def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open("{}/data/movies.json".format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                movie["rating"] = _rate
                newmovie = movie
                newmovies = movies
    with open("{}/data/movies.json".format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


# Add a new movie
def add_movie(_, info, _movie):
    with open("{}/data/movies.json".format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _movie["id"]:
                return movie
    movies["movies"].append(_movie)
    with open("{}/data/movies.json".format("."), "w") as wfile:
        json.dump(movies, wfile)
    return _movie


# Remove an existing movie
def remove_movie(_, info, _id):
    removed_movie = {}
    with open("{}/data/movies.json".format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                removedmovie = movie
                movies["movies"].remove(movie)
    with open("{}/data/movies.json".format("."), "w") as wfile:
        json.dump(movies, wfile)
    return removed_movie


def actor_with_id(_, info, _id):
    with open("{}/data/actors.json".format("."), "r") as file:
        data = json.load(file)
    for actor in data["actors"]:
        if actor["id"] == _id:
            return actor


# Get the actors when we get a movie
def resolve_actors_in_movie(movie, info):
    with open("{}/data/actors.json".format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data["actors"] if movie["id"] in actor["films"]]
        return actors
