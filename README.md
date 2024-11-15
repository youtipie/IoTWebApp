IoTWebApp
=========

**IoTWebApp** is application designed for managing IoT devices, with functionality that allows users to
connect, control, and monitor IoT actuators. This app supports network creation, device control, access management, and
data visualization for IoT networks.

Installation and Setup
----------------------

### Prerequisites

* **python** and **poetry** to install all prerequisites for backend
* **PostgreSQL** or other relational database for storing IoT device states and user information
* **Docker** (optional, for containerized deployment)

### Installation

1. Clone the repository: `git clone https://github.com/youtipie/IoTWebApp.git cd IoTWebApp`

2. Install dependencies: `poetry install`

3. Configure environment variables in a `.env` file (or use default from `.env_example`):
    * `SECRET_KEY` - Secret key of app. Leave blank to generate random.
    * `SQLALCHEMY_DATABASE_URI` - Database connection string.
    * `SQLALCHEMY_TRACK_MODIFICATIONS` - Leave at 0.
    * `JWT_SECRET_KEY` - Secret key used to generate JWT token. Leave blank to generate random.
    * `JWT_ACCESS_TOKEN_EXPIRES` - Time in minutes after which the JWT access token becomes invalid.
    * `JWT_COOKIE_SECURE` - If true this will only allow the cookies that contain your JWTs to be sent over https. In
      production, this should always be set to True.
    * `JWT_COOKIE_CSRF_PROTECT` - Enables csrf protection. Leave as false when testing, because swagger won't work.
4. Start the application: `poetry run backend/asgi.py` or using uvicorn `uvicorn backend/asgi:app`

API Documentation
-----------------

Detailed API documentation with request and response formats is available
in the `/apidocs` endpoint after running the app.

License
-------

This project is licensed under the MIT License.
