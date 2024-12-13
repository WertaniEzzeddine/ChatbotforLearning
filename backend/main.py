from fastapi import FastAPI, HTTPException, Depends,File, Header, UploadFile, Form, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from database import SessionLocal, engine
from models import *
from schemas import *
from fastapi.middleware.cors import CORSMiddleware  

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from summarize import *
from fastapi.security import OAuth2PasswordBearer
# Initialize FastAPI App
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, use specific URLs to limit access
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hashes a plain-text password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against its hashed counterpart."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Creates a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )



@app.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password securely
        hashed_password = hash_password(user.password)

        # Create new user object
        new_user = User(
            full_name=user.full_name,
            email=user.email,
            password=hashed_password
        )

        # Add user to the database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Response
        return {"message": "User registered successfully", "user": {"id": new_user.id, "email": new_user.email}}

    except Exception as e:
        # Log the exception and raise HTTP error
        print(f"Error during user registration: {e}")  # Debugging
        raise HTTPException(status_code=500, detail="An error occurred while registering the user")


@app.post("/login")
async def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Verify the password
    if not bcrypt.verify(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
        # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email,"id":user.id}, expires_delta=access_token_expires)

    # Return token and user information
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name}
    }




# Ensure the upload directory exists


@app.post("/upload_course/")
async def upload_course(
    name: str = Form(...), 
    user_id: int = Form(...), 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    UPLOAD_DIRECTORY = "./uploads/"
    try:
        # Save the file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{file.filename}"        
        # Generate a public URL (adjust according to your server setup)
        file_url = UPLOAD_DIRECTORY+filename

        with open(file_url, "wb") as f:
            f.write(await file.read())

            
        text=extract_text_from_pdf(file_url)
        text=text[:5999]
        
        prompt="make a summary for this in english:"+text
        response = llm.invoke(prompt)
        exam=llm.invoke("generate an exam without answers based on this:"+response.content)
        correction=llm.invoke("generate organised correction for this exam:"+exam.content)
        # Simulate saving to the database
       
        data =Course(name=name,
            pdf_files= file_url,
            user_id= user_id,
            summary=response.content,
            exam=exam.content,
            exam_correction=correction.content
            )
        db.add(data)
        db.commit()
        db.refresh(data)
        cours=db.query(Course).filter(Course.pdf_files==data.pdf_files ).all()
        cour=cours[0]
        serialized_course ={
                "id": cour.id,
                "name": cour.name,
                "pdf_files": cour.pdf_files,
                "summary": cour.summary,
                "created_at": cour.created_at.isoformat(),
                "user_id": cour.user_id,
                "conversation": cour.conversation or None,
                "exam":cour.exam,
                "exam_correction":cour.exam_correction

            }
            
        
 
        
        # Return the response
        return JSONResponse(content={"message": "Course uploaded successfully!", "course": serialized_course}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
def decode_jwt(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded token's payload (user info, etc.)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/courses/")
async def get_courses_by_user(Authorization: str = Header(...), db: Session = Depends(get_db)):
    token = Authorization.split(" ")[1]
    decoded_data = decode_jwt(token)
    # Extract user data from the decoded token
    user_id = decoded_data.get("id")
    try:
        # Query the database for all courses with the given token
        courses = db.query(Course).filter(Course.user_id == user_id).all()
        
        if not courses:
            raise HTTPException(status_code=404, detail="No courses found for this user")

        # Serialize the courses to JSON-compatible format
        courses_response = [course for course in courses]
        print("aaaa:",courses_response)

        # Return the courses
        return {"courses": courses_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
















class Message(BaseModel):
    course_id:int
    sender: str
    text: str


@app.post("/chat/")
def chat(message: Message, db: Session = Depends(get_db)):
    # Save user message
    user_message = ChatMessage(course_id=message.course_id, sender=message.sender, text=message.text)
    db.add(user_message)
    db.commit()
    course = db.query(Course).filter(Course.id == message.course_id).all()
    summary=course[0].summary
    # Generate bot response
    if message.sender == "user":
        prompt="in this context:"+summary+" \nanswer this:"+message.text
        response = llm.invoke(prompt)
        bot_response_text = response.content
        bot_response = ChatMessage(course_id=message.course_id,sender="bot", text=bot_response_text)
        db.add(bot_response)
        db.commit()
        return {"sender": "bot", "text": bot_response_text}
    else:
        raise HTTPException(status_code=400, detail="Invalid sender")

@app.get("/chat/history/{course_id}/")
def get_chat_history(course_id: int,db: Session = Depends(get_db)):
    history = db.query(ChatMessage).filter(ChatMessage.course_id==course_id).all()
    return [{"sender": msg.sender, "text": msg.text} for msg in history]
   
