# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import grpc
import booking_pb2
import booking_pb2_grpc
from google.protobuf.json_format import MessageToDict

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
# We use distant procedure from the Booking service to get informations
@app.route("/user/reservations/<user_id>", methods=["GET"])
def get_user_reservation(user_id):
    if request.args:
        req = request.args
        reservation_date = req["date"]
        with grpc.insecure_channel('localhost:3001') as channel :
            stub = booking_pb2_grpc.BookingStub(channel)
            all_reservations_for_user = stub.GetBookingByUserID(booking_pb2.UserID(user_id=user_id))
            reservations = []
            for reservation in all_reservations_for_user:
                for dates in reservation.dates:
                    if dates.date == reservation_date:
                        reservations.append(dates)
            channel.close()
            for item in reservations:
                res = make_response(MessageToDict(item), 200)
                return res
            return make_response(jsonify({"Error": "There is an error in user booking request"}), 402)
    else:
        return make_response(jsonify({"error": "reservation date not found"}), 400)

# Get reservations(bookings) details by user_id
# We use graphQL to access the movie Service and get informations about movies.
# We use distant procedure from the Booking service to get informations
@app.route("/user/reservation_details/<user_id>", methods=["GET"])
def get_user_reservation_details(user_id):
    with grpc.insecure_channel('localhost:3001') as channel :
        stub = booking_pb2_grpc.BookingStub(channel)
        all_reservations_for_user = stub.GetBookingByUserID(booking_pb2.UserID(user_id=user_id))
        details = []
        for reservation in all_reservations_for_user:
            for dates in reservation.dates:
                reservation_details = {"date": dates.date,  "movies": []}
                for movie_id in dates.movies: 
                    # graphQL request
                    movie_details = requests.post(
                        f"http://127.0.0.1:3001/graphql",
                        json={
                            "query": 'query{ movie_with_id(_id:"'
                            + f"{movie_id}"
                            + '"){id title director rating}}'
                        },
                    ).json()
                    reservation_details["movies"].append(movie_details["data"]["movie_with_id"])
                details.append(reservation_details)
        channel.close()
    res = make_response(jsonify(details), 200)
    return res


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
