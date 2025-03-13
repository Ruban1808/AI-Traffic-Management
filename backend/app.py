from flask import Flask, Response, jsonify
import cv2
import torch
import psycopg2
import pandas as pd
import numpy as np
from flask_cors import CORS
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="traffic_management",
        user="postgres",
        password="ruban123",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# Load YOLOv5 model safely
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    print("YOLOv5 model loaded successfully!")
except Exception as e:
    print(f"Error loading YOLOv5 model: {e}")
    model = None  # Set model to None to prevent crashes

# Load the traffic video
video_path = "traffic.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video file or stream.")
    exit()

vehicle_count = 0

def adjust_signal_time(predicted_count):
    """ Adjusts signal duration based on congestion level """
    if predicted_count > 30:
        return 60  # High congestion → 60 sec signal time
    elif predicted_count > 15:
        return 45  # Medium congestion → 45 sec signal time
    else:
        return 30  # Low congestion → 30 sec signal time

def generate_frames():
    global vehicle_count, model

    if model is None:
        print("Error: YOLOv5 model is not loaded. Cannot process video stream.")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Ensure model is available before processing
        if model:
            results = model(frame)
            detections = results.pandas().xyxy[0]

            vehicle_count = 0
            for _, row in detections.iterrows():
                label = row['name']
                if label in ["car", "truck", "bus", "motorcycle"]:
                    vehicle_count += 1
        else:
            vehicle_count = 0  # Default to 0 if model failed

        # Predict congestion and adjust signal timing
        cursor.execute("SELECT timestamp, vehicle_count FROM traffic_data ORDER BY timestamp ASC")
        data = cursor.fetchall()

        if len(data) > 10:
            df = pd.DataFrame(data, columns=['timestamp', 'vehicle_count'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['time_index'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()

            X = df[['time_index']]
            y = df['vehicle_count']

            # Use a separate variable for Linear Regression model to avoid conflicts
            traffic_model = LinearRegression()
            traffic_model.fit(X, y)

            future_time = (datetime.now() - df['timestamp'].min()).total_seconds() + 600
            predicted_count = traffic_model.predict([[future_time]])
            signal_time = adjust_signal_time(int(predicted_count[0]))
        else:
            signal_time = 30

        # Store vehicle count and signal time in PostgreSQL
        try:
            cursor.execute("INSERT INTO traffic_data (vehicle_count, signal_time) VALUES (%s, %s)", (vehicle_count, signal_time))
            conn.commit()
        except Exception as e:
            print(f"Database insertion error: {e}")

        # Convert frame to JPEG and send it
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/signal_time', methods=['GET'])
def get_signal_time():
    response = jsonify({"signal_time": 45})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response

@app.route('/vehicle_count', methods=['GET'])
def get_vehicle_count():
    """Returns the latest vehicle count detected"""
    return jsonify({"vehicle_count": vehicle_count})

@app.route('/traffic_data', methods=['GET'])
def get_traffic_data():
    """Fetches the last 10 traffic data entries from the database"""
    cursor.execute("SELECT timestamp, vehicle_count, signal_time FROM traffic_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/congestion_alert', methods=['GET'])
def congestion_alert():
    cursor.execute("SELECT vehicle_count FROM traffic_data ORDER BY timestamp DESC LIMIT 1")
    latest_count = cursor.fetchone()[0]

    alert = "No Congestion"
    if latest_count > 30:
        alert = "🚨 High Congestion! Immediate Attention Needed!"
    elif latest_count > 15:
        alert = "⚠️ Medium Congestion! Monitor Closely."

    return jsonify({"alert": alert})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
