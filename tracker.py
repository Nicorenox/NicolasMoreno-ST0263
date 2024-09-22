import grpc
from concurrent import futures
import time
import p2p_pb2_grpc as pb2_grpc
import p2p_pb2 as pb2

class TrackerService(pb2_grpc.PeerServiceServicer):
    def __init__(self):
        self.nodes = {}
        self.files = {}

    def JoinNetwork(self, request, context):
        self.nodes[request.address] = request.available_files
        for file in request.available_files:
            if file not in self.files:
                self.files[file] = set()
            self.files[file].add(request.address)
        self.print_status()
        return pb2.JoinResponse(message=f"Node {request.address} successfully joined.")

    def LeaveNetwork(self, request, context):
        if request.address in self.nodes:
            for file, nodes in list(self.files.items()):
                if request.address in nodes:
                    nodes.remove(request.address)
                    if not nodes:
                        del self.files[file]
            del self.nodes[request.address]
            self.print_status()  # Actualizar la visualización al desconectar
        return pb2.LeaveResponse(message=f"Node {request.address} left the network.")

    def ListNodes(self, request, context):
        return pb2.ListNodesResponse(addresses=list(self.nodes.keys()))

    def ReplicateFiles(self, filename):
        if filename in self.files:
            available_nodes = list(self.nodes.keys())
            for node in self.files[filename]:
                if node in available_nodes:
                    continue  # No replicar en el mismo nodo
                with grpc.insecure_channel(node) as channel:
                    stub = pb2_grpc.PeerServiceStub(channel)
                    response = stub.GetFile(pb2.GetFileRequest(filename=filename))
                    if response.success:
                        for target_node in available_nodes:
                            if target_node != node:
                                with grpc.insecure_channel(target_node) as new_node_channel:
                                    new_node_stub = pb2_grpc.PeerServiceStub(new_node_channel)
                                    new_node_stub.PutFile(pb2.PutFileRequest(
                                        filename=filename,
                                        filedata=response.filedata
                                    ))
                                    print(f"File {filename} replicated to {target_node}")
                        break

    def print_status(self):
        print("\nCurrent tracker status:")
        print("Nodes and their files:")
        for node, files in self.nodes.items():
            print(f" - {node}: {', '.join(files) if files else 'No files'}")
        print("Files and their nodes:")
        for file, nodes in self.files.items():
            print(f" - {file}: {', '.join(nodes)}")
        print("")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_PeerServiceServicer_to_server(TrackerService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Tracker started, listening on port 50052")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
