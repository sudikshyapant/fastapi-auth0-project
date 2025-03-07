# FastAPI Auth0 JWT Authentication

Securely authenticate FastAPI endpoints using Auth0 JWT.


## Setup

### 1. Create Auth0 account
- Sign up at Auth0 and create a new API.
- Example API name: `fastapi-auth0-project_0`.


### 2. Configure Auth0 for JWT Authentication
```ini
[AUTH0]
DOMAIN = <YOUR_AUTH0_DOMAIN>  # Found in your Auth0 dashboard (e.g., dev-xxxxx.region.auth0.com)
API_AUDIENCE = <YOUR_API_AUDIENCE>  # Your API audience identifier from Auth0
ISSUER = https://<DOMAIN>
ALGORITHMS = RS256  # Algorithm used for JWT verification
```
Note: Replace `<YOUR_AUTH0_DOMAIN>`, `<YOUR_API_AUDIENCE>`, and `<YOUR_ISSUER_URL>` with actual values from your Auth0 account.

#### How to find your Auth0 domain:
- Go to your Auth0 Dashboard.
- Your domain is listed in the top-left corner (e.g., dev-xxxxx.us.auth0.com).
- If you selected the USA region, your domain will end in .us.auth0.com. Other regions have different suffixes.

### 3. Virtual Environment
```sh
python -m  venv venv  # Create virtual env
venv\Scripts\activate  # Activate virtual environment (Windows)
source venv/bin/activate  # Activate virtual environment (Mac/Linux)
```

### 4. Install Dependencies
```sh
python -m pip install -r dependency.txt  # Install dependencies
```

### 5. Run Server
```sh
uvicorn main:app --reload
```

### Access API Docs
- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)


## License
This project is licensed under the MIT License.

