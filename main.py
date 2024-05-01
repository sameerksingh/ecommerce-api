from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils import create_jwt_token, authenticate_creds
from app.views import product_views, user_views, cart_views, order_views
import uvicorn

app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(product_views.router)
app.include_router(user_views.router)
app.include_router(cart_views.router)
app.include_router(order_views.router)


# Login endpoint to obtain JWT token
@app.post("/api/login")
async def login(payload: dict):
    # Authenticate user (replace with actual authentication logic)
    username = payload["username"]
    password = payload["password"]
    role = authenticate_creds(username, password)
    token = create_jwt_token(username, role)
    return {"access_token": token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
