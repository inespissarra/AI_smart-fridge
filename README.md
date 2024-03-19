# A02 CHIP The Fridge Project

## Team

| Number | Name               | E-mail                                 |
|--------|--------------------|----------------------------------------|
| 99176  | Ana Jin            | <anainesj@tecnico.ulisboa.pt>          |
| 99236  | Inês Pissarra      | <ines.pissarra@tecnico.ulisboa.pt>     |
| 99261  | Juliana Marcelino  | <juliana.marcelino@tecnico.ulisboa.pt> |

## Components

- Arduino Starter Kit
- Nicla Vision
- System that runs the database and code
- Display

## Required Platforms

It was used the following text platforms to program our smart fridge:

- OpenMV IDE - to program the Camera
- Arduino IDE - to program the Arduino
- Visual Studio Code - to program the remaining code

## Setup

The design of the CHIP - smart fridge would be the following:

![CHIP](<chip.png>)

The fridge has a shelf that is used to put a product so that it can be scanned by the camera above it. The shelf is retractable to take up less space.

In order to simulate this design, we used a box as the place to scan products:
![camera_shelf](<img/camera_shelf.jpg>)

And a smaller box to have the Arduino inside and be a shelf for the fridge:
![fridge_shelf](<img/fridge_shelf.jpg>)

### Camera

In the code `camera/camera.py` it is necessary to configure the SSID and KEY variables to the correspondents of the local Wi-Fi. The IP variable also needs to be replaced by the right IP.

By running the code in OpenMV IDE (with the camera connected to the computer), it is possible to see what the camera is capturing.

To make this code the default when the camera is connected to the energy click `Tools > Save open script to OpenMV Cam (as main.py)` in OpenMV IDE.

The camera has to be connected to the energy using a USB-Micro USB cable. The light turns green if the camera is connected correctly as this indicates it is ready to capture a picture. When the camera is taking the picture, the light turns red. Finally, when the product is ready to be removed, the light turns blue. The picture is sent to the system by Wi-Fi.

To run the code that processes the camera data (in the computer), go to `data_process/camera` and run `camera.py` with the following commands:

```sh
cd data_process/camera
python3 camera.py
```

### Arduino

For the project to run, the Arduino must be assembled as follows:

![Arduino](<img/Dazzling Albar-Tumelo.png>)

To make this code the default when the Arduino is connected to the computer:

- Click `Select Board` and then `Arduino Uno`
- Click `Verify` (the check button)
- Click `Upload` (arrow button).

The Arduino must be connected to the computer for collected data to be processed.

To run the code that processes the Arduino data (in the computer), go to `data_process/` and run `arduino.py` with the following commands:

```sh
cd data_process/
python3 arduino.py
```

### Web App

![Webpage](<img/webpage.png>)

To run the web app, execute the commands:

```sh
cd app/
sudo service mariadb start
./database.sh
python3 app.py
```

## Additional Information

### Remaining Folders

The `object_recognition` and `date_recognition` folders contain the code to create the machine learning models that recognize the products

### Links to Used Tools and Libraries

- [Python](https://www.python.org/)
- [PyTorch](https://pytorch.org/)
- [Pytesseract](https://pypi.org/project/pytesseract/)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [SmtpLib](https://docs.python.org/3/library/smtplib.html)
- [MySQL](https://www.mysql.com/)
- [OpenMV IDE](https://openmv.io/pages/download?gad_source=1&gclid=CjwKCAjw7-SvBhB6EiwAwYdCAdFi9kPw_PdA8yJYGA-OzIwjfuq-NtvnOjP9ont1bPy2H4JPX77EaRoCROcQAvD_BwE)
- [Arduino IDE](https://www.arduino.cc/en/software)
- [Visual Studio Code](https://code.visualstudio.com/)

----
END OF README
