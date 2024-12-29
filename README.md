# Project Setup

This project consists of two main parts:

1. **Client**: A Vite Vue 3 application written in TypeScript, located in the `client` folder.
2. **Server**: A Python Django backend using SQLite, located in the `server` folder.

## Prerequisites

Ensure you have the following installed:

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **pip** (Python package manager)

---

## Getting Started

### 1. Start the Client

Navigate to the `client` folder and run the following commands:

```bash
cd client
npm install
npm run dev
```

This will start the Vite development server. You can access the client at http://localhost:5173 by default.

### 2. Start the Server

Navigate to the server folder and run the following commands:

```bash
cd server
pip install -r requirements.txt
python manage.py runserver
```

This will start the Django development server. The backend will be available at http://127.0.0.1:8000 by default.
