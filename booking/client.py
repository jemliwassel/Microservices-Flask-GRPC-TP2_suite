import grpc

import booking_pb2
import booking_pb2_grpc

def get_booking_by_user_id(stub, user_id):
    user_booking = stub.GetBookingByUserID(user_id)
    print("Booking : " , user_booking)

def add_booking_for_user(stub, user_id, date, movie_id):
    booking_request = booking_pb2.AddBookingRequest(user_id=user_id, date=date, movie_id=movie_id)
    response = stub.AddBookingForUser(booking_request)
    if response.success:
        print(response.message)
    else:
        print(f"Échec de la réservation : {response.message}")
        
def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3001') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        print("------------------- GetBookingByUserID----------------")
        user_id = booking_pb2.UserID(user_id  = "chris_rivers")
        get_booking_by_user_id(stub, user_id)
        print("-----------------AddBookingForUser----------------------")
        # booking_request = booking_pb2.AddBookingRequest(
        #     user_id= "chris_rivers",
        #     date = "20151201",
        #     movie_id ="267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
        # )
        add_booking_for_user(stub, user_id= "chris_rivers", date = "20151201", movie_id ="FR2023HORROR")
    channel.close()
    
if __name__ == '__main__':
    run()
    