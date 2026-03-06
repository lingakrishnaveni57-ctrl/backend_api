from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Auth API",
    description="Signup with OTP, login, and profile endpoints. Provides JWT authentication."
)

# Include routes
app.include_router(router)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # local dev
        "https://frontend-ui-five-teal.vercel.app"  # Vercel frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route
@app.get("/")
def root():
    return {"message": "Backend API is running"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

