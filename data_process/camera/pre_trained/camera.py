# receive image
import socket
import cv2

# predict image
import torch
import torchvision
import cv2
import json
import numpy as np

# recognize date
import pytesseract
from PIL import Image
import re


#-----------------------------------------------------------
# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(("192.168.1.5", 8080))  # Replace with Raspberry Pi's IP address
print("Server is running on port 8080")
server_socket.listen(5)
#-----------------------------------------------------------

# ------------- Load the machine learning model-------------

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(num_classes=3, weights=None)
model.load_state_dict(torch.load('faster_rcnn_model2.pth', map_location=torch.device('cpu')))
model.eval()

# predict the image
image_path = './received_image.jpg'
#-----------------------------------------------------------

def receive_image():
    # Wait for a connection
    client_socket, _ = server_socket.accept()

    # Receive the image size
    img_size_bytes = b''
    while len(img_size_bytes) < 4:
        chunk = client_socket.recv(4 - len(img_size_bytes))
        if not chunk:
            break
        img_size_bytes += chunk

    print(img_size_bytes)

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
        f.close()

    # Close the client socket
    client_socket.close()

def recognize_image():
    def load_image(image_path):
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        img = torch.tensor(img, dtype=torch.float32).permute(2, 0, 1)
        img = img.unsqueeze(0)
        return img
    
    def predict_image(model, img):
        with torch.no_grad():
            prediction = model(img)

        label = prediction[0]['labels']

        json_file = 'coco_train.json'
        with open(json_file) as f:
            data = json.load(f)

        # get the most probable class
        if len(prediction[0]['scores']) == 0:
            return "", 0
        
        max_score_index = np.argmax(prediction[0]['scores'])
        max_score = prediction[0]['scores'][max_score_index]

        name = next((category['name'] for category in data['categories'] if category['id'] == label[max_score_index]), '')

        return name, max_score
    
    img = load_image(image_path)

    class_label, max_score = predict_image(model, img)

    print(f'A imagem {image_path} é da classe {class_label} com probabilidade {max_score * 100 :.2f}')
    if max_score > 0.8:
        print("Produto reconhecido")
    else:
        print("Produto não reconhecido")
        class_label = "Desconhecido"
    return class_label

def recognize_date():
    padrao_data = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}$'

    image = Image.open('received_image.jpg')

    result = pytesseract.image_to_string(image)

    print(result)

    # filter date
    result = result.split(' ')
    for i in result:
        if re.match(padrao_data, i):
            print(i)
            day = i.split('/')[0]
            month = i.split('/')[1]
            year = i.split('/')[2]
            return f"{year}-{month}-{day}"
    return "None"
    
def save_last_product(product, quantity, expiration_date):
    with open('../../last_product.txt', 'w') as f:
        f.write(product + '\n')
        f.write(quantity + '\n')
        f.write(expiration_date + '\n')
        f.close()

def resize_image():
    img_array = cv2.imread('received_image.jpg')
    img_array = cv2.resize(img_array, (504, 378))
    cv2.imwrite('received_image.jpg', img_array)

while True:
    receive_image()
    print("Image received")

    resize_image()

    product = recognize_image()

    expiration_date = recognize_date()
    
    if product == "eggs":
        quantity = "6"
    else:
        quantity = "1"

    save_last_product(product, quantity, expiration_date)
