# Project 0: Securely Time-Stamping a Document

import os
import rsa  # External RSA library for key generation and encryption
import RSA  # Custom RSA utility module for encryption/decryption (likely a provided file)
import time  # For sleeping the server loop
import grpc  # gRPC framework for remote procedure calls
import hashlib  # For generating secure SHA-256 hashes
import GMT_pb2  # Generated gRPC message classes
import GMT_pb2_grpc  # Generated gRPC service classes
import GMTTimeServer  # Custom module for getting the current GMT time
from concurrent import futures  # For multi-threaded server support


# Define a class that implements the gRPC service
class TimeStampServiceServicer(GMT_pb2_grpc.TimeStampServiceServicer):

    def __init__(self):
        # Store received document (encrypted content)
        self.document = None

        # Generate RSA public and private keys for the server
        self.public_key, self.private_key = rsa.newkeys(1024)

        # Save the server's public key to a file so the client can read and use it
        with open("GMT_Server_Public_Key.txt", "w") as file:
            file.write(f"e: {self.public_key.e}\nn: {self.public_key.n}\n")

    # Implement the RPC method for time-stamping a document
    def GetDocumentTimeStamp(self, request, context):

        # Get current GMT timestamp from the custom module
        timestamp = str(GMTTimeServer.get_current_gmt_time())

        # Decrypt the incoming document hash using the server's private key
        self.document = rsa.decrypt(request.document, self.private_key).decode('utf-8')

        # Combine document hash and timestamp, hash the result, then sign it using server's private key
        signature = RSA.encrypt(
            self.private_key.d,
            self.private_key.n,
            hashlib.sha256((self.document + timestamp).encode()).hexdigest()
        )

        print("\n\nDocument Signed and Timestamped Successfully.\n\n")

        # Send the signed hash and timestamp back to the client
        return GMT_pb2.TimeStampResponse(signature=signature, timestamp=timestamp)


# Entry point to start the server
if __name__ == '__main__':

    # Create a gRPC server with a thread pool of 10 workers
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the time-stamp service with the server
    GMT_pb2_grpc.add_TimeStampServiceServicer_to_server(
        TimeStampServiceServicer(), server)

    # Open port 50051 for communication (localhost only)
    server.add_insecure_port('localhost:50051')
    server.start()

    print("\n\n\nGMT Time Stamping Server Running...\n\n\n")

    try:
        # Keep the server running indefinitely (until Ctrl+C)
        while True:
            time.sleep(86400)  # Sleep for 1 day in each loop iteration

    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        print("\n\n\nShutting down GMT Time Stamping Server...\n\n\n")
        server.stop(0)
        os._exit(0)
