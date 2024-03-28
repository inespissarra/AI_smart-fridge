# CHIP The Fridge

Ambient Intelligence Project (MEIC-A, Instituto Superior Técnico, 2023/2024)

CHIP The Fridge is a smart fridge that helps users to manage their food. It has a camera that scans the products before they are stored in the fridge. The camera sends the image to a system that processes the data and stores it in a database. The system also receives data from an Arduino that informs the system when a product is added or removed from the fridge. The system has a web app that allows users to see the products in the fridge and their expiration dates. The system also allows the user to send the shopping list to the user's email.

## General Information

Nowadays it is common to have food waste. This project aims to help people manage their food as the system helps the user keep track of the products in the fridge and their expiration dates. The system also creates a shopping list and send it to the user's email to make shopping easier.

## Built With

This project was built using Arduino and a camera (Nicla Vision). For the software part Python was used as the main programming language. The system uses a MySQL database to store the products and their expiration dates. The system also uses PyTorch to train the machine learning models and Tesseract to process the data from the camera. The web app was built using Flask and the email was sent using the secure-smtplib library.

### Hardware

* [Arduino Starter Kit](https://store.arduino.cc/products/arduino-starter-kit-multi-language) - 1 unit - Light sensor to detect if a shelf inside the fridge has a product
* [Nicla Vision](https://store.arduino.cc/products/nicla-vision) - 1 unit - Camera to take pictures of the products so that the system can process the data

### Software

* [OpenMV IDE](https://openmv.io/pages/download?gad_source=1&gclid=CjwKCAjw7-SvBhB6EiwAwYdCAdFi9kPw_PdA8yJYGA-OzIwjfuq-NtvnOjP9ont1bPy2H4JPX77EaRoCROcQAvD_BwE) - to program the camera
* [Arduino IDE](https://www.arduino.cc/en/software) - To program the Arduino
* [Visual Studio Code](https://code.visualstudio.com/) - To program the remaining code
* [RectLabel](https://rectlabel.com/) - To create the dataset for the machine learning models
* [Google Colab](https://colab.research.google.com/) - To train the machine learning models

## Getting Started

These instructions will get you a copy of the project up and running on for testing purposes.

### Assembly Instructions

The design of CHIP, The Smart Fridge would be the following:

![CHIP](<img/chip.png>)

The fridge has a shelf that is used to put a product so that it can be scanned by the camera above it. The shelf is retractable to take up less space.

In order to simulate this design, we used a box as the place to scan products:

![camera_shelf](<img/camera_shelf.jpg>)

And a smaller box to have the Arduino inside and be a shelf for the fridge:

![fridge_shelf](<img/fridge_shelf.jpg>)

#### Arduino

For the project to run, the Arduino must be assembled as follows:

![Arduino](<img/Dazzling Albar-Tumelo.png>)

### Software Prerequisites

There are some libraries and tools we need before we start.

MySQL: 
```
sudo apt-get install mysql-server
```

PyTorch:
```
pip install torch torchvision
```

Pytesseract:
```
pip install pytesseract
```

Flask:
```
pip install Flask
```

SmtpLib:
```
pip install secure-smtplib
```

### Installation

### Camera

In the code `camera/camera.py` it is necessary to configure the SSID and KEY variables to the correspondents of the local Wi-Fi. The IP variable also needs to be replaced by the correct IP.

By running the code in OpenMV IDE (with the camera connected to the computer), it is possible to see what the camera is capturing.

To make this code the default when the camera is connected to the energy click `Tools > Save open script to OpenMV Cam (as main.py)` in OpenMV IDE.

The camera has to be connected to the energy using a USB-Micro USB cable. The light turns green if the camera is connected correctly as this indicates it is ready to capture a picture. When the camera is taking the picture, the light turns red. Finally, when the product is ready to be removed, the light turns blue. The picture is sent to the system by Wi-Fi.

To run the code that processes the camera data (in the computer), go to `data_process/camera/_model_` ( __model_ _ must be replaced by `new_model` or `pre_trained`) and run `camera.py` with the following commands:

```sh
cd data_process/camera/_model_
python3 camera.py
```

The correspondent models must be in the same folder as the `camera.py` code.

#### Arduino

To make the code the default when the Arduino is connected to the computer:

- Click `Select Board` and then `Arduino Uno`;
- Click `Verify` (check button);
- Click `Upload` (arrow button).

The Arduino must be connected to the computer for collected data to be processed.

In the code `data_process/arduino.py` it is necessary to configure the correct port for the Arduino by changing the `ser` variable. To know the port go to Arduino IDE and click `Tools > Port`. The port that appears with a check mark is the correct one.

Then, run the code with the following commands:

```sh
cd data_process/
python3 arduino.py
```

### Web App

The web app is a Flask app that allows the user to see the products in the fridge and their expiration dates. The user can also send the shopping list to the user's email.

The web app design is the following:

![Webpage](<img/webpage.png>)

To create the database and run the web app, execute the commands:

```sh
cd app/
sudo service mariadb start
./database.sh
python3 app.py
```

You should see the following message:

```sh
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
```

## Demo

Open the web page with url `http://127.0.0.1:5000`

![Web page normal](<img/webpage_normal.png>)

### Send Shopping List

To send the shopping list to your email, click on the button `Send by Email`

![Send email](<img/send_email.png>)

![Popup](<img/popup.png>)

Now you can find in your email inbox the following email:
![Email](<img/email.png>)

### Put a Product in the Fridge

First check that the camera is ready to scan products (green light):
![Camera green light](<img/camera_green_light.png>)

Put the product on the shelf under the camera, and the light of the camera should turn red:
![Camera red light](<img/camera_red_light.png>)

When the light turns blue, you can take the product from the shelf:
![Camera blue light](<img/camera_blue_light.png>)

Put the product on the fridge's shelf with sensor:
![Product on shelf](<img/product_shelf.png>)

Now you can see on the web page that the product was added successfully in the application:
![Web page with product](<img/web_product.png>)

If an item is taken out and then promptly placed back in the fridge, it does not need to be scanned.

If you want to put multiple identical products, just scan the first one. And when a sensors that detects a produt will assume that the same product is being put in the fridge.

## Additional Information

### Remaining Folders

The `object_recognition` folder contains the code to create the machine learning models that recognize the products. 
There are two models:
- The new model, trained from scratch with the products that we want to recognize;
- The pre-trained model, that was adapted (fine-tuned) to recognize our specific products.

Unfortunately, the resulting models and the datasets are too big to be uploaded here.

The new model dataset and model can be found [here](https://drive.google.com/drive/folders/1BwTqUBPTOYiVevAY4tJy5jK9-yekGmWB?usp=drive_link).

The pre-trained model dataset and model can be found [here](https://drive.google.com/drive/folders/15AGG313OgU8PVDHnomRwuMnfar2_iWbs?usp=drive_link)

To train the machine learning models, the usage of Google Colab is recommended, as it has a GPU that speeds up the process. To change the runtime to GPU, go to `Runtime > Change runtime type` and select `T4 GPU`. 
The dataset (in a zip file) should be uploaded to the drive. 
In the case of the new model, the dataset should be a folder with one folder for each class and the images of the products inside the respective class folder.
In the case of the pre-trained model, the dataset should be a folder with a COCO JSON file and the respective images. An easy way to create this dataset is to use the `RectLabel` tool.
The number of classes (usually `num_classes`) should be adapted.

### Authors

| Number | Name               | Github                                 |
|--------|--------------------|----------------------------------------|
| 99176  | Ana Jin            | <https://github.com/Ananxv>            |
| 99236  | Inês Pissarra      | <https://github.com/inespissarra>      |
| 99261  | Juliana Marcelino  | <https://github.com/julianafmar>       |
