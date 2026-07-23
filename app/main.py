import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from app.database import engine, Base, get_db, user as UserORM
from app.routers import estimator

def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')  # Convert the plain text password to byte tracking bytes
    salt = bcrypt.gensalt()                    # Generate a secure random salt configuration    
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)   
    # Hash the password and decode back to a string for MySQL storage
    return hashed_password_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Matches raw incoming text against the secure hashed password from MySQL"""
    try:
        # Convert both strings back to raw bytes for structural matching
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except Exception:
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n[DATABASE] Connecting to MySQL & verifying schema structures.")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("[DATABASE] Success! All database tables are synchronized.\n")
    except Exception as e:
        print("[DATABASE ERROR] Lifespan initialization failed:")
        traceback.print_exc()
    yield

app = FastAPI(title="Project Estimator & Profile Matcher", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(estimator.router)

# SECURE USER REGISTRATION ROUTE
@app.post("/api/register")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        # check if the email is already exist in the database
        email_check_query = select(UserORM).where(UserORM.email == email)
        result = await db.execute(email_check_query)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="An account with this email is already registered")

        # Hash the raw password variable securely using bcrypt
        secure_hashed_password = get_password_hash(password)
        # Create the data mapping dictionary using the user ORM
        new_record = UserORM(
            name=name,
            email=email,
            hashed_password=secure_hashed_password
        )
        # Stage record addition (get_db auto-commits on completion)
        db.add(new_record)

        return JSONResponse(
            status_code=201,
            content={"message": "Account created successfully! Redirecting..."}
        )

    except HTTPException:
        raise
    except Exception as err:
        print(f"[REGISTRATION PIPELINE FAILURE]: {err}")
        raise HTTPException(status_code=500, detail="Database insertion error")


# LOGIN ROUTE FOR USER
@app.post("/api/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = select(UserORM).where(UserORM.email == email)
        result = await db.execute(query)
        found_user = result.scalar_one_or_none()
        
        if not found_user:
            raise HTTPException(status_code=401, detail="Invalid email or password combination")
            
        # Verified via the hashing context helper
        if not verify_password(password, found_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password combination")
            
        return JSONResponse(
            status_code=200,
            content={"message": "Login successful", "redirect": "/dashboard.html"}
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AUTH ERROR LOG]: {e}")
        raise HTTPException(status_code=500, detail="Database processing failure")

# UI routing
@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/register.html")
def read_registration_page():
    """Serves the user account setup view layer"""
    return FileResponse("registration.html")

@app.get("/dashboard.html")
def read_dashboard():
    return FileResponse("dashboard.html")

@app.get("/analytics.html")
def read_analytics_dashboard():
    return FileResponse("analytics.html")
