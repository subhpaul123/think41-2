# 🛍️ E-Commerce Support Chatbot

An AI-powered support assistant for e-commerce platforms using **FastAPI + React + Groq LLM**. Supports persistent chat conversations and easy local dev with SQLite + Docker.


## 🧠 Features

-   Conversational AI using Groq (LLaMA 3)

-   Chat history stored per user + conversation

-   Full CRUD API for messages and conversations

-   SQLite for persistence

-   React UI to view and interact with chat

-   Alembic for DB migrations

-   Dockerized backend and frontend


## 🧱 Tech Stack

| Layer | Tech |
| --- | --- |
| Backend | FastAPI + SQLAlchemy + Alembic |
| Frontend | React (Vite) + Axios |
| Database | SQLite (via SQLAlchemy ORM) |
| AI | Groq API (LLaMA-3-70B) |
| DevOps | Docker + Docker Compose |


## ⚙️ Prerequisites

-   Python 3.10+

-   Node.js (v18+)

-   Docker & Docker Compose (optional)

-   Groq API key (get from https://console.groq.com/keys)


## 📁 Project Structure


```
ecom-support-chatbot/
├── backend/             ← FastAPI backend
│   ├── alembic/         ← Alembic migration folder
│   ├── models/          ← SQLAlchemy models
│   ├── routers/         ← API routes
│   ├── ecommerce.db     ← SQLite DB file (auto-created)
│   ├── main.py          ← FastAPI app
│   └── .env             ← Contains GROQ_API_KEY
│
├── frontend/            ← React app (Vite)
│   ├── src/components/  ← UI components
│   ├── src/context/     ← Global state
│   └── index.html
│
├── docker-compose.yml
└── README.md`

```

## 🚀 Getting Started (Without Docker)


### 🔁 0. Clone the Project

```bash
git clone https://github.com/your-username/ecom-support-chatbot.git
cd ecom-support-chatbot
```


### 🔧 1. Backend Setup


```bash
cd backend
# Create virtual env
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt`
```
### 📦 2. Set Groq API Key

Create a `.env` file in the `backend/` folder:

```env
GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 🧬 3. Run Alembic Migrations

Initialize (only once, already done):

```python
alembic init alembic
```

Then replace `alembic.ini` with:

```ini

[alembic]
script_location = %(here)s/alembic

prepend_sys_path = .

path_separator = os

sqlalchemy.url = sqlite:///./ecommerce.db


[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

And run migration:
```python
alembic revision --autogenerate -m "Initial tables"
alembic upgrade head
```

You should now see a file `ecommerce.db`.

### ▶️ 4. Start Backend

```bash
uvicorn main:app --reload --port 8000
```

-   API available at: <http://localhost:8000>

-   API docs: <http://localhost:8000/docs>


### 💻 5. Frontend Setup

```bash
cd frontend
```

#### Install dependencies
```bash
npm install
```

#### Run frontend
```
npm run dev
```

Frontend runs on: <http://localhost:5173>\
(Or whatever Vite logs in terminal.)


🧪 Sample API Call
------------------

### POST `/api/chat`


```json
{
  "user_id": 1,
  "message": "Where is my order?",
  "conversation_id": 3   // optional
}
```

### GET `/api/conversations/3`

Returns message history for a specific conversation.


🐳 Docker Setup (Optional)
--------------------------


```docker
# Build + start containers
docker-compose up --build`

-   React: <http://localhost:3000>

-   FastAPI: <http://localhost:8000>
```

### ✅ Checklist for Fresh Setup
---------------------------

```bash
# Clone the project
git clone https://github.com/yourname/ecom-support-chatbot
cd ecom-support-chatbot
```

#### Set backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=sk-..." > .env
alembic upgrade head
uvicorn main:app --reload
```

#### Set frontend
```bash
cd ../frontend
npm install
npm run dev
```


📌 Notes
--------

-   SQLite is used for simplicity. Can be swapped with PostgreSQL.

-   No frontend build config is needed for local dev.

-   Conversations/messages persist as long as `ecommerce.db` is intact.

-   Only minimal auth/user logic is implemented (by `user_id`).