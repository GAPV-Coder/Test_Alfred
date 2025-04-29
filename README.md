## Delivery Service API
The Delivery Service API is a RESTful API built with Django and Django REST Framework for managing delivery services. It allows users to create service requests, assign drivers, and complete services. The API uses JWT authentication to secure endpoints and includes logic to assign the nearest available driver based on geographic coordinates.
Features

Create and manage addresses, drivers, and services.
Request a delivery service with a pickup address (POST /api/service-request/).
Mark a service as completed and free the assigned driver (POST /api/service-complete/<id>/).
Retrieve a list of services (GET /api/services/).
JWT-based authentication for secure access.
Distance calculation to assign the nearest driver using the Haversine formula.
SQLite database for persistent storage.

## Tech Stack

Backend: Django, Django REST Framework
Authentication: Simple JWT
Database: SQLite
Configuration: python-decouple
Testing: Django's built-in testing framework

# Installation
Prerequisites

Python 3.13
Git

Steps

# Clone the Repository:
git clone <repository_url>
cd delivery_service


# Set Up a Virtual Environment:
python -m venv venv-delivery_service
.\venv-delivery_service\Scripts\activate  # On Windows
source venv-delivery_service/bin/activate  # On Linux/Mac


# Install Dependencies:
pip install -r requirements.txt

# Ensure requirements.txt includes:
django
djangorestframework
djangorestframework-simplejwt
python-decouple


# Configure Environment Variables:

Create a .env file in the project root (delivery_service/):SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1


# Generate a secure SECRET_KEY using:from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())




## Run Migrations:
python manage.py migrate


# Create a Superuser (for admin access and testing):
python manage.py createsuperuser

Example credentials: username: admin, password: admin123

Run the Development Server:
python manage.py runserver

The API will be available at `http://127.0.0.1:8000/.


# Authentication
Obtain a JWT access token via POST /api/token/. Include the token in the Authorization header: Bearer <access_token>.
Example: Obtain Token

Request:POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}


Response:{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}



## API Endpoints
All endpoints require authentication unless specified.

# Create a Service Request

Endpoint: POST /api/service-request/
Description: Creates a new service with a pickup address and assigns the nearest available driver.
Request:{
    "pickup_address": {
        "street": "TV56 La Paz St",
        "city": "Cartagena de Indias",
        "latitude": 10.3932,
        "longitude": -75.4832
    }
}


Response (201 Created):{
    "id": 1,
    "pickup_address": {
        "id": 1,
        "street": "TV56 La Paz St",
        "city": "Cartagena de Indias",
        "latitude": 10.3932,
        "longitude": -75.4832
    },
    "driver": {
        "id": 1,
        "name": "Test Driver",
        "location": {
            "id": 2,
            "street": "123 Main St",
            "city": "Mexico City",
            "latitude": 19.4326,
            "longitude": -99.1332
        },
        "is_available": false
    },
    "status": "IN_PROGRESS",
    "estimated_arrival_time": "2025-04-28T20:30:00Z",
    "created_at": "2025-04-28T20:00:00Z"
}


# Complete a Service

Endpoint: POST /api/service-complete/<id>/
Description: Marks a service as completed and makes the driver available again. No request body required.
Request:POST http://127.0.0.1:8000/api/service-complete/1/
Authorization: Bearer <access_token>


Response (200 OK):{
    "id": 1,
    "pickup_address": {
        "id": 1,
        "street": "TV56 La Paz St",
        "city": "Cartagena de Indias",
        "latitude": 10.3932,
        "longitude": -75.4832
    },
    "driver": {
        "id": 1,
        "name": "Test Driver",
        "location": {
            "id": 2,
            "street": "123 Main St",
            "city": "Mexico City",
            "latitude": 19.4326,
            "longitude": -99.1332
        },
        "is_available": true
    },
    "status": "COMPLETED",
    "estimated_arrival_time": "2025-04-28T20:30:00Z",
    "created_at": "2025-04-28T20:00:00Z"
}


# List Services

Endpoint: GET /api/services/
Description: Retrieves a list of all services.
Request:GET http://127.0.0.1:8000/api/services/
Authorization: Bearer <access_token>


Response (200 OK):[
    {
        "id": 1,
        "pickup_address": {
            "id": 1,
            "street": "TV56 La Paz St",
            "city": "Cartagena de Indias",
            "latitude": 10.3932,
            "longitude": -75.4832
        },
        "driver": {
            "id": 1,
            "name": "Test Driver",
            "location": {
                "id": 2,
                "street": "123 Main St",
                "city": "Mexico City",
                "latitude": 19.4326,
                "longitude": -99.1332
            },
            "is_available": true
        },
        "status": "COMPLETED",
        "estimated_arrival_time": "2025-04-28T20:30:00Z",
        "created_at": "2025-04-28T20:00:00Z"
    }
]


# Create a Driver

Endpoint: POST /api/drivers/
Description: Creates a new driver with a location.
Request:{
    "name": "Test Driver",
    "location_id": 1,
    "is_available": true
}


Response (201 Created):{
    "id": 1,
    "name": "Test Driver",
    "location": {
        "id": 1,
        "street": "123 Main St",
        "city": "Mexico City",
        "latitude": 19.4326,
        "longitude": -99.1332
    },
    "is_available": true
}


# Create an Address

Endpoint: POST /api/addresses/
Description: Creates a new address.
Request:{
    "street": "123 Main St",
    "city": "Mexico City",
    "latitude": 19.4326,
    "longitude": -99.1332
}


Response (201 Created):{
    "id": 1,
    "street": "123 Main St",
    "city": "Mexico City",
    "latitude": 19.4326,
    "longitude": -99.1332
}



## Testing
The project includes 12 unit tests to validate the API's functionality, model integrity, and service logic.
Run Tests
python manage.py test delivery

# Test Coverage

Total Tests: 12
Location: delivery/tests/
Files:
test_api.py (6 tests):
Tests creation of service requests with valid and invalid data.
Validates service completion, including edge cases (non-existent services, already completed).
Verifies service listing and authentication requirements.


test_models.py (3 tests):
Ensures Address, Driver, and Service models are correctly defined and saved.
Validates model fields and relationships (e.g., Driver.location, Service.driver).


test_services.py (3 tests):
Tests ServiceManager.find_nearest_driver for correct driver assignment based on distance.
Validates ServiceManager.create_service for service creation and driver availability updates.
Handles edge cases (e.g., no available drivers).



# Expected Output
Found 12 test(s).
System check identified no issues (0 silenced).
............
Ran 12 tests in 0.150s
OK

# Error Handling

401 Unauthorized: Missing or invalid JWT token.
400 Bad Request: Invalid request data or no drivers available.
404 Not Found: Service or resource not found.
500 Internal Server Error: Server-side issues (logged for debugging).

## Database Queries
To inspect the database, use the following SQL queries:
-- Services
SELECT id, status, driver_id FROM delivery_service WHERE id IN (1, 2);

-- Available Drivers
SELECT id, name, is_available FROM delivery_driver WHERE is_available = true LIMIT 5;

-- Specific Address
SELECT id, street, city FROM delivery_address WHERE id = 31;

-- List Addresses
SELECT id, street, city FROM delivery_address LIMIT 5;

-- List Drivers
SELECT id, name FROM delivery_driver LIMIT 5;

## Notes

Ensure at least one driver with is_available=True exists before creating a service request.
The estimated_arrival_time is calculated based on distance (assuming 40 km/h average speed).
Models are imported directly (e.g., from delivery.models.address import Address) to avoid conflicts caused by delivery/models/__init__.py.
Requires python-decouple for configuration. Install with pip install python-decouple.
Models use app_label = 'delivery' in their Meta classes.
Use Postman or cURL for testing API endpoints.

## Troubleshooting

ModuleNotFoundError: No module named 'decouple':Install python-decouple:pip install python-decouple


RuntimeError: Conflicting 'address' models:Ensure delivery/models/__init__.py is empty and imports use from delivery.models.address import Address.
ImportError:Verify relative imports (e.g., from ..models.address import Address in api/, tests/, services/).
Database Errors:Run migrations:python manage.py makemigrations
python manage.py migrate


No Drivers Available:Create a driver with POST /api/drivers/ and set is_available=True.

## AWS Deployment (Conceptual)

# Recommended Services

Amazon ECS with Fargate: For running application containers without managing servers.
Amazon RDS (PostgreSQL): Managed relational database for high availability.
Elastic Load Balancer (ALB): To distribute traffic and enhance scalability.
Amazon Route 53: For DNS management.
AWS Secrets Manager: To store sensitive variables like SECRET_KEY and database credentials.
Amazon CloudWatch: For monitoring and logging.

## Deployment Steps

# Containerization:

Use the existing Dockerfile and docker-compose.yml to build the application image.

ECR: Push the image to Amazon Elastic Container Registry (ECR).

ECS: Set up an ECS cluster with Fargate. Define tasks using the application image.
Configure the ALB to route traffic to the ECS service.

RDS: Create a PostgreSQL instance in RDS.

# Configure ECS environment variables to connect to the RDS database.

# Security: 
Use security groups to restrict access to RDS and ECS.
Implement AWS WAF to protect the API from common attacks.
Enable HTTPS on the ALB with a certificate from AWS Certificate Manager.

# Scalability:
Configure auto-scaling in ECS based on CPU/memory metrics.
Use RDS Multi-AZ for high availability.

# CI/CD:
Set up a pipeline with AWS CodePipeline and CodeBuild to automate deployments.

## Considerations

Security: Store secrets in Secrets Manager and rotate credentials regularly.

Scalability: Use Fargate for horizontal scaling without managing underlying infrastructure.

Cost: Monitor usage with AWS Cost Explorer to optimize resources.

## Documentation API Postman
https://documenter.getpostman.com/view/27313712/2sB2j3AB4S

## License
This project is licensed under the MIT License.
