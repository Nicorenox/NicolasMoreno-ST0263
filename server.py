import grpc
from concurrent import futures
import p2p_pb2_grpc as pb2_grpc
import p2p_pb2 as pb2
import time
import sys

class PeerService(pb2_grpc.PeerServiceServicer):
    def __init__(self):
        self.files = {}

    def PutFile(self, request, context):
        self.files[request.filename] = request.filedata
        return pb2.PutFileResponse(success=True, message="File stored successfully.")

    def GetFile(self, request, context):
        if request.filename in self.files:
            return pb2.GetFileResponse(success=True, filedata=self.files[request.filename])
        return pb2.GetFileResponse(success=False, filedata=b"")

def register_with_tracker(tracker_address, node_address):
    with grpc.insecure_channel(tracker_address) as channel:
        stub = pb2_grpc.PeerServiceStub(channel)
        response = stub.JoinNetwork(pb2.JoinRequest(address=node_address, available_files=[]))
        print(response.message)

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_PeerServiceServicer_to_server(PeerService(), server)
    server.add_insecure_port(f'0.0.0.0:{port}')  # Cambia a 0.0.0.0
    server.start()
    print(f"Peer server started, listening on port {port}")

    # Aquí asegúrate de que apunte al contenedor del tracker (p.ej., 'tracker:50052')
    register_with_tracker('tracker:50052', f'server:{port}')

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    port = sys.argv[1]
    serve(port)
