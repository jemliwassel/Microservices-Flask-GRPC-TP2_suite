import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]
            
    def GetShowtimeByDate(self, request, context):
        date_to_search = request.date
        matching_showtimes = []
        for showtime in self.db:
            if showtime["date"] == date_to_search:
                matching_showtimes.append(showtime)
        if not matching_showtimes:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Aucun horaire trouvé pour la date spécifiée.")
            return showtime_pb2.ShowtimeData()
        
        response = showtime_pb2.ShowtimeData()
        response.date = date_to_search
        response.movies = json.dumps(matching_showtimes)
        return response
    
    def GetListShowtimes(self, request, context):
        for showtime in self.db:
            response = showtime_pb2.ShowtimeData()
            response.date = showtime["date"]
            response.movies = json.dumps(showtime)
            yield response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
