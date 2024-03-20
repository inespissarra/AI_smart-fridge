# receive image
import socket
import cv2

# predict image
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from tensorflow.keras.models import load_model

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
model = load_model('recognizer.h5')

# create data generator for training set
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    "./dataset",
    target_size=(504, 378),
    batch_size=8,
    class_mode='categorical')

# obtain class indices from the training set
class_indices = train_generator.class_indices

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
    def predict_image(model, image_path, image_height, image_width):
        img = load_img(image_path, target_size=(image_height, image_width))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)/255
        prediction = model.predict(img)
        return prediction

    def get_class_label(prediction, class_indices):
        class_label = None
        max_prob = np.max(prediction)
        for label, index in class_indices.items():
            if prediction[0][index] == max_prob:
                class_label = label
                break
        return class_label

    prediction = predict_image(model, image_path, 504, 378)
    class_label = get_class_label(prediction, class_indices)

    print(f'The image {image_path} is classified as {class_label} with probability {np.max(prediction) * 100 :.2f}')
    if np.max(prediction) > 0.8:
        print("Product recognized")
    else:
        print("Product not recognized")
        class_label = "Unknown"
    return class_label

def recognize_date():
    padrao_data = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}$'

    image = Image.open('received_image.jpg')

    result = pytesseract.image_to_string(image)

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
        f.write("1\n")
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
    
    quantity = "1"

    save_last_product(product, quantity, expiration_date)
