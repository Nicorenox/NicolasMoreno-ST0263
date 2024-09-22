import grpc
import p2p_pb2_grpc as pb2_grpc
import p2p_pb2 as pb2
import sys

def upload_file(filename):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = pb2_grpc.PeerServiceStub(channel)
        
        with open(filename, 'rb') as f:
            filedata = f.read()

            # Send file to all available nodes
            response = stub.ListNodes(pb2.Empty())
            nodes = response.addresses
            
            for node in nodes:
                with grpc.insecure_channel(node) as node_channel:
                    node_stub = pb2_grpc.PeerServiceStub(node_channel)
                    try:
                        node_stub.PutFile(pb2.PutFileRequest(filename=filename, filedata=filedata))
                        print(f"File sent to node {node}")
                    except grpc.RpcError as e:
                        print(f"Failed to send file to node {node}: {e}")

def download_file(filename, output_filename):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = pb2_grpc.PeerServiceStub(channel)
        
        response = stub.ListNodes(pb2.Empty())
        nodes = response.addresses
        
        for node in nodes:
            with grpc.insecure_channel(node) as node_channel:
                node_stub = pb2_grpc.PeerServiceStub(node_channel)
                try:
                    response = node_stub.GetFile(pb2.GetFileRequest(filename=filename))
                    if response.success:
                        with open(output_filename, 'wb') as f:
                            f.write(response.filedata)
                        print(f"File downloaded and saved as {output_filename}")
                        return
                except grpc.RpcError as e:
                    print(f"Failed to download file from node {node}: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python client.py --upload <filename> | --download <filename> <output_filename>")
        return
    
    if sys.argv[1] == '--upload':
        upload_file(sys.argv[2])
    
    elif sys.argv[1] == '--download':
        download_file(sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
