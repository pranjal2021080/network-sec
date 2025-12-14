# Project 0: RSA-based Public-key Certification Authority (CA)

from base64 import b64encode, b64decode

# Function to encrypt a message using RSA public key (e, n)
def encrypt(e, n, message):

    encrypted_message = ""

    # Convert the message to bytes, then to an integer, and apply RSA encryption: c = m^e mod n
    power_raised = pow(int.from_bytes(message.encode("utf-8"), "big"), e, n)

    # Convert the encrypted integer back to bytes, then encode to base64 string
    encrypted_message += b64encode(power_raised.to_bytes(
        power_raised.bit_length() // 8 + 1, "big")).decode("ascii") + " "

    return encrypted_message


# Function to decrypt a base64-encoded message using RSA private key (d, n)
def decrypt(d, n, encrypted_message):

    decrypted_message = ""

    # Split and iterate over each encrypted base64 message segment
    for message in encrypted_message.split(" ")[0: -1]:

        # Decode base64 to bytes, convert to integer, and apply RSA decryption: m = c^d mod n
        power_raised = pow(int.from_bytes(b64decode(message), "big"), d, n)

        # Convert the decrypted integer back to string
        decrypted_message += power_raised.to_bytes(
            power_raised.bit_length() // 8 + 1, "big").decode("utf-8")

    return decrypted_message
