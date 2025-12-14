# Project 0: Securely Time-Stamping a Document

import os
import rsa               # External RSA library for key handling and encryption
import RSA               # Custom RSA module (probably for encrypt/decrypt methods)
import grpc              # gRPC module for client-server communication
import PyPDF2            # Library to read/write PDF files
import GMT_pb2           # Generated protobuf module for message structures
import hashlib           # Provides hash functions like SHA256
import GMT_pb2_grpc      # Generated protobuf module for gRPC stubs
from reportlab.pdfgen import canvas         # Used to draw text onto PDF pages
from reportlab.lib.pagesizes import letter  # Standard letter page size for PDF

# Generates a SHA-256 hash of all the text from a PDF file (excluding formatting)
def generate_PDF_hash(document):
    all_pages = ""

    with open(document, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Extract text from each page and concatenate
        for page in range(len(reader.pages)):
            all_pages += reader.pages[page].extract_text()

        file.close()

    # Return the hash of the full concatenated content
    return hashlib.sha256(all_pages.encode()).hexdigest()

# Generates a SHA-256 hash of all lines in a text file
def generate_TXT_hash(document):
    all_content = []

    with open(document, 'r') as file:
        all_content = file.readlines()

        file.close()

    # Join all lines and return the hash
    return hashlib.sha256("".join(all_content).encode()).hexdigest()

# Appends the timestamp and signature to a PDF file as a new page
def generate_PDF(document, signature, timestamp):
    writer = PyPDF2.PdfWriter()

    with open(document, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Copy all original pages to a new PDF writer
        for page in range(len(reader.pages)):
            writer.add_page(reader.pages[page])

        file.close()

    # Create a new page with timestamp and signature using ReportLab
    canvass = canvas.Canvas('temp.pdf', pagesize=letter)
    canvass.drawString(100, 100, "GMT Authentication Service")
    canvass.drawString(100, 80, timestamp)
    canvass.drawString(100, 60, signature)
    canvass.save()

    # Add the new timestamp page to the final PDF
    with open('temp.pdf', 'rb') as temp:
        writer.add_page(PyPDF2.PdfReader(temp).pages[0])
        temp.close()

    # Overwrite original file with the updated one
    with open(document, 'wb') as output:
        writer.write(output)
        output.close()

    os.remove('temp.pdf')  # Clean up the temporary file

# Appends the timestamp and signature to a TXT file at the end
def generate_TXT(document, signature, timestamp):
    with open(document, 'a') as file:
        file.write("\nGMT Authentication Service\n" +
                   timestamp + '\n' + signature)
        file.close()

# Verifies a document's timestamp and digital signature
def verify_document(document):

    # If the document is a PDF file
    if document.decode('utf8').endswith(".pdf"):
        all_pages = ""

        with open(document, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            # Concatenate all pages except the last (timestamp page)
            for page in range(len(reader.pages) - 1):
                all_pages += reader.pages[page].extract_text()

            # Extract and decrypt the signature from the last page
            signature = RSA.decrypt(
                server_public_key.e, server_public_key.n, reader.pages[-1].extract_text()[-174:][:-1])

            # Recompute the hash from the content and compare with signature
            hash = hashlib.sha256((hashlib.sha256(all_pages.encode()).hexdigest(
            ) + reader.pages[-1].extract_text()[-208:-175][1:]).encode()).hexdigest()

            # Verification success/failure output
            if hash == signature:
                print("\n\nDocument Timestamped and VERIFIED Successfully.\n\n")
            else:
                print("\n\nDocument Verification Failed.\n\n")

            file.close()

    # If the document is a TXT file
    elif document.decode('utf8').endswith(".txt"):
        lines = []

        with open(document, "r") as file:
            lines = file.readlines()
            file.close()

        # Remove the last 3 lines: header, timestamp, and signature
        content = lines[:-3]
        content[-1] = content[-1][:-1]  # Strip newline from last line

        # Decrypt the signature
        signature = RSA.decrypt(server_public_key.e,
                                server_public_key.n, lines[-1])

        # Recompute the hash of the content + timestamp
        hash = hashlib.sha256((hashlib.sha256(
            "".join(content).encode()).hexdigest() + lines[-2][:-1]).encode()).hexdigest()

        # Verification success/failure output
        if hash == signature:
            print("\n\nDocument Timestamped and VERIFIED Successfully.\n\n")
        else:
            print("\n\nDocument Verification Failed.\n\n")

# Entry point of the program
if __name__ == '__main__':

    print("\n\n\n<---------------GMT Authentication Service--------------->\n\n\n")

    while True:
        try:
            server_public_key = None
            document = str(
                input("Enter the Document Path or Content: ")).encode()

            # Connect to the gRPC server
            channel = grpc.insecure_channel('localhost:50051')
            stub = GMT_pb2_grpc.TimeStampServiceStub(channel)

            # Read server's public key for encryption
            with open("GMT_Server_Public_Key.txt", "r") as file:
                lines = file.readlines()
                server_public_key = rsa.key.PublicKey(
                    int(lines[1].split()[1]), int(lines[0].split()[1]))
                file.close()

            # Handle PDF document timestamping
            if document.decode('utf8').endswith(".pdf"):
                response = stub.GetDocumentTimeStamp(GMT_pb2.TimeStampRequest(document=rsa.encrypt(
                    generate_PDF_hash(document.decode('utf8')).encode(), server_public_key)))

                generate_PDF(document, response.signature, response.timestamp)

            # Handle TXT document timestamping
            elif document.decode('utf8').endswith(".txt"):
                response = stub.GetDocumentTimeStamp(GMT_pb2.TimeStampRequest(document=rsa.encrypt(
                    generate_TXT_hash(document.decode('utf8')).encode(), server_public_key)))

                generate_TXT(document, response.signature, response.timestamp)

            # Handle plain string message input
            else:
                response = stub.GetDocumentTimeStamp(GMT_pb2.TimeStampRequest(document=rsa.encrypt(
                    hashlib.sha256(document).hexdigest().encode(), server_public_key)))

                print("\n" + document.decode() + "\nGMT Authentication Service\n" +
                      response.timestamp + '\n' + response.signature)

                # Decrypt and verify response
                signature = RSA.decrypt(server_public_key.e,
                                        server_public_key.n, response.signature)

                hash = hashlib.sha256(
                    (hashlib.sha256(document).hexdigest() + response.timestamp).encode()).hexdigest()

                if hash == signature:
                    print("\n\nDocument Timestamped and VERIFIED Successfully.\n\n")
                else:
                    print("\n\nDocument Verification Failed.\n\n")

                continue

            # For file input, verify after timestamping
            verify_document(document)

        # Gracefully exit the loop on Ctrl+C
        except KeyboardInterrupt:
            print("\n\n\nGMT Authentication Service Shutting Down...\n\n\n")
            os._exit(0)
