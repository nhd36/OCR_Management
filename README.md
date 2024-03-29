OCR-Management is the Web Application project that allows users to put their documents and managing them on-cloud.

**Technologies Usage:
- Frontend: Jinja2, Flask
- Backend: Flask, FlaskSQLAlchemy

To run project, needs two available ports on your machine (Normally 5000 and 8000, depends on your prefer).

Initialize Project:

- UBUNTU:
```
apt-get install python3-virtualenv
pip3 install virtualenv
virtualenv venv
source ven/bin/activate
```
Backend:
- Needs available fields for .env file:
```
API_PORT=
IP=
JWT_SECRET_KEY=
API_KEY=
API_SECRET=
OCR_API=
```
- To start running Backend server, run following commands:
```
cd OCR_Backend_API
pip3 install -r requirements
python3 run.py
```

Frontend:
- Needs available fields for .env file:
```
APP_PORT=
API_PORT=
IP=
SECRET_KEY=
JWT_SECRET_KEY=
API_KEY=
API_SECRET=
```
- To start running Frontend server, run following commands:
```
cd OCR_Frontend_Clientside
pip3 install -r requirements
python3 run.py
```

- You will need your own script which will make request to your OCR API and get the data back. The structure of the response data from OCR can be edit and 
view in path ./OCR_Backend_API/side_methods.py
- You need to know the respond structure of your API, and edit the structure in scan_OCR() function inside side_methods.py
- In my opinion, it should only return a bunch of text. It would be fine!

Each .env file should be placed in their following directory. For example, .env file for Backend should be putting in OCR_Backend_API directory.

**Working on Docker, coming soon**.

NOTE: YOU NEED TO HAVE YOUR OWN OCR API TO WORK ON THIS APP. THIS APP ONLY DO BASIC CRUD OPERATIONS AND INTEGRATE WITH THIRD PARTY API.
