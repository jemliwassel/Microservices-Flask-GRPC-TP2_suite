import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]
    
    def GetBookingByUserID(self, request, context):
        user_id = request.user_id 
        for booking in self.db : 
            if booking['userid'] == user_id :
                # print("Boking was found successfully !")
                booking_response = booking_pb2.BookingData(user_id = user_id)
                for dates in booking['dates'] : 
                    user_reservation = booking_pb2.MovieDates(
                        date = dates['date'],
                        movies = dates ['movies']
                    )
                    booking_response.dates.append(user_reservation)
                return booking_response
        return booking_pb2.BookingData()
    
    def AddBookingForUser(self, request, context):
        user_id = request.user_id
        date = request.date
        movie_id = request.movie_id
        for booking in self.db:
            if booking['userid'] == user_id:
                for dates in booking['dates']:
                    if dates['date'] == date:               
                        if movie_id not in dates['movies']:
                            dates['movies'].append(movie_id)
                        else:
                            return booking_pb2.AddBookingResponse(success= False, message =f"Le film avec l'id {movie_id} est déjà réservé pour cette date.")
                    else:
                        new_date = {
                            'date': date,
                            'movies': [movie_id]
                        }
                        booking["dates"].append(new_date)
        new_bookings = {"bookings": self.db}
        with open('{}/data/bookings.json'.format("."), "w") as wfile:
            json.dump(new_bookings, wfile)
        return booking_pb2.AddBookingResponse(success=True, message="Réservation ajoutée avec succès.")
  
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
