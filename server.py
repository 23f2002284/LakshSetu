# main.py
from typing import Union
from fastapi import FastAPI, HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import UserProfile
import uvicorn
from table import UserDB,SessionLocal
from sqlalchemy.orm import Session
# Create FastAPI app
app = FastAPI(
    title="User Registration API",
    description="API for user profile registration",
    version="1.0.0"
)

# Add CORS middleware - IMPORTANT for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
    return {"message": " API is running!", "status": "healthy"}


@app.post("/registration")
async def user_registration(user_data: UserProfile, db: Session = Depends(get_db)):
  
    try:
        print(f"Received registration for: {user_data.name}")
        print(f"Email: {user_data.email}")
        # print(f"Skills: {user_data.skills}")

        existing_user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        # Create new user in database
        db_user = UserDB(
            name=user_data.name,
            email=user_data.email,
            profile_data=user_data.model_dump()  # Store complete profile as JSON
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        print(f"User saved to database with ID: {db_user.id}")
        
        return {
            "message": "Registration successful",
            "user_id": db_user.id,
            "user_name": db_user.name,
            "user_email": db_user.email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
                
       



# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)