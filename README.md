# 🖐️ AI Gesture Wallpaper Controller

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Computer%20Vision-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Real--Time%20Vision-red?logo=opencv)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow)

**An AI-powered Windows desktop application that uses real-time hand gesture recognition to control wallpapers through natural hand movements.**

Control your desktop wallpaper **without touching your keyboard or mouse** using computer vision, hand landmark detection, and gesture-based interaction.

## 📌 Project Overview

AI Gesture Wallpaper Controller combines computer vision and desktop automation to provide a touch-free wallpaper management system.

The application detects hand gestures through a webcam using MediaPipe and OpenCV and maps them to wallpaper actions such as changing wallpapers, switching categories, activating controls, and pausing the system.

## ✨ Features

- Real-time hand gesture recognition
- Touch-free Windows wallpaper control
- Gesture stabilization for reliable detection
- Multiple wallpaper categories
- Next/previous wallpaper navigation
- Next/previous category navigation
- Activate and pause controls
- Professional real-time dashboard
- Gesture stability indicator
- Recent action history
- Hand landmark visualization
- Modular project architecture

## 🖐️ Gesture Controls

| Gesture | Action |
|---|---|
| Open Palm | Activate controls |
| Fist | Pause controls |
| One Finger | Next wallpaper |
| Two Fingers | Previous wallpaper |
| Thumbs Up | Next category |
| Thumbs Down | Previous category |

## 🖥️ Application Preview

The application provides a real-time dashboard displaying the detected gesture, gesture stability, current wallpaper, wallpaper category, system status, and recent actions.

![AI Gesture Wallpaper Dashboard](screenshots/dashboard.png)

## 🧠 Technologies Used

- Python
- MediaPipe
- OpenCV
- NumPy
- Windows API
- Computer Vision
- Hand Landmark Detection

## 🏗️ Project Structure

```text
AI-Gesture-Wallpaper/
│
├── Wallpapers/
│   ├── Anime4K/
│   ├── Avengers4K/
│   └── Cars4K/
│
├── gestures/
│   └── gesture_detector.py
│
├── models/
│   └── hand_landmarker.task
│
├── ui/
│   ├── __init__.py
│   └── dashboard.py
│
├── src/
│   └── hand_detection_test.py
│
├── main.py
├── gesture_detection.py
├── wallpaper_controller.py
│
├── test_gestures.py
├── test_hand_tracking.py
├── test_wallpaper.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Harshith380/AI-Gesture-Wallpaper.git
```

### 2. Open the project

```bash
cd AI-Gesture-Wallpaper
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Start the application with:

```bash
python main.py
```

Make sure your webcam is available before starting the application.

Press:

```text
Q
```

to exit the application.

## 🧪 Testing

Individual components can be tested using:

```bash
python test_gestures.py
```

```bash
python test_hand_tracking.py
```

```bash
python test_wallpaper.py
```

## 🔄 How It Works

```text
Webcam
   ↓
OpenCV Video Capture
   ↓
MediaPipe Hand Landmark Detection
   ↓
Gesture Detection
   ↓
Gesture Stabilization
   ↓
Gesture → Action Mapping
   ↓
Wallpaper Controller
   ↓
Windows Desktop Wallpaper
```

## 🎯 Supported Wallpaper Categories

The project currently includes:

- Anime4K
- Avengers4K
- Cars4K

Additional categories can be added by creating a new folder inside:

```text
Wallpapers/
```

and placing supported image files inside it.

Supported image formats include:

```text
.jpg
.jpeg
.png
.bmp
.webp
```

## 🔐 Requirements

- Windows operating system
- Python 3.13+
- Webcam
- Internet connection for initial dependency/model setup

## 🚀 Future Improvements

- Voice control integration
- More gesture types
- Custom user-defined gestures
- Automatic wallpaper scheduling
- System tray support
- Gesture sensitivity configuration
- Machine-learning based gesture classification
- Performance optimization

## 👨‍💻 Author

**Harshith**

Computer Science Engineering Student

GitHub:
https://github.com/Harshith380

## ⭐ Project Highlights

This project demonstrates practical application of:

- Computer Vision
- AI-based gesture recognition
- Real-time video processing
- Desktop automation
- Python modular architecture
- Human-computer interaction