
import cv2
import mediapipe as mp

from gestures.gesture_detector import detect_gesture


MODEL_PATH = "models/hand_landmarker.task"


# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2
)


with HandLandmarker.create_from_options(options) as landmarker:

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        exit()

    print("Webcam started.")
    print("Show your hand to the camera.")
    print("Gestures:")
    print("  Open Palm   -> OPEN_PALM")
    print("  Fist        -> FIST")
    print("  Two Fingers -> TWO_FINGERS")
    print("  One Finger  -> ONE_FINGER")
    print("Press Q to quit.")

    while True:

        ret, frame = cap.read()

        if not ret:
            print("ERROR: Could not read webcam frame.")
            break

        # Flip camera horizontally
        frame = cv2.flip(frame, 1)

        # Convert BGR -> RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert OpenCV image to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hands
        result = landmarker.detect(mp_image)

        # Default gesture
        gesture_text = "NO_HAND"

        # Draw landmarks and detect gesture
        if result.hand_landmarks:

            # Use the first detected hand
            hand_landmarks = result.hand_landmarks[0]

            # Detect gesture
            gesture_text = detect_gesture(hand_landmarks)

            # Get frame dimensions
            h, w, _ = frame.shape

            # Draw landmarks
            for landmark in hand_landmarks:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

        # Display detected gesture
        cv2.putText(
            frame,
            f"Gesture: {gesture_text}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Display window
        cv2.imshow(
            "AI Gesture Wallpaper - Gesture Detection",
            frame
        )

        # Quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

