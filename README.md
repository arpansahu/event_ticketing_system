---

# **Event Ticketing System**

This is a web-based Event Ticketing System built using Django REST framework that allows users to manage events, purchase tickets, and generate sales reports.

---

## **Table of Contents**
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
5. [Environment Variables](#environment-variables)
6. [Running the Application](#running-the-application)
7. [Running Without Docker](#running-without-docker)
8. [Running Tests](#running-tests)
9. [Postman Collection](#postman-collection)
10. [API Endpoints](#api-endpoints)
11. [Troubleshooting](#troubleshooting)
12. [Contributing](#contributing)
13. [License](#license)

---

## **Features**
- Event listing and creation
- Ticket purchasing with atomic transactions
- Reporting system for ticket sales and total revenue
- API documentation using Swagger (DRF Spectacular)
- Supports concurrent ticket purchases with database locking

---

## **Technologies Used**
- **Django**: Backend framework
- **Django REST Framework**: API development
- **PostgreSQL**: Database
- **Docker and Docker Compose**: Containerization
- **Gunicorn**: WSGI HTTP server for serving Django in production
- **DRF Spectacular**: API documentation

---

## **Prerequisites**
Ensure the following software is installed:
- **Git**: `https://git-scm.com/`
- **Python 3.10+**: `https://www.python.org/downloads/`
- **PostgreSQL**: `https://www.postgresql.org/download/`
- **Docker and Docker Compose** (if using Docker): `https://docs.docker.com/get-docker/`

---

## **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/arpansahu/event_ticketing_system.git
cd event_ticketing_system
```

---

## **Environment Variables**

| Variable            | Description                    |
|---------------------|----------------------------------|
| `DEFAULT_POSTGRES_DATABASE_NAME`  | PostgreSQL database name         |
| `DEFAULT_POSTGRES_USER`           | PostgreSQL username              |
| `DEFAULT_POSTGRES_PASSWORD`       | PostgreSQL password              |
| `DEFAULT_POSTGRES_HOST`           | Database hostname (`127.0.0.1` for local) |
| `DEFAULT_POSTGRES_PORT`           | Database port (`5433`)           |

---

## **Running the Application**

### **1. Running with Docker (Recommended)**
To run the project in a containerized environment using Docker:
1. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

2. Access the app at:
   - **Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
   - **ReDoc:** `http://127.0.0.1:8000/api/schema/redoc/`

---

## **Running Without Docker**

### **1. Update Database Variables in `settings.py`**

To run the project without Docker, update the following variables in `settings.py`:

```python
# ============================ ENV VARIABLES ============================
DEFAULT_POSTGRES_DATABASE_NAME = "event_ticketing_db"
DEFAULT_POSTGRES_USER = "event_user"
DEFAULT_POSTGRES_PASSWORD = "event_password"
DEFAULT_POSTGRES_HOST = "127.0.0.1"  # 'postgres' inside Docker
DEFAULT_POSTGRES_PORT = "5432"
```

---

### **2. Install PostgreSQL and Create a Database**

1. **Ensure PostgreSQL Server is Running:**
   ```bash
   sudo systemctl start postgresql  # For Linux
   brew services start postgresql   # For macOS (Homebrew)
   ```

2. **Access PostgreSQL Shell:**
   ```bash
   psql -U postgres
   ```

3. **Create Database and User:**
   ```sql
   CREATE DATABASE event_ticketing_db;
   CREATE USER event_user WITH PASSWORD 'event_password';
   GRANT ALL PRIVILEGES ON DATABASE event_ticketing_db TO event_user;
   ```

---

### **3. Create a Virtual Environment and Install Dependencies**

1. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate Virtual Environment:**
   ```bash
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

### **4. Run Database Migrations**

Apply database migrations:
```bash
python manage.py migrate
```

---

### **5. Seed the Database with Demo Data (Optional)**

Run the seed command to populate demo events and tickets:
```bash
python manage.py seed
```

---

### **6. Run the Development Server**

Start the Django development server:
```bash
python manage.py runserver
```
The application will be accessible at:
- **API Base URL:** `http://127.0.0.1:8000/`
- **Swagger UI (API Docs):** `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://127.0.0.1:8000/api/schema/redoc/`

---

## **Running Tests**

### **1. Run All Tests**
To run the complete test suite:
```bash
python manage.py test
```

---

### **2. Run Specific Test Files**

Here are the available test files and how to run them:

1. **Test Concurrency (`test_concurrency.py`)**
   - **Purpose:** Tests concurrent ticket purchases to ensure atomic transactions.
   ```bash
   python manage.py test tickets.tests.test_concurrency
   ```

2. **Test Events (`test_events.py`)**
   - **Purpose:** Tests the views related to event listing, creation, and details.
   ```bash
   python manage.py test tickets.tests.test_events
   ```

3. **Test Models (`test_models.py`)**
   - **Purpose:** Tests the database models to ensure correct field validations.
   ```bash
   python manage.py test tickets.tests.test_models
   ```

4. **Test Serializers (`test_serializers.py`)**
   - **Purpose:** Tests the data validation logic in serializers.
   ```bash
   python manage.py test tickets.tests.test_serializers
   ```

5. **Test Tickets (`test_tickets.py`)**
   - **Purpose:** Tests ticket-related operations such as ticket purchases.
   ```bash
   python manage.py test tickets.tests.test_tickets
   ```

---

## **Postman Collection**

### **1. Pre-Built Postman Collection**

The project includes a pre-built Postman collection that you can import for testing:
- **File Path:** `postman_collection/event_ticketing_system.postman_collection.json`

### **2. Import Steps**
1. Open **Postman**.
2. Click **Import**.
3. Select the file `event_ticketing_system.postman_collection.json`.
4. **Set the `baseUrl` Variable:**
   - In Postman, set the `baseUrl` environment variable to:
     ```plaintext
     http://127.0.0.1:8000
     ```
   - This is used to configure the API base URL.

---

## **API Endpoints**

| HTTP Method | Endpoint             | Description                       |
|-------------|----------------------|----------------------------------- |
| `GET`       | `/api/events/`        | List all events                   |
| `POST`      | `/api/events/`        | Create a new event                 |
| `GET`       | `/api/events/{id}/`   | Get event details by ID            |
| `POST`      | `/api/tickets/purchase/` | Purchase a ticket              |
| `GET`       | `/api/reports/`       | Get ticket sales report            |

---

## **API Documentation**
- **Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://127.0.0.1:8000/api/schema/redoc/`

---

## **Troubleshooting**

### **Common Issues**
1. **Database Connection Error**:
   - Ensure PostgreSQL is running.
   - Verify the `settings.py` has correct values for `DEFAULT_POSTGRES_DATABASE_NAME`, `DEFAULT_POSTGRES_USER`, and `DEFAULT_POSTGRES_PASSWORD`.

2. **Migration Errors**:
   - Run the following:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **PostgreSQL Access Error**:
   - Add this line to `pg_hba.conf` to allow local connections:
     ```bash
     local   all   event_user   md5
     ```
   - Restart PostgreSQL:
     ```bash
     sudo systemctl restart postgresql
     ```

4. **Docker Volume Issues**:
   - To clear the volumes and start fresh:
     ```bash
     docker-compose down -v
     docker-compose up --build
     ```

---

## **Contributing**
- Fork the repository
- Create a new branch (`feature/new-feature`)
- Commit your changes (`git commit -m "Add new feature"`)
- Push to the branch (`git push origin feature/new-feature`)
- Open a Pull Request

---

## **License**
This project is licensed under the MIT License.

---