# AI Gesture Wallpaper Controller

An AI-powered Windows desktop application that allows users to control and change wallpapers using real-time hand gestures.

The system uses computer vision and hand landmark detection to recognize predefined hand gestures and map them to wallpaper control actions.

---

## 🚀 Features

- Real-time hand gesture recognition
- AI-based hand landmark detection using MediaPipe
- Automatic wallpaper switching
- Multiple wallpaper categories
- Gesture-based category navigation
- Gesture stabilization to reduce accidental actions
- Professional real-time dashboard
- Gesture stability percentage
- Recent action history
- Windows desktop wallpaper integration
- Webcam-based interaction
- Responsive gesture control

---

## 🖐️ Gesture Controls

| Gesture | Action |
|---|---|
| Open Palm | Activate controls |
| Fist | Pause controls |
| One Finger | Next wallpaper |
| Two Fingers | Previous wallpaper |
| Thumbs Up | Next wallpaper category |
| Thumbs Down | Previous wallpaper category |

---

## 🖥️ Dashboard

The application provides a real-time dashboard displaying:

- Current detected gesture
- Gesture stability
- Controller status
- Current wallpaper category
- Current wallpaper
- Gesture mappings
- Recent actions
- Session running time

---

## 🧠 How It Works

The application follows a computer vision pipeline:

```text
Webcam
   ↓
OpenCV Frame Capture
   ↓
MediaPipe Hand Landmark Detection
   ↓
Hand Landmark Analysis
   ↓
Gesture Classification
   ↓
Gesture Stabilization
   ↓
Wallpaper Controller
   ↓
Windows Wallpaper