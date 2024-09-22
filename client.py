import grpc
import p2p_pb2_grpc as pb2_grpc
import p2p_pb2 as pb2
import sys

def upload_file(filename):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = pb2_grpc.PeerServiceStub(channel)
        with open(filename, 'rb') as f:
            filedata = f.read()

        # Obtener nodos disponibles
        response = stub.ListNodes(pb2.Empty())
        nodes = response.addresses
        if not nodes:
            print("No nodes available to upload the file.")
            return

        # Priorizar el nodo más reciente primero
        for node in nodes:
            with grpc.insecure_channel(node) as node_channel:
                node_stub = pb2_grpc.PeerServiceStub(node_channel)
                try:
                    node_stub.PutFile(pb2.PutFileRequest(
                        filename=filename,
                        filedata=filedata
                    ))
                    print(f"File sent to node {node}")
                except grpc.RpcError as e:
                    print(f"Failed to send file to node {node}: {e}")

def download_file(filename, output_filename):
    # Obtener nodos disponibles
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = pb2_grpc.PeerServiceStub(channel)
        response = stub.ListNodes(pb2.Empty())
        nodes = response.addresses

    if not nodes:
        print("No nodes available to download the file.")
        return

    # Descargar el archivo desde los nodos
    file_data = b""
    for node in nodes:
        with grpc.insecure_channel(node) as channel:
            stub = pb2_grpc.PeerServiceStub(channel)
            try:
                response = stub.GetFile(pb2.GetFileRequest(filename=filename))
                if response.success:
                    file_data = response.filedata
                    break
                else:
                    print(f"Failed to download file from node {node}")
            except grpc.RpcError as e:
                print(f"Failed to download file from node {node}: {e}")

    if file_data:
        with open(output_filename, 'wb') as f:
            f.write(file_data)
        print(f"File downloaded and saved as {output_filename}")
    else:
        print("File not found on any node.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py --upload <filename> | --download <filename> <output_filename>")
        return

    if sys.argv[1] == '--upload':
        if len(sys.argv) != 3:
            print("Usage: python client.py --upload <filename>")
            return
        filename = sys.argv[2]
        upload_file(filename)
    elif sys.argv[1] == '--download':
        if len(sys.argv) != 4:
            print("Usage: python client.py --download <filename> <output_filename>")
            return
        filename = sys.argv[2]
        output_filename = sys.argv[3]
        download_file(filename, output_filename)
    else:
        print("Usage: python client.py --upload <filename> | --download <filename> <output_filename>")

if __name__ == '__main__':
    main()
