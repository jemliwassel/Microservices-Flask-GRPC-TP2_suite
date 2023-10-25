import grpc

import booking_pb2
import booking_pb2_grpc


def get_list_booking(stub):
    bookings = stub.GetListBookings(booking_pb2.EmptyBooking())
    for booking in bookings:
        print(booking)


def get_booking_by_user_id(stub, user_id):
    user_bookings = stub.GetBookingByUserID(user_id)
    for booking in user_bookings:
        print(booking)


def add_booking_for_user(stub, user_id, date, movie_id):
    booking_request = booking_pb2.AddBookingRequest(
        user_id=user_id, date=date, movie_id=movie_id
    )
    response = stub.AddBookingForUser(booking_request)
    print(response)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:3001") as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        print("-------------- GetListBooking --------------")
        get_list_booking(stub)
        print("------------------- GetBookingByUserID----------------")
        user_id = booking_pb2.UserID(user_id="chris_rivers")
        get_booking_by_user_id(stub, user_id)
        print("-----------------AddBookingForUser----------------------")
        add_booking_for_user(
            stub,
            user_id="chris_rivers",
            date="20151201",
            movie_id="7daf7208-be4d-4944-a3ae-c1c2f516f3e6",
        )
    channel.close()


if __name__ == "__main__":
    run()
