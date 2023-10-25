import grpc

import showtime_pb2
import showtime_pb2_grpc

def get_showtime_by_date(stub, date):
    showtime = stub.GetShowtimeByDate(date)
    print(showtime)

def get_list_showtimes(stub):
    all_showtimes = stub.GetListShowtimes(showtime_pb2.Empty())
    for showtime in all_showtimes:
        print("Showtime : ",showtime)
        
def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)
        
        print("-------------- GetShowtimeByDate --------------")
        date = showtime_pb2.ShowtimeDate(date= "20151130")
        get_showtime_by_date(stub, date)
        
        print("-------------- GetListShowtimes --------------")
        get_list_showtimes(stub)
        
    channel.close()
    
if __name__ == '__main__':
    run()
        
