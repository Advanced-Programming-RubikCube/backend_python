# Rubik Timer

**Rubik Timer** is a web application that allows you to time your Rubik's Cube solving sessions. You can use the live timer to record your solving times, and if you sign up and log in, your solves will be saved so you can view your history and statistics (average time and best time).

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints (Advanced)](#api-endpoints-advanced)
- [Development](#development)
- [License](#license)

---

## Features

- **Live Timer:**  
  Start and stop the timer using the spacebar to record your solving time.
- **User Registration & Authentication:**  
  Sign up or log in to save your solve history.
- **Dashboard:**  
  View your solve history, including your average and best times.
- **Persistent Data:**  
  All data is stored in a JSON file that persists between container restarts.
- **Dockerized Deployment:**  
  Easily run the application using Docker and Docker Compose.

---

## Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1. Clone the Repository:

  ```bash
   git clone <repository_url>
   cd rubik-timer
  ```

2. Navigate to the project directory:

  ```bash
Copy
cd rubik-timer
  ```

3. Build and run the containers:

  ```bash
Copy
docker-compose up --build
  ```

4. Access the application:
  
  ```bash
Frontend: http://localhost:3000
Backend API: http://localhost:3001
  ```

## Usage

### 1. Open the Application

- Open your web browser and navigate to:  
  **[http://localhost:3000](http://localhost:3000)**

### 2. Using the Timer

- **Live Timer:**  
  The main page displays a large timer.
  
- **Start/Stop the Timer:**  
  - **Start:** Press and release the spacebar to start the timer.
  - **Stop:** Press the spacebar again to stop the timer.
  
- **Result:**  
  When you stop the timer, your recorded time will be displayed on the screen.

### 3. User Registration and Login

- **Using the App Without an Account:**  
  - You can use the timer without logging in, but your solve times will not be saved for future reference.
  
- **Saving Your Solve History:**  
  - To save your solve history, click the **Login** or **Sign Up** buttons located in the top-right corner.
  - An authentication modal will appear:
    - **Sign Up:** Enter a unique username and password to create an account.
    - **Login:** Enter your credentials to log in.
  - Upon successful authentication:
    - Your username will appear in the header along with a **Logout** button.
    - A sidebar (left panel) will be displayed, showing your solve history and statistics.

### 4. Dashboard Overview

- **Sidebar (Dashboard):**  
  When logged in, the sidebar on the left displays:
  - **Statistics:**  
    - **Average Time:** Your average solve time.
    - **Best Time:** Your best (minimum) solve time.
  - **Solve History:**  
    - A list of all your recorded solves is displayed below the statistics.

### 5. Logging Out

- To log out, simply click the **Logout** button in the header.
- Once logged out, your solves will not be saved until you log in again.


## API Endpoints (Advanced)

This section details the advanced API endpoints available in the Rubik Timer backend. These endpoints are intended for developers and advanced users who wish to interact directly with the API.

---

### GET /

**Description:**  
Returns a simple welcome message to indicate that the API is running.

**Request:**  
- **Method:** GET  
- **URL:** `http://localhost:3001/`

**Example Response:**

```json
{
    "message": "Welcome to the Rubik Timer API"
}
```

### POST /signup

**Description:**
Registers a new user by providing a unique username and password. If the username is already taken, an error is returned.

**Request:**
```
Method: POST
URL: http://localhost:3001/signup
Headers:
Content-Type: application/json
Body = 
{
    "username": "your_username",
    "password": "your_password"
}
```

### POST /login
**Description:**
Authenticates a user with their username and password, and returns a JWT token for authorized access to protected endpoints.

**Request:**

```

Method: POST
URL: http://localhost:3001/login
Headers:
(The Content-Type is set automatically when using form data.)
Body: (x-www-form-urlencoded)
```

```
Key	Value
username	your_username
password	your_password
```

### POST /solves/
**Description:**
Creates a new solve record for the authenticated user. The solve is associated with the user's username.

**Request:**

```

Method: POST
URL: http://localhost:3001/solves/
Headers:
Content-Type: application/json
Authorization: Bearer <JWT_token>
Body: (Raw JSON)
```

json

```
Copy
{
  "cube_type": "3x3",
  "solve_time": 12.34
}
```
Example Response:

json
```
Copy
{
  "id": 1,
  "cube_type": "3x3",
  "solve_time": 12.34,
  "timestamp": "2025-02-10T15:30:00.000000",
  "username": "your_username"
}
```

### GET /solves/
**Description:**
Retrieves the solve history for the authenticated user. Only solves associated with the user (by username) are returned.

**Request:**

```

Method: GET
URL: http://localhost:3001/solves/
Headers:
Authorization: Bearer <JWT_token>

```
Example Response:

json
```
Copy
[
  {
    "id": 1,
    "cube_type": "3x3",
    "solve_time": 12.34,
    "timestamp": "2025-02-10T15:30:00.000000",
    "username": "your_username"
  },
  {
    "id": 2,
    "cube_type": "3x3",
    "solve_time": 11.98,
    "timestamp": "2025-02-10T16:00:00.000000",
    "username": "your_username"
  }
]
```

### GET /solves/stats
**Description:**
Retrieves statistics (average time and best time) for each cube type based on the authenticated user's solves.

**Request:**

```

Method: GET
URL: http://localhost:3001/solves/stats
Headers:
Authorization: Bearer <JWT_token>
Example Response:

```

json
```
Copy
[
  {
    "cube_type": "3x3",
    "average_time": 12.16,
    "best_time": 11.98
  }
]
```
### GET /users/ (Debug Endpoint)
**Description:**
For development purposes only. Returns a list of all registered users, including their IDs, usernames, and hashed passwords. Do not expose this endpoint in production.

**Request:**

```

Method: GET
URL: http://localhost:3001/users/

```
Example Response:

json
```
Copy
[
  {
    "id": 1,
    "username": "user1",
    "hashed_password": "$2b$12$..."
  },
  {
    "id": 2,
    "username": "user2",
    "hashed_password": "$2b$12$..."
  }
]
```


# 7. Security Considerations
JWT Security:
Tokens are generated with a secret key and a secure algorithm.
The token includes an expiration time and the user's username (in the "sub" claim).
Password Security:
Passwords are hashed using bcrypt (via Passlib) before being stored.
Protected Endpoints:
Endpoints requiring authentication check for a valid JWT token.
Data Persistence:
The JSON database is stored in a persistent bind mount to prevent data loss.
Debug Endpoints:
Endpoints that expose sensitive information (e.g., /users/) should only be enabled for development or debugging purposes.
