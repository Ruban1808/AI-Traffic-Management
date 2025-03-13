# 🚦 AI Traffic Management System

## 📌 Overview
The **AI Traffic Management System** is an intelligent traffic control solution that **optimizes traffic signals** based on real-time congestion levels. It uses **computer vision** to detect vehicles from live CCTV feeds, calculates congestion levels, and dynamically adjusts traffic signals to improve flow efficiency.

## 🎯 Features
✅ **Live Traffic Feed** with real-time video streaming  
✅ **Vehicle Detection** using AI-based computer vision  
✅ **Optimized Signal Timing** based on congestion levels  
✅ **Admin Dashboard** with real-time analytics & graphs  
✅ **Real-time Congestion Alerts** (Low, Medium, High)  

## 🏗️ Project Architecture
The system follows a **Monorepo** structure containing both **Frontend (React.js)** and **Backend (Flask + OpenCV + YOLOv5)** in a single repository.

```
📂 AI-Traffic-Management
│── 📂 backend
│   ├── app.py                  # Flask Backend API
│   ├── detection.py             # Vehicle Detection Logic (YOLO/OpenCV)
│   ├── requirements.txt         # Dependencies for Backend
│   ├── traffic_signal.py        # Traffic Signal Optimization Logic
│   ├── database.db              # SQLite Database (Stores Traffic Data)
│── 📂 frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── TrafficFeed.js   # Displays live traffic feed & congestion alerts
│   │   │   ├── AdminDashboard.js # Displays analytics (Recharts.js)
│   ├── package.json             # Dependencies for Frontend
│   ├── App.js                   # Main React Component
│── 📜 README.md                  # Documentation
```

## ⚙️ Tech Stack
| Component    | Technology Used |
|-------------|----------------|
| **Frontend** | React.js, Recharts.js |
| **Backend** | Flask, OpenCV, YOLOv5 |
| **Database** | SQLite |
| **AI Model** | YOLOv5 (for vehicle detection) |

## 🚀 Setup Instructions

### 📥 1. Clone the Repository
```bash
git clone https://github.com/your-repo/AI-Traffic-Management.git
cd AI-Traffic-Management
```

### ⚡ 2. Backend Setup
#### 🔹 Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 🔹 Run the Flask Backend
```bash
python app.py
```
✅ **Backend is now running on `http://127.0.0.1:5000/`**

---

### 💻 3. Frontend Setup
#### 🔹 Install Dependencies
```bash
cd frontend
npm install
```

#### 🔹 Start the React Frontend
```bash
npm start
```
✅ **Frontend is now running on `http://localhost:3000/`**

---

## 📊 API Endpoints

### 🚗 Vehicle Detection API
| Endpoint                  | Method | Description |
|---------------------------|--------|-------------|
| `/video_feed`             | GET    | Returns the live traffic feed |
| `/vehicle_count`          | GET    | Returns the number of detected vehicles |
| `/traffic_data`           | GET    | Fetches past traffic records |
| `/signal_time`            | GET    | Returns optimized signal time |

---

## 📧 Contact
For any issues or queries, reach out at **your-email@example.com**  

🚀 **Happy Coding!**
