# LawVriksh Backend Assignment

## Project Overview
This is a backend project for the LawVriksh internship assignment.  
It implements a **blog management system** with CRUD operations, likes, and comments using **FastAPI** and **PostgreSQL**.

## Features

- **User Authentication**
  - Signup (`POST /api/auth/signup`)
  - Login (`POST /api/auth/login`) using JWT
- **Blog Post CRUD**
  - Create (`POST /api/posts/`) ✅ Auth required
  - Read all posts (`GET /api/posts/`) ❌ Auth optional
  - Read single post (`GET /api/posts/{id}`) ❌ Auth optional
  - Update (`PUT /api/posts/{id}`) ✅ Auth required, only author
  - Delete (`DELETE /api/posts/{id}`) ✅ Auth required, only author
- **Like Functionality**
  - Like a post (`POST /api/posts/{id}/like`) ✅ Auth required, one like per user
- **Comment Functionality**
  - Add comment (`POST /api/posts/{id}/comment`) ✅ Auth required
  - Get comments (`GET /api/posts/{id}/comments`) ❌ Auth optional

  

## Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic schemas
- JWT authentication
- Postman for API testing

## Setup Instructions

1. **Clone the repo (if not already)**  
```bash
git clone https://github.com/faizansaiyed123/CRUD.git
cd CRUD


2: Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux



3:Install dependencies
pip install -r requirements.txt


4: Configure environment variables (create .env file)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql://user:password@localhost:5432/your-db


5:Run the project
uvicorn app.main:app --reload


6:Access API docs
Open http://127.0.0.1:8000/docs in your browser.



Postman Collection :
1: Open Postman.
Click Import → File, and select LawVriksh_Backend.postman_collection.json.

2: The collection will appear in your workspace.

3: Create a Postman Environment:

4: Click the gear icon → Manage Environments → Add.

5: Name it LawVriksh.

6: Add variables:

Key	Value
7: base_url	http://127.0.0.1:8000
8: access_token	(leave empty initially)

9: Save the environment and select it in Postman.

10: Open the Signup request and in Login request in Postman.
11: Go to the Tests tab.
12: Paste the following script:

const response = pm.response.json();
const token = response.token || response.data?.token || response.data?.access_token;
if (token) {
    pm.environment.set("access_token", token);
}



Usage:
Run Signup first to create a new user.
Run Login to obtain the access_token.
Copy the returned token into the access_token environment variable.
You can now test all authenticated endpoints (Create Post, Update, Delete, Like, Comment).
Non-authenticated endpoints (Get Posts, Get Comments) can be tested directly.

Notes:
Make sure your FastAPI server is running:
uvicorn app.main:app --reload


Update the .env file with your database credentials and secret key before running.