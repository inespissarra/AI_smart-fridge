import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(("192.168.43.117", 8080))  # Replace with Raspberry Pi's IP address
server_socket.listen(5)

while True:
    # Wait for a connection
    client_socket, _ = server_socket.accept()

    # Receive the image size
    img_size_bytes = b''
    while len(img_size_bytes) < 4:
        chunk = client_socket.recv(4 - len(img_size_bytes))
        if not chunk:
            break
        img_size_bytes += chunk

    # Convert image size bytes to integer
    img_size = int.from_bytes(img_size_bytes, byteorder='big')

    # Receive the image data
    img_data = b''
    while len(img_data) < img_size:
        chunk = client_socket.recv(min(4096, img_size - len(img_data)))
        if not chunk:
            break
        img_data += chunk

    # Write image data to file
    with open('received_image.jpg', 'wb') as f:
        f.write(img_data)

    # Close the client socket
    client_socket.close()
