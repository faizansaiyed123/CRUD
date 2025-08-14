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



Postman Collection Setup:
1: Import the collection
Open Postman → Import → File → Select LawVriksh_Backend.postman_collection.json

2: Create an environment
Click the gear icon → Manage Environments → Add
Name: LawVriksh
Add variables:
Key	Value
base_url	http://127.0.0.1:8000
access_token	(leave empty initially)

3:Add auto-token capture script
In both Signup and Login requests, go to the Tests tab and paste:

const response = pm.response.json();
const token = response.token || response.data?.token || response.data?.access_token;
if (token) {
    pm.environment.set("access_token", token);
}


Usage:

1: Run Signup to create a new user.
-> The token will be returned and stored automatically in the access_token environment variable.

2: Run Login to log in with your credentials.
->The script will update the token automatically.

3:Test authenticated endpoints:
-> Create Post
->Update Post
->Delete Post
->Like Post
->Comment on Post

4:Test non-authenticated endpoints directly:
->Get Posts
->Get Comments

Notes:
1: Ensure your FastAPI server is running:
-> uvicorn app.main:app --reload