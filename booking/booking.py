from flask import Flask, request, jsonify, make_response
import json
import requests

app = Flask(__name__)

PORT = 3201
HOST = "0.0.0.0"

with open("{}/data/bookings.json".format("."), "r") as jsf:
    bookings = json.load(jsf)["bookings"]


@app.route("/", methods=["GET"])
def home():
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"


@app.route("/bookings", methods=["GET"])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res


@app.route("/bookings/<user_id>", methods=["GET"])
def get_booking_for_user(user_id):
    for booking in bookings:
        if str(booking["userid"] == str(user_id)):
            res = make_response(jsonify(booking), 200)
            return res
    return make_response(jsonify({"error": "User ID not found"}), 400)


@app.route("/bookings/<user_id>", methods=["POST"])
def add_booking_byuser(user_id):
    req = request.get_json()
    if "date" not in req or "movies" not in req:
        return make_response(jsonify({"error": "Invalid request data"}), 409)
    date = req["date"]
    movie_id_to_book = req["movies"]
    movies = requests.get(f"http://127.0.0.1:3202/showtimes/{date}").json()
    if movie_id_to_book not in movies["movies"]:
        return make_response(
            jsonify({"error": "movie ID was not found in showtimes"}), 409
        )
    for booking in bookings:
        if booking["userid"] == user_id:
            for dates in booking["dates"]:
                if dates["date"] == date:
                    if movie_id_to_book not in dates["movies"]:
                        dates["movies"].append(movie_id_to_book)
                    else:
                        return make_response(
                            jsonify({"error": "Movie ID already exists for the date."}),
                            409,
                        )
                else:
                    booking["dates"].append(
                        {"date": date, "movies": [movie_id_to_book]}
                    )
            return make_response(jsonify({"message": "Booking added"}), 200)
    new_booking = {
        "user_id": user_id,
        "dates": [{"date": date, "movies": [movie_id_to_book]}],
    }
    bookings.append(new_booking)
    with open("databases/bookings.json", "w") as jsf:
        json.dump({"bookings": bookings}, jsf)
    return make_response(jsonify({"message": "Booking added Successfully"}), 200)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
