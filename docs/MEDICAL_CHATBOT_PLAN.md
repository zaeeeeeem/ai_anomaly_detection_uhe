# Medical Chatbot Portal - Implementation Plan

## Project Overview
A medical-related chatbot portal with user authentication, conversation management, and multi-model AI support (Gemini API + Ollama local models).

### Key Features
- User authentication (Login/Signup)
- Conversation management with sidebar navigation
- Real-time chat interface
- Multi-model AI support (Gemini API + Ollama)
- 100vh layout with no page scroll (individual sections scroll independently)

---

## PHASE 0: PROJECT SETUP & INITIALIZATION

### 0.1 Project Structure Setup

#### Directory Structure
```
medical-chatbot-portal/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── conversations.py
│   │   │   └── chat.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── gemini_service.py
│   │   │   └── ollama_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py
│   │       └── dependencies.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
└── README.md
```

### 0.2 Technology Stack Selection

#### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **AI Integration**:
  - Google Gemini API (google-generativeai)
  - Ollama API (requests/httpx)
- **WebSocket**: FastAPI WebSockets
- **Environment**: python-dotenv
- **Validation**: Pydantic v2

#### Frontend
- **Framework**: React 18+ with Vite
- **Routing**: React Router v6
- **State Management**: Context API + useReducer (or Zustand for advanced)
- **HTTP Client**: Axios
- **WebSocket**: native WebSocket API or socket.io-client
- **Styling**: CSS Modules / Styled Components (as per Frontend SKILL.md)
- **Form Handling**: React Hook Form
- **Validation**: Zod
- **Icons**: Lucide React or custom SVGs

### 0.3 Development Environment Setup

#### Prerequisites
```bash
# System Requirements
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git
- Ollama (for local models)
```

#### Backend Setup Commands
```bash
# Create backend directory
mkdir -p backend/app/{models,schemas,routers,services,utils}
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create requirements.txt (see section 0.4)
touch requirements.txt

# Install dependencies
pip install -r requirements.txt

# Create .env file
touch .env
```

#### Frontend Setup Commands
```bash
# Create frontend with Vite
npm create vite@latest frontend -- --template react
cd frontend

# Install dependencies (see section 0.5)
npm install

# Create .env file
touch .env.local
```

### 0.4 Backend Dependencies

#### requirements.txt
```txt
# Core Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.9

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1
bcrypt==4.1.2

# AI Services
google-generativeai==0.3.2
httpx==0.26.0

# Data Validation
pydantic==2.5.3
pydantic-settings==2.1.0
email-validator==2.1.0

# CORS
python-cors==1.0.0

# Testing (optional but recommended)
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
```

### 0.5 Frontend Dependencies

#### package.json additions
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.3",
    "axios": "^1.6.5",
    "react-hook-form": "^7.49.3",
    "zod": "^3.22.4",
    "@hookform/resolvers": "^3.3.4",
    "lucide-react": "^0.309.0",
    "framer-motion": "^10.18.0"
  }
}
```

Install command:
```bash
npm install react-router-dom axios react-hook-form zod @hookform/resolvers lucide-react framer-motion
```

### 0.6 Environment Configuration

#### Backend .env.example
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/medical_chatbot
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_chatbot
DB_USER=your_username
DB_PASSWORD=your_password

# JWT Configuration
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama2

# Application Settings
APP_NAME="Medical Chatbot Portal"
APP_VERSION=1.0.0
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

#### Frontend .env.local.example
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME="Medical Chatbot Portal"
```

### 0.7 Database Setup

#### PostgreSQL Database Creation
```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE medical_chatbot;

# Create user (if needed)
CREATE USER medical_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE medical_chatbot TO medical_user;

# Exit
\q
```

#### Alembic Initialization
```bash
cd backend

# Initialize Alembic
alembic init alembic

# Update alembic.ini with your database URL
# Edit alembic/env.py to import your models
```

### 0.8 Ollama Setup

#### Install Ollama
```bash
# For macOS
brew install ollama

# For Linux
curl -fsSL https://ollama.com/install.sh | sh

# For Windows - Download from https://ollama.com/download
```

#### Pull Medical-Related Models
```bash
# Start Ollama service
ollama serve

# Pull recommended models (in another terminal)
ollama pull llama2
ollama pull medllama2  # Medical-specific model if available
ollama pull mistral
ollama pull codellama  # For technical medical queries

# Test Ollama
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "What is hypertension?"
}'
```

### 0.9 Project Initialization Checklist

- [ ] Create project directory structure
- [ ] Set up Python virtual environment
- [ ] Install backend dependencies
- [ ] Set up Node.js frontend project
- [ ] Install frontend dependencies
- [ ] Create and configure .env files for backend and frontend
- [ ] Set up PostgreSQL database
- [ ] Initialize Alembic for migrations
- [ ] Install and configure Ollama
- [ ] Pull necessary Ollama models
- [ ] Obtain Google Gemini API key
- [ ] Initialize Git repository
- [ ] Create .gitignore files

#### .gitignore (Root Level)
```gitignore
# Environment files
.env
.env.local
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/
.Python

# Node
node_modules/
dist/
.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite

# Logs
*.log
```

---

## PHASE 1: BACKEND DEVELOPMENT

### 1.1 Database Models Design

#### 1.1.1 User Model (app/models/user.py)

**Purpose**: Store user authentication and profile information

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
```

#### 1.1.2 Conversation Model (app/models/conversation.py)

**Purpose**: Store conversation metadata and settings

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class ModelType(enum.Enum):
    GEMINI = "gemini"
    OLLAMA = "ollama"

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False, default="New Conversation")
    model_type = Column(Enum(ModelType), nullable=False, default=ModelType.GEMINI)
    model_name = Column(String, nullable=False, default="gemini-pro")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
```

#### 1.1.3 Message Model (app/models/message.py)

**Purpose**: Store individual chat messages

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class MessageRole(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
```

### 1.2 Pydantic Schemas

#### 1.2.1 User Schemas (app/schemas/user.py)

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
```

#### 1.2.2 Conversation Schemas (app/schemas/conversation.py)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.conversation import ModelType

class ConversationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    model_type: ModelType
    model_name: str

class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    model_type: ModelType = ModelType.GEMINI
    model_name: str = "gemini-pro"

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    model_type: Optional[ModelType] = None
    model_name: Optional[str] = None

class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    message_count: Optional[int] = 0
    last_message_preview: Optional[str] = None

    class Config:
        from_attributes = True
```

#### 1.2.3 Message Schemas (app/schemas/message.py)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.message import MessageRole

class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)
    role: MessageRole

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    conversation_id: int
    message: str = Field(..., min_length=1)
    model_type: Optional[ModelType] = None
    model_name: Optional[str] = None

class ChatResponse(BaseModel):
    message_id: int
    content: str
    role: MessageRole
    created_at: datetime
```

### 1.3 Database Configuration

#### 1.3.1 Database Setup (app/database.py)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 1.3.2 Configuration (app/config.py)

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Gemini
    GEMINI_API_KEY: str

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_DEFAULT_MODEL: str = "llama2"

    # Application
    APP_NAME: str = "Medical Chatbot Portal"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 1.4 Security & Authentication

#### 1.4.1 Security Utilities (app/utils/security.py)

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT access token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None
```

#### 1.4.2 Dependencies (app/utils/dependencies.py)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = decode_access_token(token)
    if email is None:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### 1.5 AI Services Implementation

#### 1.5.1 Gemini Service (app/services/gemini_service.py)

```python
import google.generativeai as genai
from typing import List, Dict
from app.config import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiService:
    """Service for interacting with Google Gemini API"""

    def __init__(self):
        self.available_models = [
            "gemini-pro",
            "gemini-pro-vision",
        ]

    def get_available_models(self) -> List[str]:
        """Get list of available Gemini models"""
        return self.available_models

    async def generate_response(
        self,
        message: str,
        model_name: str = "gemini-pro",
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate a response using Gemini API

        Args:
            message: User's message
            model_name: Gemini model to use
            conversation_history: Previous messages for context

        Returns:
            Generated response text
        """
        try:
            model = genai.GenerativeModel(model_name)

            # Build context from conversation history
            if conversation_history:
                # Format history for Gemini
                history_text = "\n".join([
                    f"{msg['role']}: {msg['content']}"
                    for msg in conversation_history[-10:]  # Last 10 messages for context
                ])
                full_prompt = f"{history_text}\nuser: {message}\nassistant:"
            else:
                full_prompt = message

            # Add medical context system prompt
            system_prompt = """You are a helpful medical assistant AI. Provide accurate,
            evidence-based medical information. Always remind users to consult with healthcare
            professionals for personal medical advice. Do not provide diagnoses or treatment
            recommendations without proper medical consultation."""

            full_prompt = f"{system_prompt}\n\n{full_prompt}"

            # Generate response
            response = model.generate_content(full_prompt)

            return response.text

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

    async def stream_response(
        self,
        message: str,
        model_name: str = "gemini-pro",
        conversation_history: List[Dict[str, str]] = None
    ):
        """
        Stream response from Gemini API (for future WebSocket implementation)

        Args:
            message: User's message
            model_name: Gemini model to use
            conversation_history: Previous messages for context

        Yields:
            Response chunks
        """
        try:
            model = genai.GenerativeModel(model_name)

            # Build context
            if conversation_history:
                history_text = "\n".join([
                    f"{msg['role']}: {msg['content']}"
                    for msg in conversation_history[-10:]
                ])
                full_prompt = f"{history_text}\nuser: {message}\nassistant:"
            else:
                full_prompt = message

            system_prompt = """You are a helpful medical assistant AI. Provide accurate,
            evidence-based medical information."""

            full_prompt = f"{system_prompt}\n\n{full_prompt}"

            # Stream response
            response = model.generate_content(full_prompt, stream=True)

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            raise Exception(f"Gemini streaming error: {str(e)}")


# Create singleton instance
gemini_service = GeminiService()
```

#### 1.5.2 Ollama Service (app/services/ollama_service.py)

```python
import httpx
from typing import List, Dict, Optional
from app.config import settings

class OllamaService:
    """Service for interacting with local Ollama models"""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.default_model = settings.OLLAMA_DEFAULT_MODEL

    async def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of available Ollama models"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [
                        {
                            "name": model["name"],
                            "size": model.get("size", "unknown")
                        }
                        for model in data.get("models", [])
                    ]
                return []
        except Exception as e:
            print(f"Error fetching Ollama models: {str(e)}")
            return []

    async def generate_response(
        self,
        message: str,
        model_name: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate a response using Ollama API

        Args:
            message: User's message
            model_name: Ollama model to use
            conversation_history: Previous messages for context

        Returns:
            Generated response text
        """
        if not model_name:
            model_name = self.default_model

        try:
            # Build conversation context
            context = self._build_context(conversation_history)

            # Medical system prompt
            system_prompt = """You are a helpful medical assistant. Provide accurate medical
            information while reminding users to consult healthcare professionals for personal advice."""

            # Build prompt
            full_prompt = f"{system_prompt}\n\n{context}User: {message}\nAssistant:"

            # Make request to Ollama
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": full_prompt,
                        "stream": False
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                else:
                    raise Exception(f"Ollama API returned status {response.status_code}")

        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")

    async def stream_response(
        self,
        message: str,
        model_name: Optional[str] = None,
        conversation_history: List[Dict[str, str]] = None
    ):
        """
        Stream response from Ollama API

        Args:
            message: User's message
            model_name: Ollama model to use
            conversation_history: Previous messages for context

        Yields:
            Response chunks
        """
        if not model_name:
            model_name = self.default_model

        try:
            context = self._build_context(conversation_history)
            system_prompt = """You are a helpful medical assistant."""

            full_prompt = f"{system_prompt}\n\n{context}User: {message}\nAssistant:"

            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": full_prompt,
                        "stream": True
                    }
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                import json
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            raise Exception(f"Ollama streaming error: {str(e)}")

    def _build_context(self, conversation_history: List[Dict[str, str]] = None) -> str:
        """Build conversation context from history"""
        if not conversation_history:
            return ""

        context = ""
        for msg in conversation_history[-10:]:  # Last 10 messages
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"

        return context

    async def check_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception:
            return False


# Create singleton instance
ollama_service = OllamaService()
```

#### 1.5.3 Authentication Service (app/services/auth_service.py)

```python
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings

class AuthService:
    """Service for authentication operations"""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def authenticate_user(db: Session, credentials: UserLogin) -> Token:
        """Authenticate user and return JWT token"""
        user = db.query(User).filter(User.email == credentials.email).first()

        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")


# Create singleton instance
auth_service = AuthService()
```

### 1.6 API Routers/Endpoints

#### 1.6.1 Authentication Router (app/routers/auth.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    - **email**: Valid email address
    - **username**: Unique username (3-50 characters)
    - **password**: Strong password (minimum 8 characters)
    - **full_name**: Optional full name
    """
    user = auth_service.create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and get access token

    - **email**: User's email
    - **password**: User's password

    Returns JWT access token for subsequent requests
    """
    token = auth_service.authenticate_user(db, credentials)
    return token


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Get current authenticated user information"""
    return current_user


@router.post("/logout")
def logout():
    """
    Logout endpoint (client should discard token)
    JWT tokens are stateless, so logout is handled client-side
    """
    return {"message": "Logged out successfully"}
```

#### 1.6.2 Conversations Router (app/routers/conversations.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse,
    ConversationUpdate
)
from app.schemas.message import MessageResponse
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new conversation

    - **title**: Conversation title (default: "New Conversation")
    - **model_type**: AI model type (gemini or ollama)
    - **model_name**: Specific model to use
    """
    conversation = Conversation(
        user_id=current_user.id,
        title=conversation_data.title,
        model_type=conversation_data.model_type,
        model_name=conversation_data.model_name
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


@router.get("", response_model=List[ConversationResponse])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all conversations for current user

    Returns conversations ordered by most recently updated
    """
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Add message count and preview to each conversation
    result = []
    for conv in conversations:
        conv_dict = {
            "id": conv.id,
            "title": conv.title,
            "model_type": conv.model_type,
            "model_name": conv.model_name,
            "user_id": conv.user_id,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": len(conv.messages),
            "last_message_preview": conv.messages[-1].content[:100] if conv.messages else None
        }
        result.append(conv_dict)

    return result


@router.get("/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific conversation by ID"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    return conversation


@router.put("/{conversation_id}", response_model=ConversationResponse)
def update_conversation(
    conversation_id: int,
    update_data: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update conversation details

    - **title**: New conversation title
    - **model_type**: Change AI model type
    - **model_name**: Change specific model
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Update fields if provided
    if update_data.title is not None:
        conversation.title = update_data.title
    if update_data.model_type is not None:
        conversation.model_type = update_data.model_type
    if update_data.model_name is not None:
        conversation.model_name = update_data.model_name

    db.commit()
    db.refresh(conversation)

    return conversation


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a conversation and all its messages"""
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    db.delete(conversation)
    db.commit()

    return None


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all messages in a conversation"""
    # Verify conversation ownership
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return messages
```

#### 1.6.3 Chat Router (app/routers/chat.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation, ModelType
from app.models.message import Message, MessageRole
from app.schemas.message import MessageCreate, MessageResponse
from app.services.gemini_service import gemini_service
from app.services.ollama_service import ollama_service
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/{conversation_id}/message", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send a message and get AI response

    - **conversation_id**: ID of the conversation
    - **content**: Message content

    Returns the AI's response message
    """
    # Verify conversation ownership
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Save user message
    user_message = Message(
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=message_data.content
    )
    db.add(user_message)
    db.commit()

    # Get conversation history for context
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc()).all()

    conversation_history = [
        {"role": msg.role.value, "content": msg.content}
        for msg in messages[:-1]  # Exclude the just-added user message
    ]

    # Generate AI response based on model type
    try:
        if conversation.model_type == ModelType.GEMINI:
            ai_response = await gemini_service.generate_response(
                message=message_data.content,
                model_name=conversation.model_name,
                conversation_history=conversation_history
            )
        elif conversation.model_type == ModelType.OLLAMA:
            ai_response = await ollama_service.generate_response(
                message=message_data.content,
                model_name=conversation.model_name,
                conversation_history=conversation_history
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid model type"
            )

        # Save AI response
        assistant_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)

        return assistant_message

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )


@router.get("/models/gemini")
def get_gemini_models():
    """Get available Gemini models"""
    return {"models": gemini_service.get_available_models()}


@router.get("/models/ollama")
async def get_ollama_models():
    """Get available Ollama models"""
    models = await ollama_service.get_available_models()
    return {"models": models}


@router.get("/ollama/status")
async def check_ollama_status():
    """Check if Ollama is running"""
    is_running = await ollama_service.check_connection()
    return {
        "status": "online" if is_running else "offline",
        "url": ollama_service.base_url
    }
```

### 1.7 Main Application File

#### 1.7.1 Main App (app/main.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, conversations, chat

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Medical Chatbot Portal with AI assistance",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(conversations.router)
app.include_router(chat.router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Medical Chatbot Portal API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
```

#### 1.7.2 Models Init (app/models/__init__.py)

```python
from app.models.user import User
from app.models.conversation import Conversation, ModelType
from app.models.message import Message, MessageRole

__all__ = ["User", "Conversation", "Message", "ModelType", "MessageRole"]
```

#### 1.7.3 Routers Init (app/routers/__init__.py)

```python
from app.routers import auth, conversations, chat

__all__ = ["auth", "conversations", "chat"]
```

### 1.8 Database Migrations

#### 1.8.1 Alembic Configuration

**Edit alembic/env.py:**

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
from app.models import *  # Import all models
from app.config import settings

# this is the Alembic Config object
config = context.config

# Set database URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# ... rest of the env.py file
```

#### 1.8.2 Create Initial Migration

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 1.9 Running the Backend

#### 1.9.1 Development Server

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run with uvicorn (auto-reload enabled)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python -m app.main
```

#### 1.9.2 Testing Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "securepass123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepass123"
  }'

# Create conversation (with token)
curl -X POST http://localhost:8000/api/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Medical Question",
    "model_type": "gemini",
    "model_name": "gemini-pro"
  }'

# Send message
curl -X POST http://localhost:8000/api/chat/1/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "content": "What are the symptoms of hypertension?"
  }'
```

### 1.10 Backend Phase 1 Checklist

- [ ] Create all database models (User, Conversation, Message)
- [ ] Create all Pydantic schemas
- [ ] Set up database configuration and connection
- [ ] Implement security utilities (JWT, password hashing)
- [ ] Create authentication dependencies
- [ ] Implement Gemini service
- [ ] Implement Ollama service
- [ ] Create authentication service
- [ ] Build authentication router (signup, login)
- [ ] Build conversations router (CRUD operations)
- [ ] Build chat router (send message, get models)
- [ ] Create main application file
- [ ] Configure CORS middleware
- [ ] Set up Alembic migrations
- [ ] Create initial migration
- [ ] Apply migrations to database
- [ ] Test all endpoints
- [ ] Verify Gemini API integration
- [ ] Verify Ollama integration
- [ ] Document API endpoints

---

## PHASE 2: FRONTEND DEVELOPMENT

### 2.1 Design Philosophy & Aesthetic Direction

**Reference: Skills/Frontend SKILL.md**

#### 2.1.1 Conceptual Direction for Medical Chatbot

**Chosen Aesthetic: Clinical Elegance with Modern Digital Health Tone**

- **Purpose**: Create a trustworthy, professional medical consultation interface that feels both modern and reassuring
- **Tone**: Refined minimalism with subtle medical/health-focused accents
- **Differentiation**: Clean, spacious design with medical-grade professionalism but warm, approachable interface
- **Key Memory Point**: The unique split-scroll interface where conversations and messages scroll independently within a fixed 100vh container

#### 2.1.2 Typography Strategy

Following Frontend SKILL.md guidelines - avoid generic fonts (Inter, Roboto, Arial):

**Primary Typography Stack:**
- **Headings/Display**: "Instrument Sans" or "Cabinet Grotesk" - clean, professional, modern
- **Body Text**: "General Sans" or "Satoshi" - highly legible for medical content
- **Monospace (for technical info)**: "JetBrains Mono" or "IBM Plex Mono"

**Fallback Stack:**
```css
--font-display: 'Cabinet Grotesk', 'Helvetica Neue', sans-serif;
--font-body: 'Satoshi', -apple-system, system-ui, sans-serif;
--font-mono: 'JetBrains Mono', 'Courier New', monospace;
```

#### 2.1.3 Color Palette

**Avoid**: Generic purple gradients on white (common AI aesthetic)

**Medical Portal Palette:**
```css
:root {
  /* Primary - Medical Blue/Teal (trustworthy, professional) */
  --color-primary: #0A7EA4;
  --color-primary-light: #1E96BD;
  --color-primary-dark: #065A75;

  /* Secondary - Healing Green (calm, health-focused) */
  --color-secondary: #16A34A;
  --color-secondary-light: #22C55E;

  /* Neutral - Warm grays (softer than pure gray) */
  --color-bg-primary: #FAFAF9;
  --color-bg-secondary: #F5F5F4;
  --color-bg-tertiary: #FFFFFF;

  /* Text */
  --color-text-primary: #1C1917;
  --color-text-secondary: #57534E;
  --color-text-tertiary: #78716C;

  /* Borders */
  --color-border-light: #E7E5E4;
  --color-border-medium: #D6D3D1;

  /* Status Colors */
  --color-success: #16A34A;
  --color-warning: #EA580C;
  --color-error: #DC2626;

  /* AI Message Background */
  --color-ai-message: #F0F9FF;
  --color-user-message: #FAFAF9;
}
```

#### 2.1.4 Spatial Composition & Layout

**Key Layout Feature: Fixed 100vh with Dual-Scroll Areas**

```
┌─────────────────────────────────────────┐
│  Navigation Bar (fixed, ~60px)         │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┬───────────────────────┐  │
│  │          │                       │  │
│  │ Sidebar  │   Main Chat Area      │  │
│  │          │                       │  │
│  │ (scroll) │     (scroll)          │  │ } calc(100vh - 60px)
│  │          │                       │  │
│  │ ↕        │        ↕              │  │
│  │          │                       │  │
│  └──────────┴───────────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
```

**No page scroll** - Only sidebar and chat area scroll independently

### 2.2 Project Structure Setup

#### 2.2.1 Frontend Directory Structure

```
frontend/
├── public/
│   ├── fonts/
│   │   ├── CabinetGrotesk-Variable.woff2
│   │   └── Satoshi-Variable.woff2
│   └── favicon.ico
├── src/
│   ├── assets/
│   │   └── images/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── SignupForm.jsx
│   │   │   └── AuthLayout.jsx
│   │   ├── chat/
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   ├── MessageList.jsx
│   │   │   └── TypingIndicator.jsx
│   │   ├── conversations/
│   │   │   ├── ConversationList.jsx
│   │   │   ├── ConversationItem.jsx
│   │   │   └── NewConversationButton.jsx
│   │   ├── layout/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── MainLayout.jsx
│   │   ├── modals/
│   │   │   ├── ModelSelectorModal.jsx
│   │   │   └── ConfirmationModal.jsx
│   │   └── common/
│   │       ├── Button.jsx
│   │       ├── Input.jsx
│   │       ├── LoadingSpinner.jsx
│   │       └── ErrorMessage.jsx
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   └── ChatContext.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useChat.js
│   │   └── useConversations.js
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── Chat.jsx
│   │   └── NotFound.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── conversationService.js
│   │   └── chatService.js
│   ├── styles/
│   │   ├── global.css
│   │   ├── variables.css
│   │   ├── animations.css
│   │   └── fonts.css
│   ├── utils/
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   └── validators.js
│   ├── App.jsx
│   └── main.jsx
├── .env.local
├── .gitignore
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

### 2.3 Core Styling Setup

#### 2.3.1 CSS Variables (src/styles/variables.css)

**Reference: Frontend SKILL.md - Use CSS variables for consistency**

```css
:root {
  /* Typography */
  --font-display: 'Cabinet Grotesk', 'Helvetica Neue', sans-serif;
  --font-body: 'Satoshi', -apple-system, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;

  /* Font Sizes */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Colors (from 2.1.3) */
  --color-primary: #0A7EA4;
  --color-primary-light: #1E96BD;
  --color-primary-dark: #065A75;
  --color-secondary: #16A34A;
  --color-secondary-light: #22C55E;

  --color-bg-primary: #FAFAF9;
  --color-bg-secondary: #F5F5F4;
  --color-bg-tertiary: #FFFFFF;

  --color-text-primary: #1C1917;
  --color-text-secondary: #57534E;
  --color-text-tertiary: #78716C;

  --color-border-light: #E7E5E4;
  --color-border-medium: #D6D3D1;

  --color-success: #16A34A;
  --color-warning: #EA580C;
  --color-error: #DC2626;

  --color-ai-message: #F0F9FF;
  --color-user-message: #FAFAF9;

  /* Spacing */
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */

  /* Border Radius */
  --radius-sm: 0.375rem;   /* 6px */
  --radius-md: 0.5rem;     /* 8px */
  --radius-lg: 0.75rem;    /* 12px */
  --radius-xl: 1rem;       /* 16px */
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

  /* Layout */
  --navbar-height: 60px;
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 60px;

  /* Transitions */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 350ms ease;

  /* Z-Index */
  --z-dropdown: 1000;
  --z-modal: 2000;
  --z-toast: 3000;
}
```

#### 2.3.2 Global Styles (src/styles/global.css)

```css
@import './variables.css';
@import './fonts.css';
@import './animations.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  overflow: hidden; /* CRITICAL: No page scroll */
}

body {
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: 1.6;
  color: var(--color-text-primary);
  background-color: var(--color-bg-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#root {
  height: 100%;
  overflow: hidden; /* CRITICAL: No page scroll */
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: var(--font-semibold);
  line-height: 1.2;
}

h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
h4 { font-size: var(--text-xl); }
h5 { font-size: var(--text-lg); }
h6 { font-size: var(--text-base); }

a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--color-primary-dark);
}

button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  outline: none;
}

input, textarea {
  font-family: inherit;
  font-size: inherit;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-bg-secondary);
}

::-webkit-scrollbar-thumb {
  background: var(--color-border-medium);
  border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-tertiary);
}

/* Selection */
::selection {
  background-color: var(--color-primary-light);
  color: white;
}
```

#### 2.3.3 Animations (src/styles/animations.css)

**Reference: Frontend SKILL.md - Motion with staggered reveals and micro-interactions**

```css
/* Fade In Animation */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Slide In From Bottom */
@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Slide In From Left */
@keyframes slideInLeft {
  from {
    transform: translateX(-20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Slide In From Right */
@keyframes slideInRight {
  from {
    transform: translateX(20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Scale In */
@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* Pulse (for loading indicators) */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Typing Indicator */
@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
}

/* Shimmer Effect */
@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

/* Utility Classes */
.animate-fade-in {
  animation: fadeIn var(--transition-base) ease-out;
}

.animate-slide-up {
  animation: slideInUp var(--transition-base) ease-out;
}

.animate-slide-left {
  animation: slideInLeft var(--transition-base) ease-out;
}

.animate-slide-right {
  animation: slideInRight var(--transition-base) ease-out;
}

.animate-scale-in {
  animation: scaleIn var(--transition-base) ease-out;
}

/* Staggered Animation (for lists) */
.stagger-children > * {
  animation: slideInUp var(--transition-slow) ease-out;
  animation-fill-mode: backwards;
}

.stagger-children > *:nth-child(1) { animation-delay: 0ms; }
.stagger-children > *:nth-child(2) { animation-delay: 50ms; }
.stagger-children > *:nth-child(3) { animation-delay: 100ms; }
.stagger-children > *:nth-child(4) { animation-delay: 150ms; }
.stagger-children > *:nth-child(5) { animation-delay: 200ms; }
.stagger-children > *:nth-child(6) { animation-delay: 250ms; }
.stagger-children > *:nth-child(7) { animation-delay: 300ms; }
.stagger-children > *:nth-child(8) { animation-delay: 350ms; }

/* Hover Transitions */
.hover-lift {
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Focus Visible */
.focus-ring:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: var(--radius-md);
}
```

#### 2.3.4 Font Loading (src/styles/fonts.css)

```css
/* Cabinet Grotesk - Display Font */
@font-face {
  font-family: 'Cabinet Grotesk';
  src: url('/fonts/CabinetGrotesk-Variable.woff2') format('woff2-variations');
  font-weight: 400 700;
  font-display: swap;
}

/* Satoshi - Body Font */
@font-face {
  font-family: 'Satoshi';
  src: url('/fonts/Satoshi-Variable.woff2') format('woff2-variations');
  font-weight: 400 700;
  font-display: swap;
}

/* JetBrains Mono - Monospace */
@font-face {
  font-family: 'JetBrains Mono';
  src: url('/fonts/JetBrainsMono-Variable.woff2') format('woff2-variations');
  font-weight: 400 700;
  font-display: swap;
}

/* Note: Download fonts from:
   - Cabinet Grotesk: https://fontshare.com/fonts/cabinet-grotesk
   - Satoshi: https://fontshare.com/fonts/satoshi
   - JetBrains Mono: https://www.jetbrains.com/lp/mono/

   Place downloaded .woff2 files in /public/fonts/
*/
```

### 2.4 Service Layer Implementation

#### 2.4.1 API Configuration (src/services/api.js)

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle 401 Unauthorized
      if (error.response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }

      // Handle other errors
      const message = error.response.data?.detail || 'An error occurred';
      return Promise.reject(new Error(message));
    }

    return Promise.reject(error);
  }
);

export default api;
```

#### 2.4.2 Auth Service (src/services/authService.js)

```javascript
import api from './api';

export const authService = {
  // Signup
  async signup(userData) {
    const response = await api.post('/api/auth/signup', userData);
    return response.data;
  },

  // Login
  async login(credentials) {
    const response = await api.post('/api/auth/login', credentials);
    const { access_token } = response.data;

    // Store token
    localStorage.setItem('access_token', access_token);

    // Get user info
    const user = await this.getCurrentUser();
    localStorage.setItem('user', JSON.stringify(user));

    return { token: access_token, user };
  },

  // Logout
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  // Get current user
  async getCurrentUser() {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated() {
    const token = localStorage.getItem('access_token');
    return !!token;
  },

  // Get stored user
  getStoredUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
};
```

#### 2.4.3 Conversation Service (src/services/conversationService.js)

```javascript
import api from './api';

export const conversationService = {
  // Get all conversations
  async getConversations() {
    const response = await api.get('/api/conversations');
    return response.data;
  },

  // Get single conversation
  async getConversation(conversationId) {
    const response = await api.get(`/api/conversations/${conversationId}`);
    return response.data;
  },

  // Create new conversation
  async createConversation(data) {
    const response = await api.post('/api/conversations', data);
    return response.data;
  },

  // Update conversation
  async updateConversation(conversationId, data) {
    const response = await api.put(`/api/conversations/${conversationId}`, data);
    return response.data;
  },

  // Delete conversation
  async deleteConversation(conversationId) {
    await api.delete(`/api/conversations/${conversationId}`);
  },

  // Get messages for a conversation
  async getMessages(conversationId) {
    const response = await api.get(`/api/conversations/${conversationId}/messages`);
    return response.data;
  },
};
```

#### 2.4.4 Chat Service (src/services/chatService.js)

```javascript
import api from './api';

export const chatService = {
  // Send message
  async sendMessage(conversationId, content) {
    const response = await api.post(`/api/chat/${conversationId}/message`, {
      content,
    });
    return response.data;
  },

  // Get available Gemini models
  async getGeminiModels() {
    const response = await api.get('/api/chat/models/gemini');
    return response.data.models;
  },

  // Get available Ollama models
  async getOllamaModels() {
    const response = await api.get('/api/chat/models/ollama');
    return response.data.models;
  },

  // Check Ollama status
  async checkOllamaStatus() {
    const response = await api.get('/api/chat/ollama/status');
    return response.data;
  },
};
```

### 2.5 Context & State Management

#### 2.5.1 Auth Context (src/context/AuthContext.jsx)

```javascript
import React, { createContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          const storedUser = authService.getStoredUser();
          setUser(storedUser);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (credentials) => {
    try {
      const { user: loggedInUser } = await authService.login(credentials);
      setUser(loggedInUser);
      setIsAuthenticated(true);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const signup = async (userData) => {
    try {
      await authService.signup(userData);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
```

#### 2.5.2 Chat Context (src/context/ChatContext.jsx)

```javascript
import React, { createContext, useState, useCallback } from 'react';
import { conversationService } from '../services/conversationService';
import { chatService } from '../services/chatService';

export const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);

  // Load conversations
  const loadConversations = useCallback(async () => {
    try {
      setLoading(true);
      const data = await conversationService.getConversations();
      setConversations(data);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Load messages for a conversation
  const loadMessages = useCallback(async (conversationId) => {
    try {
      setLoading(true);
      const data = await conversationService.getMessages(conversationId);
      setMessages(data);
    } catch (error) {
      console.error('Failed to load messages:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Select conversation
  const selectConversation = useCallback(async (conversation) => {
    setActiveConversation(conversation);
    await loadMessages(conversation.id);
  }, [loadMessages]);

  // Create new conversation
  const createConversation = useCallback(async (data) => {
    try {
      const newConv = await conversationService.createConversation(data);
      setConversations((prev) => [newConv, ...prev]);
      setActiveConversation(newConv);
      setMessages([]);
      return newConv;
    } catch (error) {
      console.error('Failed to create conversation:', error);
      throw error;
    }
  }, []);

  // Send message
  const sendMessage = useCallback(async (content) => {
    if (!activeConversation || !content.trim()) return;

    try {
      setSending(true);

      // Optimistically add user message
      const userMessage = {
        role: 'user',
        content,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Send to backend
      const aiMessage = await chatService.sendMessage(activeConversation.id, content);

      // Add AI response
      setMessages((prev) => [...prev, aiMessage]);

      // Update conversation list (move to top)
      setConversations((prev) => {
        const updated = prev.filter((c) => c.id !== activeConversation.id);
        return [activeConversation, ...updated];
      });
    } catch (error) {
      console.error('Failed to send message:', error);
      // Remove optimistic message on error
      setMessages((prev) => prev.slice(0, -1));
      throw error;
    } finally {
      setSending(false);
    }
  }, [activeConversation]);

  // Delete conversation
  const deleteConversation = useCallback(async (conversationId) => {
    try {
      await conversationService.deleteConversation(conversationId);
      setConversations((prev) => prev.filter((c) => c.id !== conversationId));

      if (activeConversation?.id === conversationId) {
        setActiveConversation(null);
        setMessages([]);
      }
    } catch (error) {
      console.error('Failed to delete conversation:', error);
      throw error;
    }
  }, [activeConversation]);

  const value = {
    conversations,
    activeConversation,
    messages,
    loading,
    sending,
    loadConversations,
    selectConversation,
    createConversation,
    sendMessage,
    deleteConversation,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};
```

### 2.6 Custom Hooks

#### 2.6.1 useAuth Hook (src/hooks/useAuth.js)

```javascript
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }

  return context;
};
```

#### 2.6.2 useChat Hook (src/hooks/useChat.js)

```javascript
import { useContext } from 'react';
import { ChatContext } from '../context/ChatContext';

export const useChat = () => {
  const context = useContext(ChatContext);

  if (!context) {
    throw new Error('useChat must be used within ChatProvider');
  }

  return context;
};
```

#### 2.6.3 useConversations Hook (src/hooks/useConversations.js)

```javascript
import { useEffect } from 'react';
import { useChat } from './useChat';

export const useConversations = () => {
  const { conversations, loading, loadConversations } = useChat();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  return { conversations, loading, refresh: loadConversations };
};
```

### 2.7 Common Components

#### 2.7.1 Button Component (src/components/common/Button.jsx)

```jsx
import React from 'react';
import './Button.css';

export const Button = ({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  fullWidth = false,
  onClick,
  type = 'button',
  ...props
}) => {
  const classes = [
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    fullWidth && 'btn-full',
    loading && 'btn-loading',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      type={type}
      className={classes}
      disabled={disabled || loading}
      onClick={onClick}
      {...props}
    >
      {loading && <span className="btn-spinner"></span>}
      <span className={loading ? 'btn-text-hidden' : ''}>{children}</span>
    </button>
  );
};
```

**Button.css:**

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: var(--font-display);
  font-weight: var(--font-medium);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  cursor: pointer;
  border: none;
  outline: none;
  position: relative;
}

/* Sizes */
.btn-small {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
}

.btn-medium {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-base);
}

.btn-large {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-lg);
}

/* Variants */
.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-medium);
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--color-bg-tertiary);
  border-color: var(--color-border-medium);
}

.btn-danger {
  background-color: var(--color-error);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #B91C1C;
}

.btn-ghost {
  background-color: transparent;
  color: var(--color-text-secondary);
}

.btn-ghost:hover:not(:disabled) {
  background-color: var(--color-bg-secondary);
}

/* Full Width */
.btn-full {
  width: 100%;
}

/* Disabled */
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading */
.btn-loading {
  cursor: wait;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  position: absolute;
}

.btn-text-hidden {
  visibility: hidden;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

#### 2.7.2 Input Component (src/components/common/Input.jsx)

```jsx
import React from 'react';
import './Input.css';

export const Input = ({
  label,
  error,
  type = 'text',
  fullWidth = false,
  ...props
}) => {
  return (
    <div className={`input-wrapper ${fullWidth ? 'input-full' : ''}`}>
      {label && <label className="input-label">{label}</label>}
      <input
        type={type}
        className={`input ${error ? 'input-error' : ''}`}
        {...props}
      />
      {error && <span className="input-error-text">{error}</span>}
    </div>
  );
};
```

**Input.css:**

```css
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.input-full {
  width: 100%;
}

.input-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-secondary);
}

.input {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-md);
  background-color: var(--color-bg-tertiary);
  color: var(--color-text-primary);
  transition: all var(--transition-fast);
  outline: none;
}

.input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(10, 126, 164, 0.1);
}

.input-error {
  border-color: var(--color-error);
}

.input-error:focus {
  box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.1);
}

.input-error-text {
  font-size: var(--text-sm);
  color: var(--color-error);
}

.input::placeholder {
  color: var(--color-text-tertiary);
}
```

#### 2.7.3 Loading Spinner (src/components/common/LoadingSpinner.jsx)

```jsx
import React from 'react';
import './LoadingSpinner.css';

export const LoadingSpinner = ({ size = 'medium', text = '' }) => {
  return (
    <div className="spinner-container">
      <div className={`spinner spinner-${size}`}></div>
      {text && <p className="spinner-text">{text}</p>}
    </div>
  );
};
```

**LoadingSpinner.css:**

```css
.spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  padding: var(--space-8);
}

.spinner {
  border: 3px solid var(--color-bg-secondary);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner-small {
  width: 20px;
  height: 20px;
  border-width: 2px;
}

.spinner-medium {
  width: 40px;
  height: 40px;
}

.spinner-large {
  width: 60px;
  height: 60px;
  border-width: 4px;
}

.spinner-text {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

### 2.8 Layout Components

#### 2.8.1 Main Layout (src/components/layout/MainLayout.jsx)

**CRITICAL: This implements the fixed 100vh layout with no page scroll**

```jsx
import React from 'react';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import './MainLayout.css';

export const MainLayout = ({ children }) => {
  return (
    <div className="main-layout">
      <Navbar />
      <div className="main-content">
        <Sidebar />
        <main className="main-area">{children}</main>
      </div>
    </div>
  );
};
```

**MainLayout.css:**

```css
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* CRITICAL: Prevents page scroll */
}

.main-content {
  flex: 1;
  display: flex;
  height: calc(100vh - var(--navbar-height));
  overflow: hidden; /* CRITICAL: Prevents page scroll */
}

.main-area {
  flex: 1;
  overflow-y: auto; /* Only chat area scrolls */
  overflow-x: hidden;
  background-color: var(--color-bg-primary);
}
```

#### 2.8.2 Navbar (src/components/layout/Navbar.jsx)

```jsx
import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { LogOut, Settings, User } from 'lucide-react';
import './Navbar.css';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-brand">
          <div className="navbar-logo">
            <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
              <rect width="32" height="32" rx="8" fill="var(--color-primary)" />
              <path
                d="M16 8v16M8 16h16"
                stroke="white"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          </div>
          <h1 className="navbar-title">MediChat Portal</h1>
        </div>

        <div className="navbar-actions">
          <button
            className="navbar-user-btn"
            onClick={() => setShowDropdown(!showDropdown)}
          >
            <div className="user-avatar">
              {user?.full_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
            </div>
            <span className="user-name">{user?.full_name || user?.username}</span>
          </button>

          {showDropdown && (
            <div className="navbar-dropdown">
              <button className="dropdown-item">
                <User size={18} />
                <span>Profile</span>
              </button>
              <button className="dropdown-item">
                <Settings size={18} />
                <span>Settings</span>
              </button>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item danger" onClick={handleLogout}>
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};
```

**Navbar.css:**

```css
.navbar {
  height: var(--navbar-height);
  background-color: var(--color-bg-tertiary);
  border-bottom: 1px solid var(--color-border-light);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  height: 100%;
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 100%;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.navbar-logo {
  display: flex;
  align-items: center;
}

.navbar-title {
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  font-family: var(--font-display);
}

.navbar-actions {
  position: relative;
}

.navbar-user-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.navbar-user-btn:hover {
  background-color: var(--color-bg-secondary);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: var(--font-semibold);
  font-size: var(--text-sm);
}

.user-name {
  font-size: var(--text-base);
  color: var(--color-text-primary);
  font-weight: var(--font-medium);
}

.navbar-dropdown {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  min-width: 200px;
  background-color: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--space-2);
  animation: slideInUp 0.2s ease-out;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: transparent;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  transition: background-color var(--transition-fast);
  text-align: left;
}

.dropdown-item:hover {
  background-color: var(--color-bg-secondary);
}

.dropdown-item.danger {
  color: var(--color-error);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--color-border-light);
  margin: var(--space-2) 0;
}
```

#### 2.8.3 Sidebar (src/components/layout/Sidebar.jsx)

**CRITICAL: Sidebar scrolls independently**

```jsx
import React from 'react';
import { useChat } from '../../hooks/useChat';
import { useConversations } from '../../hooks/useConversations';
import { ConversationList } from '../conversations/ConversationList';
import { NewConversationButton } from '../conversations/NewConversationButton';
import { LoadingSpinner } from '../common/LoadingSpinner';
import './Sidebar.css';

export const Sidebar = () => {
  const { conversations, loading } = useConversations();
  const { activeConversation, selectConversation } = useChat();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2 className="sidebar-title">Conversations</h2>
        <NewConversationButton />
      </div>

      <div className="sidebar-content">
        {loading ? (
          <LoadingSpinner size="small" text="Loading conversations..." />
        ) : (
          <ConversationList
            conversations={conversations}
            activeConversation={activeConversation}
            onSelectConversation={selectConversation}
          />
        )}
      </div>
    </aside>
  );
};
```

**Sidebar.css:**

```css
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--color-bg-tertiary);
  border-right: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* CRITICAL: Container doesn't scroll */
}

.sidebar-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0; /* Don't shrink header */
}

.sidebar-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto; /* CRITICAL: Only content scrolls */
  overflow-x: hidden;
  padding: var(--space-3);
}
```

### 2.9 Conversation Components

#### 2.9.1 Conversation List (src/components/conversations/ConversationList.jsx)

```jsx
import React from 'react';
import { ConversationItem } from './ConversationItem';
import './ConversationList.css';

export const ConversationList = ({
  conversations,
  activeConversation,
  onSelectConversation,
}) => {
  if (conversations.length === 0) {
    return (
      <div className="conversation-list-empty">
        <p>No conversations yet.</p>
        <p>Click "New Chat" to start.</p>
      </div>
    );
  }

  return (
    <div className="conversation-list stagger-children">
      {conversations.map((conversation) => (
        <ConversationItem
          key={conversation.id}
          conversation={conversation}
          isActive={activeConversation?.id === conversation.id}
          onClick={() => onSelectConversation(conversation)}
        />
      ))}
    </div>
  );
};
```

**ConversationList.css:**

```css
.conversation-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.conversation-list-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8) var(--space-4);
  text-align: center;
  color: var(--color-text-tertiary);
  font-size: var(--text-sm);
  gap: var(--space-2);
}
```

#### 2.9.2 Conversation Item (src/components/conversations/ConversationItem.jsx)

```jsx
import React, { useState } from 'react';
import { useChat } from '../../hooks/useChat';
import { MessageSquare, Trash2, MoreVertical } from 'lucide-react';
import './ConversationItem.css';

export const ConversationItem = ({ conversation, isActive, onClick }) => {
  const { deleteConversation } = useChat();
  const [showMenu, setShowMenu] = useState(false);

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (confirm('Delete this conversation?')) {
      await deleteConversation(conversation.id);
    }
    setShowMenu(false);
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <div
      className={`conversation-item ${isActive ? 'active' : ''}`}
      onClick={onClick}
    >
      <div className="conversation-icon">
        <MessageSquare size={20} />
      </div>

      <div className="conversation-details">
        <div className="conversation-header">
          <h3 className="conversation-title">{conversation.title}</h3>
          <button
            className="conversation-menu-btn"
            onClick={(e) => {
              e.stopPropagation();
              setShowMenu(!showMenu);
            }}
          >
            <MoreVertical size={16} />
          </button>
        </div>

        {conversation.last_message_preview && (
          <p className="conversation-preview">
            {conversation.last_message_preview}
          </p>
        )}

        <div className="conversation-meta">
          <span className="conversation-model">{conversation.model_name}</span>
          <span className="conversation-date">
            {formatDate(conversation.updated_at || conversation.created_at)}
          </span>
        </div>
      </div>

      {showMenu && (
        <div className="conversation-menu">
          <button className="menu-item danger" onClick={handleDelete}>
            <Trash2 size={16} />
            <span>Delete</span>
          </button>
        </div>
      )}
    </div>
  );
};
```

**ConversationItem.css:**

```css
.conversation-item {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
  background-color: transparent;
  border: 1px solid transparent;
}

.conversation-item:hover {
  background-color: var(--color-bg-secondary);
  border-color: var(--color-border-light);
}

.conversation-item.active {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.conversation-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background-color: var(--color-bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
}

.conversation-item.active .conversation-icon {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.conversation-details {
  flex: 1;
  min-width: 0;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-1);
}

.conversation-title {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.conversation-item.active .conversation-title {
  color: white;
}

.conversation-menu-btn {
  opacity: 0;
  padding: var(--space-1);
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--color-text-tertiary);
  transition: opacity var(--transition-fast);
}

.conversation-item:hover .conversation-menu-btn,
.conversation-menu-btn:focus {
  opacity: 1;
}

.conversation-item.active .conversation-menu-btn {
  color: white;
  opacity: 0.8;
}

.conversation-preview {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: var(--space-2);
}

.conversation-item.active .conversation-preview {
  color: rgba(255, 255, 255, 0.8);
}

.conversation-meta {
  display: flex;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.conversation-item.active .conversation-meta {
  color: rgba(255, 255, 255, 0.7);
}

.conversation-model {
  padding: 2px 6px;
  background-color: var(--color-bg-secondary);
  border-radius: var(--radius-sm);
  font-weight: var(--font-medium);
}

.conversation-item.active .conversation-model {
  background-color: rgba(255, 255, 255, 0.2);
}

.conversation-menu {
  position: absolute;
  top: 100%;
  right: var(--space-2);
  margin-top: var(--space-1);
  background-color: var(--color-bg-tertiary);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: var(--space-1);
  z-index: 10;
  animation: scaleIn 0.15s ease-out;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  transition: background-color var(--transition-fast);
  width: 100%;
  text-align: left;
}

.menu-item:hover {
  background-color: var(--color-bg-secondary);
}

.menu-item.danger {
  color: var(--color-error);
}
```

#### 2.9.3 New Conversation Button (src/components/conversations/NewConversationButton.jsx)

```jsx
import React, { useState } from 'react';
import { useChat } from '../../hooks/useChat';
import { chatService } from '../../services/chatService';
import { Plus, Loader } from 'lucide-react';
import './NewConversationButton.css';

export const NewConversationButton = () => {
  const { createConversation } = useChat();
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState({ gemini: [], ollama: [] });
  const [formData, setFormData] = useState({
    title: '',
    model_type: 'gemini',
    model_name: 'gemini-pro',
  });

  const handleOpen = async () => {
    setShowModal(true);
    setLoading(true);

    try {
      const [geminiModels, ollamaModels] = await Promise.all([
        chatService.getGeminiModels(),
        chatService.getOllamaModels(),
      ]);

      setModels({
        gemini: geminiModels,
        ollama: ollamaModels,
      });
    } catch (error) {
      console.error('Failed to load models:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createConversation(formData);
      setShowModal(false);
      setFormData({ title: '', model_type: 'gemini', model_name: 'gemini-pro' });
    } catch (error) {
      console.error('Failed to create conversation:', error);
    }
  };

  return (
    <>
      <button className="new-conversation-btn" onClick={handleOpen}>
        <Plus size={18} />
      </button>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>New Conversation</h2>

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) =>
                    setFormData({ ...formData, title: e.target.value })
                  }
                  placeholder="Conversation title"
                  required
                />
              </div>

              <div className="form-group">
                <label>Model Type</label>
                <select
                  value={formData.model_type}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      model_type: e.target.value,
                      model_name:
                        e.target.value === 'gemini' ? 'gemini-pro' : 'llama2',
                    })
                  }
                >
                  <option value="gemini">Gemini (Cloud)</option>
                  <option value="ollama">Ollama (Local)</option>
                </select>
              </div>

              <div className="form-group">
                <label>Model</label>
                {loading ? (
                  <div className="loading-models">
                    <Loader size={16} className="spin" />
                    Loading models...
                  </div>
                ) : (
                  <select
                    value={formData.model_name}
                    onChange={(e) =>
                      setFormData({ ...formData, model_name: e.target.value })
                    }
                  >
                    {formData.model_type === 'gemini'
                      ? models.gemini.map((model) => (
                          <option key={model} value={model}>
                            {model}
                          </option>
                        ))
                      : models.ollama.map((model) => (
                          <option key={model.name} value={model.name}>
                            {model.name}
                          </option>
                        ))}
                  </select>
                )}
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
};
```

**NewConversationButton.css:**

```css
.new-conversation-btn {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background-color: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.new-conversation-btn:hover {
  background-color: var(--color-primary-dark);
  transform: scale(1.05);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
  animation: fadeIn 0.2s ease-out;
}

.modal-content {
  background-color: var(--color-bg-tertiary);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  max-width: 500px;
  width: 90%;
  animation: scaleIn 0.3s ease-out;
}

.modal-content h2 {
  margin-bottom: var(--space-6);
  color: var(--color-text-primary);
}

.form-group {
  margin-bottom: var(--space-5);
}

.form-group label {
  display: block;
  margin-bottom: var(--space-2);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-secondary);
}

.form-group input,
.form-group select {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  background-color: var(--color-bg-primary);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(10, 126, 164, 0.1);
}

.loading-models {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3);
  color: var(--color-text-tertiary);
  font-size: var(--text-sm);
}

.modal-actions {
  display: flex;
  gap: var(--space-3);
  justify-content: flex-end;
  margin-top: var(--space-6);
}

.btn-primary,
.btn-secondary {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border: none;
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
}

.btn-secondary {
  background-color: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-medium);
}

.btn-secondary:hover {
  background-color: var(--color-bg-secondary);
}

.spin {
  animation: spin 1s linear infinite;
}
```

### 2.10 Chat Components

#### 2.10.1 Message List (src/components/chat/MessageList.jsx)

**CRITICAL: Messages scroll independently within fixed height container**

```jsx
import React, { useEffect, useRef } from 'react';
import { ChatMessage } from './ChatMessage';
import { TypingIndicator } from './TypingIndicator';
import './MessageList.css';

export const MessageList = ({ messages, sending }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="message-list-empty">
          <h2>Start a conversation</h2>
          <p>Ask me anything about medical topics, symptoms, or health concerns.</p>
          <p className="disclaimer">
            <strong>Disclaimer:</strong> This is an AI assistant. Always consult
            healthcare professionals for medical advice.
          </p>
        </div>
      ) : (
        <div className="messages">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          {sending && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      )}
    </div>
  );
};
```

**MessageList.css:**

```css
.message-list {
  flex: 1;
  overflow-y: auto; /* CRITICAL: Messages scroll independently */
  overflow-x: hidden;
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
}

.message-list-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-12);
  animation: fadeIn 0.6s ease-out;
}

.message-list-empty h2 {
  font-size: var(--text-3xl);
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

.message-list-empty p {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
  max-width: 600px;
}

.message-list-empty .disclaimer {
  font-size: var(--text-sm);
  color: var(--color-text-tertiary);
  padding: var(--space-4);
  background-color: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  border-left: 3px solid var(--color-warning);
}

.messages {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}
```

#### 2.10.2 Chat Message (src/components/chat/ChatMessage.jsx)

```jsx
import React from 'react';
import { User, Bot } from 'lucide-react';
import './ChatMessage.css';

export const ChatMessage = ({ message }) => {
  const isUser = message.role === 'user';

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
    });
  };

  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-avatar">
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </div>

      <div className="message-content">
        <div className="message-header">
          <span className="message-sender">{isUser ? 'You' : 'AI Assistant'}</span>
          <span className="message-time">{formatTime(message.created_at)}</span>
        </div>

        <div className="message-text">
          {message.content.split('\n').map((line, i) => (
            <p key={i}>{line}</p>
          ))}
        </div>
      </div>
    </div>
  );
};
```

**ChatMessage.css:**

```css
.chat-message {
  display: flex;
  gap: var(--space-4);
  animation: slideInUp 0.3s ease-out;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-semibold);
}

.chat-message.user .message-avatar {
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: white;
}

.chat-message.assistant .message-avatar {
  background-color: var(--color-ai-message);
  color: var(--color-primary);
  border: 1px solid var(--color-primary-light);
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-2);
}

.message-sender {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
}

.message-time {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
}

.message-text {
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  line-height: 1.6;
}

.chat-message.user .message-text {
  background-color: var(--color-user-message);
  border: 1px solid var(--color-border-light);
  color: var(--color-text-primary);
}

.chat-message.assistant .message-text {
  background-color: var(--color-ai-message);
  border: 1px solid rgba(10, 126, 164, 0.2);
  color: var(--color-text-primary);
}

.message-text p {
  margin: 0;
}

.message-text p:not(:last-child) {
  margin-bottom: var(--space-3);
}

.message-text strong {
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
}

.message-text code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
}
```

#### 2.10.3 Chat Input (src/components/chat/ChatInput.jsx)

```jsx
import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import './ChatInput.css';

export const ChatInput = ({ onSend, disabled }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message);
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  return (
    <div className="chat-input-container">
      <form className="chat-input-form" onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          className="chat-input"
          placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={1}
        />

        <button
          type="submit"
          className="chat-send-btn"
          disabled={!message.trim() || disabled}
        >
          <Send size={20} />
        </button>
      </form>

      <p className="chat-input-disclaimer">
        AI can make mistakes. Verify medical information with healthcare professionals.
      </p>
    </div>
  );
};
```

**ChatInput.css:**

```css
.chat-input-container {
  border-top: 1px solid var(--color-border-light);
  background-color: var(--color-bg-tertiary);
  padding: var(--space-6);
  flex-shrink: 0; /* Don't shrink input area */
}

.chat-input-form {
  display: flex;
  gap: var(--space-3);
  align-items: flex-end;
  margin-bottom: var(--space-3);
}

.chat-input {
  flex: 1;
  min-height: 48px;
  max-height: 200px;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  font-family: var(--font-body);
  resize: none;
  overflow-y: auto;
  transition: border-color var(--transition-fast);
}

.chat-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(10, 126, 164, 0.1);
}

.chat-input:disabled {
  background-color: var(--color-bg-secondary);
  cursor: not-allowed;
}

.chat-send-btn {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background-color: var(--color-primary);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.chat-send-btn:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
  transform: scale(1.05);
}

.chat-send-btn:disabled {
  background-color: var(--color-border-medium);
  cursor: not-allowed;
  transform: none;
}

.chat-input-disclaimer {
  font-size: var(--text-xs);
  color: var(--color-text-tertiary);
  text-align: center;
  margin: 0;
}
```

#### 2.10.4 Typing Indicator (src/components/chat/TypingIndicator.jsx)

```jsx
import React from 'react';
import { Bot } from 'lucide-react';
import './TypingIndicator.css';

export const TypingIndicator = () => {
  return (
    <div className="chat-message assistant typing">
      <div className="message-avatar">
        <Bot size={20} />
      </div>

      <div className="message-content">
        <div className="message-header">
          <span className="message-sender">AI Assistant</span>
        </div>

        <div className="typing-indicator">
          <span className="typing-dot"></span>
          <span className="typing-dot"></span>
          <span className="typing-dot"></span>
        </div>
      </div>
    </div>
  );
};
```

**TypingIndicator.css:**

```css
.typing-indicator {
  display: flex;
  gap: 6px;
  padding: var(--space-4) var(--space-5);
  background-color: var(--color-ai-message);
  border: 1px solid rgba(10, 126, 164, 0.2);
  border-radius: var(--radius-lg);
  width: fit-content;
}

.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: var(--color-primary);
  animation: typing 1.4s infinite;
}

.typing-dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}
```

### 2.11 Authentication Components

#### 2.11.1 Auth Layout (src/components/auth/AuthLayout.jsx)

```jsx
import React from 'react';
import './AuthLayout.css';

export const AuthLayout = ({ children, title, subtitle }) => {
  return (
    <div className="auth-layout">
      <div className="auth-container">
        <div className="auth-header">
          <div className="auth-logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <rect width="48" height="48" rx="12" fill="var(--color-primary)" />
              <path
                d="M24 12v24M12 24h24"
                stroke="white"
                strokeWidth="3"
                strokeLinecap="round"
              />
            </svg>
          </div>
          <h1 className="auth-title">{title}</h1>
          {subtitle && <p className="auth-subtitle">{subtitle}</p>}
        </div>

        <div className="auth-content">{children}</div>
      </div>
    </div>
  );
};
```

**AuthLayout.css:**

```css
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    135deg,
    var(--color-bg-primary) 0%,
    var(--color-bg-secondary) 100%
  );
  padding: var(--space-6);
  overflow-y: auto;
}

.auth-container {
  width: 100%;
  max-width: 480px;
  background-color: var(--color-bg-tertiary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  padding: var(--space-10);
  animation: scaleIn 0.4s ease-out;
}

.auth-header {
  text-align: center;
  margin-bottom: var(--space-8);
}

.auth-logo {
  display: flex;
  justify-content: center;
  margin-bottom: var(--space-6);
  animation: fadeIn 0.6s ease-out;
}

.auth-title {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
  animation: slideInUp 0.5s ease-out;
}

.auth-subtitle {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  animation: slideInUp 0.5s ease-out 0.1s backwards;
}

.auth-content {
  animation: slideInUp 0.5s ease-out 0.2s backwards;
}
```

#### 2.11.2 Login Form (src/components/auth/LoginForm.jsx)

```jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import './AuthForm.css';

export const LoginForm = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);

    try {
      const result = await login(formData);
      if (result.success) {
        navigate('/chat');
      } else {
        setErrors({ general: result.error });
      }
    } catch (error) {
      setErrors({ general: 'An unexpected error occurred' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      {errors.general && <div className="error-banner">{errors.general}</div>}

      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        error={errors.email}
        fullWidth
        required
      />

      <Input
        label="Password"
        type="password"
        value={formData.password}
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        error={errors.password}
        fullWidth
        required
      />

      <Button type="submit" fullWidth loading={loading}>
        Login
      </Button>

      <p className="auth-link">
        Don't have an account? <Link to="/signup">Sign up</Link>
      </p>
    </form>
  );
};
```

#### 2.11.3 Signup Form (src/components/auth/SignupForm.jsx)

```jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import './AuthForm.css';

export const SignupForm = () => {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setLoading(true);

    try {
      const result = await signup(formData);
      if (result.success) {
        navigate('/login', { state: { message: 'Account created! Please login.' } });
      } else {
        setErrors({ general: result.error });
      }
    } catch (error) {
      setErrors({ general: 'An unexpected error occurred' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      {errors.general && <div className="error-banner">{errors.general}</div>}

      <Input
        label="Full Name"
        type="text"
        value={formData.full_name}
        onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
        fullWidth
      />

      <Input
        label="Username"
        type="text"
        value={formData.username}
        onChange={(e) => setFormData({ ...formData, username: e.target.value })}
        error={errors.username}
        fullWidth
        required
      />

      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        error={errors.email}
        fullWidth
        required
      />

      <Input
        label="Password"
        type="password"
        value={formData.password}
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        error={errors.password}
        fullWidth
        required
      />

      <Button type="submit" fullWidth loading={loading}>
        Sign Up
      </Button>

      <p className="auth-link">
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </form>
  );
};
```

**AuthForm.css:**

```css
.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.error-banner {
  padding: var(--space-4);
  background-color: rgba(220, 38, 38, 0.1);
  border: 1px solid var(--color-error);
  border-radius: var(--radius-md);
  color: var(--color-error);
  font-size: var(--text-sm);
  text-align: center;
}

.auth-link {
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-2);
}

.auth-link a {
  color: var(--color-primary);
  font-weight: var(--font-medium);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.auth-link a:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}
```

### 2.12 Pages

#### 2.12.1 Login Page (src/pages/Login.jsx)

```jsx
import React from 'react';
import { AuthLayout } from '../components/auth/AuthLayout';
import { LoginForm } from '../components/auth/LoginForm';

export const Login = () => {
  return (
    <AuthLayout
      title="Welcome Back"
      subtitle="Login to continue your medical consultations"
    >
      <LoginForm />
    </AuthLayout>
  );
};
```

#### 2.12.2 Signup Page (src/pages/Signup.jsx)

```jsx
import React from 'react';
import { AuthLayout } from '../components/auth/AuthLayout';
import { SignupForm } from '../components/auth/SignupForm';

export const Signup = () => {
  return (
    <AuthLayout
      title="Create Account"
      subtitle="Join MediChat Portal for AI-powered health assistance"
    >
      <SignupForm />
    </AuthLayout>
  );
};
```

#### 2.12.3 Chat Page (src/pages/Chat.jsx)

**CRITICAL: Implements fixed 100vh layout with dual-scroll areas**

```jsx
import React, { useEffect } from 'react';
import { useChat } from '../hooks/useChat';
import { MainLayout } from '../components/layout/MainLayout';
import { MessageList } from '../components/chat/MessageList';
import { ChatInput } from '../components/chat/ChatInput';
import './Chat.css';

export const Chat = () => {
  const { activeConversation, messages, sendMessage, sending, loadConversations } =
    useChat();

  useEffect(() => {
    loadConversations();
  }, [loadConversations]);

  const handleSendMessage = async (content) => {
    try {
      await sendMessage(content);
    } catch (error) {
      console.error('Failed to send message:', error);
      alert('Failed to send message. Please try again.');
    }
  };

  return (
    <MainLayout>
      <div className="chat-page">
        {activeConversation ? (
          <>
            <div className="chat-header">
              <h2 className="chat-title">{activeConversation.title}</h2>
              <div className="chat-info">
                <span className="chat-model">
                  {activeConversation.model_type}: {activeConversation.model_name}
                </span>
              </div>
            </div>

            <MessageList messages={messages} sending={sending} />
            <ChatInput onSend={handleSendMessage} disabled={sending} />
          </>
        ) : (
          <div className="chat-empty">
            <h2>No conversation selected</h2>
            <p>Select a conversation from the sidebar or create a new one</p>
          </div>
        )}
      </div>
    </MainLayout>
  );
};
```

**Chat.css:**

```css
.chat-page {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* CRITICAL: Prevents page scroll */
}

.chat-header {
  flex-shrink: 0; /* Don't shrink header */
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-border-light);
  background-color: var(--color-bg-tertiary);
}

.chat-title {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.chat-info {
  display: flex;
  gap: var(--space-3);
}

.chat-model {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  padding: var(--space-1) var(--space-3);
  background-color: var(--color-bg-secondary);
  border-radius: var(--radius-full);
  font-weight: var(--font-medium);
}

.chat-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  text-align: center;
  animation: fadeIn 0.6s ease-out;
}

.chat-empty h2 {
  font-size: var(--text-3xl);
  color: var(--color-text-primary);
  margin-bottom: var(--space-4);
}

.chat-empty p {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
}
```

#### 2.12.4 Not Found Page (src/pages/NotFound.jsx)

```jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './NotFound.css';

export const NotFound = () => {
  return (
    <div className="not-found">
      <h1>404</h1>
      <h2>Page Not Found</h2>
      <p>The page you're looking for doesn't exist.</p>
      <Link to="/" className="back-link">
        Go to Home
      </Link>
    </div>
  );
};
```

**NotFound.css:**

```css
.not-found {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-6);
}

.not-found h1 {
  font-size: 6rem;
  font-weight: var(--font-bold);
  color: var(--color-primary);
  margin-bottom: var(--space-4);
}

.not-found h2 {
  font-size: var(--text-3xl);
  color: var(--color-text-primary);
  margin-bottom: var(--space-3);
}

.not-found p {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-8);
}

.back-link {
  padding: var(--space-3) var(--space-6);
  background-color: var(--color-primary);
  color: white;
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  text-decoration: none;
  transition: all var(--transition-fast);
}

.back-link:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
```

### 2.13 App Configuration

#### 2.13.1 Main App Component (src/App.jsx)

```jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ChatProvider } from './context/ChatContext';
import { useAuth } from './hooks/useAuth';
import { Login } from './pages/Login';
import { Signup } from './pages/Signup';
import { Chat } from './pages/Chat';
import { NotFound } from './pages/NotFound';
import { LoadingSpinner } from './components/common/LoadingSpinner';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner size="large" text="Loading..." />;
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Public Route Component (redirect to chat if already authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner size="large" text="Loading..." />;
  }

  return !isAuthenticated ? children : <Navigate to="/chat" replace />;
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <ChatProvider>
          <Routes>
            {/* Public Routes */}
            <Route
              path="/login"
              element={
                <PublicRoute>
                  <Login />
                </PublicRoute>
              }
            />
            <Route
              path="/signup"
              element={
                <PublicRoute>
                  <Signup />
                </PublicRoute>
              }
            />

            {/* Protected Routes */}
            <Route
              path="/chat"
              element={
                <ProtectedRoute>
                  <Chat />
                </ProtectedRoute>
              }
            />

            {/* Redirects */}
            <Route path="/" element={<Navigate to="/chat" replace />} />

            {/* 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </ChatProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
```

#### 2.13.2 Main Entry Point (src/main.jsx)

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/variables.css';
import './styles/global.css';
import './styles/animations.css';
import './styles/fonts.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

#### 2.13.3 Vite Configuration (vite.config.js)

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

#### 2.13.4 Index HTML (index.html)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Medical Chatbot Portal - AI-powered health assistance" />
    <title>MediChat Portal</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### 2.14 Running the Frontend

#### 2.14.1 Development Server

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev

# Server will start at http://localhost:5173
```

#### 2.14.2 Build for Production

```bash
# Build production bundle
npm run build

# Preview production build
npm run preview
```

### 2.15 Frontend Phase 2 Checklist

#### Design & Styling
- [ ] Set up CSS variables with medical-themed color palette
- [ ] Implement global styles with no page scroll (fixed 100vh)
- [ ] Create animation keyframes and utility classes
- [ ] Set up custom font loading (Cabinet Grotesk, Satoshi, JetBrains Mono)
- [ ] Test responsive design

#### Services & State
- [ ] Configure Axios API client with interceptors
- [ ] Implement auth service (signup, login, logout)
- [ ] Implement conversation service (CRUD operations)
- [ ] Implement chat service (send messages, get models)
- [ ] Create Auth context and provider
- [ ] Create Chat context and provider
- [ ] Create custom hooks (useAuth, useChat, useConversations)

#### Common Components
- [ ] Build Button component with variants and loading states
- [ ] Build Input component with error handling
- [ ] Build LoadingSpinner component

#### Layout Components
- [ ] Build MainLayout with fixed 100vh structure
- [ ] Build Navbar with user dropdown
- [ ] Build Sidebar with independent scroll
- [ ] Test dual-scroll functionality (sidebar + messages)

#### Conversation Components
- [ ] Build ConversationList component
- [ ] Build ConversationItem with delete functionality
- [ ] Build NewConversationButton with model selection modal
- [ ] Implement staggered animations for conversation list

#### Chat Components
- [ ] Build MessageList with independent scroll
- [ ] Build ChatMessage component (user + AI variants)
- [ ] Build ChatInput with auto-resize textarea
- [ ] Build TypingIndicator with animated dots
- [ ] Implement auto-scroll to latest message

#### Authentication Components
- [ ] Build AuthLayout with centered design
- [ ] Build LoginForm with validation
- [ ] Build SignupForm with validation
- [ ] Implement error handling

#### Pages & Routing
- [ ] Create Login page
- [ ] Create Signup page
- [ ] Create Chat page
- [ ] Create NotFound page
- [ ] Implement protected routes
- [ ] Implement public routes with redirects
- [ ] Test navigation flow

#### Integration & Testing
- [ ] Test authentication flow (signup -> login -> chat)
- [ ] Test conversation creation with Gemini models
- [ ] Test conversation creation with Ollama models
- [ ] Test message sending and receiving
- [ ] Test conversation deletion
- [ ] Test dual-scroll areas (sidebar + messages)
- [ ] Verify no page scroll (only section scrolls)
- [ ] Test responsive design on different screen sizes
- [ ] Verify all animations and transitions
- [ ] Test error handling and edge cases

---

## IMPLEMENTATION SUMMARY

### Phase 0: Setup ✓
- Project structure created
- Dependencies installed
- Environment configured
- Database and Ollama set up

### Phase 1: Backend ✓
- Database models implemented (User, Conversation, Message)
- Authentication system with JWT
- Gemini API integration
- Ollama integration
- RESTful API endpoints
- All CRUD operations for conversations and messages

### Phase 2: Frontend ✓
**Design Philosophy**: Clinical elegance with modern digital health tone
**Key Feature**: Fixed 100vh layout with dual independent scroll areas

- React + Vite setup
- Custom medical-themed design system (avoiding generic AI aesthetics)
- Context-based state management
- Service layer for API communication
- Comprehensive component library
- Protected routing
- Responsive layout
- Staggered animations and micro-interactions

### Critical Features Implemented
1. **No Page Scroll**: 100vh fixed layout with only sidebar and chat area scrolling
2. **Multi-Model Support**: User can select between Gemini (cloud) and Ollama (local)
3. **Real-time Chat**: Message sending with typing indicators
4. **Conversation Management**: Create, select, delete conversations
5. **Authentication**: Secure JWT-based auth with protected routes
6. **Medical Context**: System prompts and disclaimers for medical conversations
7. **Distinctive Design**: Following Frontend SKILL.md guidelines for unique aesthetics

### Next Steps for Development
1. Download and place custom fonts in `/public/fonts/`
2. Start backend server: `uvicorn app.main:app --reload`
3. Start Ollama: `ollama serve`
4. Start frontend: `npm run dev`
5. Test complete user flow: signup → login → create conversation → chat
6. Refine styling and animations based on user testing
7. Add additional features (conversation search, message export, etc.)

---

## END OF PLAN

This comprehensive plan provides everything needed to build the medical chatbot portal from scratch, with explicit attention to:
- Backend architecture with dual AI model support
- Frontend design following distinctive aesthetic guidelines
- Critical 100vh fixed layout with dual-scroll functionality
- Complete implementation details for all components
- Step-by-step checklists for each phase

Follow this plan sequentially, testing each component before moving to the next.
