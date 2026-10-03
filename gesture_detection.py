import cv2
import mediapipe as mp
import math

MODEL_PATH = "models/hand_landmarker.task"

# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


def distance(point1, point2):
    """Calculate distance between two landmarks."""
    return math.sqrt(
        (point1.x - point2.x) ** 2 +
        (point1.y - point2.y) ** 2
    )


def detect_gesture(hand):
    """
    Detect basic hand gestures.

    Returns:
        OPEN PALM
        FIST
        THUMBS UP
        PEACE
        UNKNOWN
    """

    # -----------------------------
    # Landmark points
    # -----------------------------

    wrist = hand[0]

    thumb_tip = hand[4]
    thumb_ip = hand[3]

    index_tip = hand[8]
    index_pip = hand[6]

    middle_tip = hand[12]
    middle_pip = hand[10]

    ring_tip = hand[16]
    ring_pip = hand[14]

    pinky_tip = hand[20]
    pinky_pip = hand[18]

    # -----------------------------
    # Check finger states
    # -----------------------------

    index_open = (
        distance(index_tip, wrist)
        > distance(index_pip, wrist)
    )

    middle_open = (
        distance(middle_tip, wrist)
        > distance(middle_pip, wrist)
    )

    ring_open = (
        distance(ring_tip, wrist)
        > distance(ring_pip, wrist)
    )

    pinky_open = (
        distance(pinky_tip, wrist)
        > distance(pinky_pip, wrist)
    )

    thumb_open = (
        distance(thumb_tip, wrist)
        > distance(thumb_ip, wrist)
    )

    # -----------------------------
    # THUMBS UP
    # -----------------------------

    # IMPORTANT:
    # Check thumbs up BEFORE fist.
    # Otherwise thumbs up can be detected as fist.

    if (
        thumb_open
        and not index_open
        and not middle_open
        and not ring_open
        and not pinky_open
    ):
        return "THUMBS UP"

    # -----------------------------
    # PEACE / V SIGN
    # -----------------------------

    if (
        index_open
        and middle_open
        and not ring_open
        and not pinky_open
    ):
        return "PEACE"

    # -----------------------------
    # OPEN PALM
    # -----------------------------

    if (
        thumb_open
        and index_open
        and middle_open
        and ring_open
        and pinky_open
    ):
        return "OPEN PALM"

    # -----------------------------
    # FIST
    # -----------------------------

    if (
        not index_open
        and not middle_open
        and not ring_open
        and not pinky_open
    ):
        return "FIST"

    # -----------------------------
    # UNKNOWN
    # -----------------------------

    return "UNKNOWN"


# =====================================================
# CREATE HAND LANDMARKER
# =====================================================

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2
)


# =====================================================
# START HAND DETECTION
# =====================================================

with HandLandmarker.create_from_options(options) as landmarker:

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        exit()

    print("======================================")
    print("AI Gesture Detection Started")
    print("======================================")
    print("Show your hand to the camera.")
    print()
    print("Supported gestures:")
    print("  OPEN PALM")
    print("  FIST")
    print("  THUMBS UP")
    print("  PEACE")
    print()
    print("Press Q to quit.")
    print("======================================")

    while True:

        # Read webcam frame
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Could not read webcam frame.")
            break

        # Mirror the webcam
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hands
        result = landmarker.detect(mp_image)

        gesture = "NO HAND"

        # =================================================
        # PROCESS DETECTED HAND
        # =================================================

        if result.hand_landmarks:

            # Use the first detected hand
            hand = result.hand_landmarks[0]

            # Detect gesture
            gesture = detect_gesture(hand)

            # Get frame dimensions
            h, w, _ = frame.shape

            # Draw all landmarks
            for landmark in hand:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

        # =================================================
        # DISPLAY GESTURE
        # =================================================

        cv2.putText(
            frame,
            gesture,
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )

        # Show webcam
        cv2.imshow(
            "AI Gesture Detection",
            frame
        )

        # =================================================
        # QUIT
        # =================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release webcam
    cap.release()

    # Close OpenCV windows
    cv2.destroyAllWindows()

print("Gesture detection stopped.")