# Vision Event Engine

A real-time, event-driven computer vision system that converts live video input into **structured, reliable events** instead of fragile object guesses.

This project is designed with a **systems-first mindset**: correctness, stability, and clean architecture are prioritized over over-claiming model accuracy.

---

## 🔍 What This Project Does

- Consumes live webcam video
- Detects **people**, **hands**, and **validated objects (e.g. cell phone)**
- Tracks entities over time
- Emits **structured vision events**
- Stores events in SQLite
- Streams events via REST/WebSocket using FastAPI

The system **explicitly avoids false semantic claims**.  
If an object cannot be confidently identified, it is treated as `unknown_object`.

---

## 🧠 Design Philosophy

Most demo CV projects fail because they:
- Guess object labels incorrectly
- Over-trust pretrained models
- Collapse under real-world ambiguity

This system instead:
- Separates **perception** from **event logic**
- Uses **closed-set detection only where reliable**
- Refuses to hallucinate object identity
- Treats uncertainty as a first-class concept

> A system that says “unknown” is better than one that confidently lies.

---

## 🏗️ Architecture Overview

Webcam
↓
YOLOv8 (People, Cell Phone)
MediaPipe Hands (Hands)
↓
Entity Tracking & Memory
↓
Vision Events
├─ entity_appeared
├─ entity_disappeared
└─ hand_detected
↓
FastAPI (REST + WebSocket)
↓
SQLite Event Store



---

## 📦 Technologies Used

- **Python 3.10+**
- **OpenCV** – video capture & visualization
- **YOLOv8 (Ultralytics)** – reliable closed-set detection
- **MediaPipe Hands** – accurate hand detection
- **FastAPI + Uvicorn** – event API & WebSocket streaming
- **SQLite** – lightweight event storage
- **AsyncIO** – non-blocking event pipeline

---

## 📁 Project Structure

vision-event-engine/
├── app.py
├── engine/
│ ├── bus/ # Event bus & FastAPI server
│ ├── core/ # Event models & config
│ ├── detectors/ # YOLO & Hand detectors
│ ├── input/ # Video source
│ ├── processing/ # Entity tracking & memory
│ └── storage/ # SQLite event store
├── requirements.txt
├── README.md
└── .gitignore


---

## 🚀 How to Run

### 1. Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the application
python app.py

Webcam window will open

Events will be logged to SQLite

API runs on http://localhost:8000


📡 API Endpoints

GET /events – fetch recent vision events

WS /ws/events – real-time event stream via WebSocket



Example Event (Stored & Streamed)
{
  "timestamp": "2025-01-01T12:34:56Z",
  "event_type": "entity_appeared",
  "confidence": 1.0,
  "metadata": {
    "entity_id": "a8f21c",
    "label": "person"
  }
}



⚠️ Known Limitations (Intentional)

The system does not attempt fine-grained object identity

Objects not reliably detectable are treated as unknown_object

This avoids false positives and preserves correctness

Future work could add:

Supervised fine-tuning for task-specific object identity

Multi-camera input

Distributed event processing

🎯 Why This Matters

This project demonstrates:

Real-time CV system design

Event-driven architecture

Model limitation awareness

Engineering judgment under ambiguity

It is built to work reliably, not just look impressive.