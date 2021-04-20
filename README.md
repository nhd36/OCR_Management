OCR-Management is the Web Application project that allows users to put their documents and managing them on-cloud.

- Frontend: Using JinJa + Flask, Frontend Library of Python
- Backend: Using Flask to create API.

- To run project, needs two available ports on server (Should be 5000 and 8000).
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
```
- To start running Backend port, run following commands:
```
cd OCR_Backend_API
pip3 install -r requirements
python3 app.py
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
- To start running Frontend port, run following commands:
```
cd OCR_Frontend_Clientside
pip3 install -r requirements
python3 app.py
```

Each .env file should be placed in their following directory. For example, .env file for Backend should be putting in OCR_Backend_API directory.

**Working on Docker, coming soon**.
