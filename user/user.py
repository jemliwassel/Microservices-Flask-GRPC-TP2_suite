# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
# import grpc
# from concurrent import futures
# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)

PORT = 3004
HOST = "0.0.0.0"

with open("{}/data/users.json".format("."), "r") as jsf:
    users = json.load(jsf)["users"]


# root message
@app.route("/help", methods=["GET"])
def help():
    return make_response(
        render_template("help.html", body_text="Welcome to the User service"), 200
    )


@app.route("/user/<user_id>", methods=["GET"])
def get_user_infos(user_id):
    for user in users:
        if user["id"] == user_id:
            res = make_response(jsonify(user), 200)
            return res
    return make_response(jsonify({"error": "User was not found"}), 400)


# Get reservations (Bookings) by user_id and date
@app.route("/user/reservations/<user_id>", methods=["GET"])
def get_user_reservation(user_id):
    reservation_date = request.get_json().get("date")
    all_reservations_for_user = requests.get(
        f"http://127.0.0.1:3201/bookings/<user_id>", params={user_id: user_id}
    )
    if all_reservations_for_user.status_code == 200:
        all_reservations_for_user = all_reservations_for_user.json()
        reservations = []
        for dates in all_reservations_for_user["dates"]:
            if dates["date"] == reservation_date:
                reservations.append(dates)
            else:
                continue
        res = make_response(reservations, 200)
        return res
    else:
        return make_response(jsonify({"Error": "User doesn't exist"}), 402)


# Get reservations(bookings) details by user_id
# We use graphQL to access the movie Service and get informations about movies.
@app.route("/user/reservation_details/<user_id>", methods=["GET"])
def get_user_reservation_details(user_id):
    all_reservations_for_user = requests.get(
        f"http://127.0.0.1:3201/bookings/{user_id}"
    ).json()
    details = []
    for reservation in all_reservations_for_user["dates"]:
        reservation_details = {"date": reservation["date"], "movies": []}
        for movie_id in reservation["movies"]:
            # graphQL request
            movie_details = requests.post(
                f"http://127.0.0.1:3001/graphql",
                json={
                    "query": 'query{ movie_with_id(_id:"'
                    + f"{movie_id}"
                    + '"){id title director rating}}'
                },
            ).json()
            reservation_details["movies"].append(movie_details)
        details.append(reservation_details)
    res = make_response(jsonify(reservation_details), 200)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
