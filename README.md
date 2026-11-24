# SeeYou – AI Therapist Companion

SeeYou is a full-stack web app where users can talk with an AI companion between therapy sessions and keep track of their appointments. Each user's conversation history is stored, so the AI can follow up on what they said before instead of starting from zero every time.

The language model runs **locally** through [LM Studio](https://lmstudio.ai/), so conversations never leave your own machine. That matters for something as personal as therapy.

## Features

- **AI conversation:** the user sends a message, the backend loads that user's previous messages, and the LLM replies with a short acknowledgement and a follow-up question. Every reply is saved to PostgreSQL.
- **Accounts and authentication:** sign-up and login with passwords hashed using Argon2/bcrypt, and JWT access tokens protecting the user's own data.
- **Appointments:** create, list, update and delete therapy appointments from the dashboard.
- **Appointment check:** a background task runs every hour and finds appointments in the next 24 hours, as the base for reminders.
- **Tested API:** pytest tests for password hashing, tokens and the full user lifecycle (create, duplicate check, login, update, unauthorized update, delete).

## Tech stack

| Layer | Technologies |
|---|---|
| Backend | Python 3.12, FastAPI, SQLModel (SQLAlchemy), PostgreSQL, PyJWT, python-socketio |
| AI | LM Studio Python SDK with a locally hosted LLM (e.g. Llama) |
| Frontend | React 19, TypeScript, Vite, React Router, Bootstrap / Tailwind |
| Tooling | uv, Docker Compose, pytest, Ruff, Bruno (API collection) |

## Project structure

```
therapistai/
├── backend/
│   ├── therapistai/
│   │   ├── main.py          # FastAPI app, CORS, startup tasks
│   │   ├── auth.py          # password hashing, JWT creation and validation
│   │   ├── automation.py    # hourly check for upcoming appointments
│   │   ├── ai/              # LLM client and system prompt
│   │   ├── db/models/       # User, Message, Appointment
│   │   └── routers/         # user, token, message, appointment endpoints
│   ├── tests/               # pytest suite
│   └── docker-compose.yaml  # PostgreSQL
├── frontend/
│   └── src/components/      # Home, SignIn, SignUp, Dashboard, Appointments
└── therapistAI/             # Bruno collection to try the API
```

## How it works

```
React (Vite) ──HTTP + JWT──▶ FastAPI ──▶ PostgreSQL
                               │           (users, messages, appointments)
                               ▼
                         LM Studio (local LLM)
```

1. The user signs in and receives a JWT.
2. A message is posted to `POST /message/`. The backend saves it and loads the user's earlier messages.
3. The history is sent to the local LLM together with a system prompt, which keeps replies short, plain text and focused on a follow-up question.
4. The AI reply is stored and both messages are returned to the frontend.

## Getting started

### Requirements

- Python 3.12+ and [uv](https://docs.astral.sh/uv/)
- Node.js 22
- Docker
- [LM Studio](https://lmstudio.ai/) with a model downloaded and the local server started

### 1. Start the database

```bash
cd backend
docker compose up -d     # PostgreSQL on localhost:54321
```

### 2. Configure the backend

Copy the example file and fill in the values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `DATABASE_URL` | e.g. `postgresql://postgres:<password>@localhost:54321/therapistai` |
| `JWT_SECRET` | a long random string used to sign tokens |
| `LMS_API_HOST` | LM Studio server address, default `127.0.0.1:1234` |
| `MODEL` | the model identifier loaded in LM Studio |

### 3. Run the backend

```bash
uv sync
uv run --env-file .env fastapi dev therapistai/main.py
```

The API runs at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`.

### Run the tests

```bash
cd backend
uv run pytest
```

## API overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/user/` | Create an account |
| `POST` | `/login` | Log in and receive a JWT |
| `GET` | `/user/me` | Current user (auth required) |
| `PUT` / `DELETE` | `/user/{id}` | Update or delete a user (auth required) |
| `POST` | `/message/` | Send a message and get the AI reply (auth required) |
| `GET` | `/message/` | Conversation history (auth required) |
| `GET` / `POST` | `/appointment/` | List or create appointments |
| `PATCH` / `DELETE` | `/appointment/{id}` | Update or delete an appointment |

Full request examples are in the Bruno collection in `therapistAI/`.

## Roadmap

- Send reminders (email or in-app) from the upcoming-appointment check
- Finish Google sign-in (the button and OAuth settings are prepared)
- Stream AI replies in real time over Socket.IO
- Link appointments to users and add tests for messages and appointments
- Deploy the backend and frontend

## Disclaimer

SeeYou is a portfolio project. It is not a medical product and does not replace professional therapy.

## Author

**Minshi Wang** · [GitHub](https://github.com/wms198) · wang.minshi@icloud.com
