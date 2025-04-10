# Chat to Chat 💬

A simple desktop real-time chat application built with **Python**, **FastAPI**, and **PyQt5**, deployed on **AWS EC2** with WebSocket support.

## ✨ Features

- ✅ Real-time messaging via WebSocket
- ✅ User-defined nickname
- ✅ Chat timestamp display
- ✅ Message auto-scroll
- ✅ Automatic local chat history saving (`chat_log_<username>.txt`)
- ✅ Server hosted on AWS EC2
- ✅ Client connection to public IP WebSocket service
- ✅ Chinese and English interface (coming soon)
- ✅ Auto-reconnect on failure (coming soon)

## 🖥 Technologies

- **Frontend (Desktop App)**: Python + PyQt5
- **Backend (API & WebSocket)**: FastAPI + Uvicorn
- **Protocol**: WebSocket
- **Deployment**: AWS EC2 (Linux)
- **Packaging**: PyInstaller (for `.exe`)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- `pip install -r requirements.txt`  
  (Dependencies: `fastapi`, `uvicorn`, `websockets`, `PyQt5`)

### Run Client

```bash
python client.py
