# 🧠 AI Personal Assistant (Production-Ready)

A full-stack AI-powered personal assistant with authentication, RAG memory, analytics dashboard, and Dockerized deployment.

---

## 🚀 Features

- 🔐 JWT Authentication
- 💬 Chat Interface (Typing animation)
- 🧠 RAG-based Memory (FAISS + Sentence Transformers)
- 📊 Admin Analytics Dashboard
- 🐳 Dockerized Backend & Frontend
- 🤖 Ollama LLM Integration
- 📦 Production-ready structure

---

## 🏗 Architecture

Frontend (React)
↓
FastAPI Backend
↓
RAG Layer (FAISS + Embeddings)
↓
Ollama LLM
↓
SQLite Database

---
🧠 RAG Flow

User sends message

Query embedded using sentence-transformers

FAISS retrieves relevant memory

Context sent to Ollama (phi3)

Response stored in DB

💰 Cost

Runs fully local. Zero cloud cost.

## 🐳 Run With Docker

```bash
docker compose up --build

Frontend: http://localhost:5173

Backend: http://localhost:8000

Ollama: http://localhost:11434

📊 Admin Analytics

Endpoint:

GET /admin/analytics


Shows:

Total Users

Total Messages

Most Active User

Messages per User

🧠 Tech Stack

Frontend:

React

Vite

Backend:

FastAPI

SQLAlchemy

JWT

FAISS

Sentence Transformers

AI:

Ollama (Phi3)

RAG pipeline

📌 Author

Meghna Pradhan
Full Stack AI Developer